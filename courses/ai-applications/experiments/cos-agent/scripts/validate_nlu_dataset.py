"""Offline validator for Ppopy v3 3-Stage NLU SFT datasets."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from typing import Any

REPO_EXP_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_EXP_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_EXP_ROOT))

from beauty_agent.nlu_schema import DEFAULT_KB_SEED_PATH, load_nlu_whitelist, verify_nlu_extraction
from beauty_agent.slm.prompt_builder import SYSTEM_PROMPT_NLU, build_nlu_messages
from beauty_agent.v3_contracts import NLUExtractionResult, NLURequest

ALLOWED_SPLITS = frozenset({"train", "val_internal"})
_WS_RE = re.compile(r"\s+")


def _normalize_utterance_key(text: str) -> str:
    return _WS_RE.sub(" ", text).strip()


def validate_nlu_jsonl(
    input_path: Path,
    *,
    kb_seed_path: Path = DEFAULT_KB_SEED_PATH,
    min_rows: int = 1,
    enforce_buckets: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not input_path.is_file():
        return {
            "passed": False,
            "error_count": 1,
            "errors": [f"Input file not found: {input_path}"],
            "warnings": [],
        }

    raw_bytes = input_path.read_bytes()
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{input_path}: UTF-8 BOM is not allowed")
        raw_bytes = raw_bytes[3:]

    whitelist = load_nlu_whitelist(kb_seed_path)
    split_counts: Counter[str] = Counter()
    bucket_counts: Counter[str] = Counter()
    seen_ids: set[str] = set()
    split_source_texts: dict[str, set[str]] = {"train": set(), "val_internal": set()}
    split_families: dict[str, set[str]] = {"train": set(), "val_internal": set()}
    total_rows = 0

    # Split strictly on LF byte boundaries so U+2028/U+2029 inside JSON strings
    # are not misread as line breaks, and decode each line independently.
    for line_no, raw_line_bytes in enumerate(raw_bytes.split(b"\n"), start=1):
        if raw_line_bytes.endswith(b"\r"):
            raw_line_bytes = raw_line_bytes[:-1]
        if not raw_line_bytes.strip():
            continue
        total_rows += 1
        loc = f"{input_path.name}:{line_no}"
        try:
            line = raw_line_bytes.decode("utf-8").strip()
        except UnicodeDecodeError as exc:
            errors.append(f"{loc}: invalid UTF-8 bytes: {exc}")
            continue

        try:
            row = json.loads(line)
        except Exception as exc:
            errors.append(f"{loc}: invalid JSON: {exc}")
            continue

        if not isinstance(row, dict):
            errors.append(f"{loc}: row must be a JSON object, got {type(row).__name__}")
            continue

        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id.strip():
            errors.append(f"{loc}: missing non-empty 'id'")
        elif row_id in seen_ids:
            errors.append(f"{loc}: duplicate id {row_id!r}")
        else:
            seen_ids.add(row_id)

        family_id = row.get("scenario_family_id")
        if not isinstance(family_id, str) or not family_id.strip():
            errors.append(f"{loc}: missing non-empty 'scenario_family_id'")
            family_id = None

        split = row.get("split")
        if not isinstance(split, str):
            errors.append(f"{loc}: split must be a string, got {type(split).__name__}")
            continue
        if split == "test_internal":
            errors.append(f"{loc}: forbidden split 'test_internal' in training dataset")
            continue
        if split not in ALLOWED_SPLITS:
            errors.append(f"{loc}: invalid split {split!r}; expected one of {sorted(ALLOWED_SPLITS)}")
            continue
        split_counts[split] += 1
        if family_id is not None:
            split_families[split].add(family_id)

        messages = row.get("messages")
        if not isinstance(messages, list) or len(messages) != 3:
            errors.append(f"{loc}: messages must have 3 items [system, user, assistant]")
            continue
        if not all(isinstance(msg, dict) for msg in messages):
            errors.append(f"{loc}: every item in messages must be a JSON object")
            continue

        sys_msg, user_msg, asst_msg = messages
        if sys_msg.get("role") != "system" or sys_msg.get("content") != SYSTEM_PROMPT_NLU:
            errors.append(f"{loc}: system prompt mismatch with SYSTEM_PROMPT_NLU")
        if user_msg.get("role") != "user" or asst_msg.get("role") != "assistant":
            errors.append(f"{loc}: invalid message roles")
            continue

        user_content = user_msg.get("content")
        asst_content = asst_msg.get("content")
        if not isinstance(user_content, str) or not isinstance(asst_content, str):
            errors.append(f"{loc}: user and assistant message content must be strings")
            continue

        try:
            raw_user_obj = json.loads(user_content)
        except Exception as exc:
            errors.append(f"{loc}: user message content is not valid JSON: {exc}")
            continue
        if not isinstance(raw_user_obj, dict):
            errors.append(f"{loc}: user message JSON must be an object")
            continue

        try:
            req = NLURequest.model_validate(raw_user_obj)
        except Exception as exc:
            errors.append(f"{loc}: NLURequest validation failed: {exc}")
            continue

        expected_user_obj = json.loads(build_nlu_messages(req)[1]["content"])
        if raw_user_obj != expected_user_obj:
            extra_keys = sorted(set(raw_user_obj.keys()) - set(expected_user_obj.keys()))
            missing_keys = sorted(set(expected_user_obj.keys()) - set(raw_user_obj.keys()))
            errors.append(
                f"{loc}: user message JSON does not match build_nlu_messages() wire schema "
                f"(extra_keys={extra_keys}, missing_keys={missing_keys})"
            )

        try:
            ext = NLUExtractionResult.model_validate_json(asst_content)
        except Exception as exc:
            errors.append(f"{loc}: NLUExtractionResult validation failed: {exc}")
            continue

        try:
            verify_nlu_extraction(ext, request=req, whitelist=whitelist)
        except ValueError as exc:
            errors.append(f"{loc}: Stage 3 NLU verification failed: {exc}")

        split_source_texts[split].add(_normalize_utterance_key(req.source_text))

        # Coverage bucket accounting
        if req.previous_question:
            bucket_counts["turn2_followup"] += 1
        else:
            bucket_counts["turn1_utterance"] += 1
        if any(s.polarity == "denied" for s in ext.slot_candidates) or any(
            s.polarity == "denied" for s in ext.symptom_candidates
        ):
            bucket_counts["denied_polarity"] += 1
        if any(s.subject == "other" for s in ext.slot_candidates) or any(
            s.subject == "other" for s in ext.symptom_candidates
        ):
            bucket_counts["other_subject"] += 1
        if ext.symptom_candidates:
            bucket_counts["high_risk_symptom"] += 1
        if ext.product_mentions:
            bucket_counts["product_mention"] += 1
        if not ext.slot_candidates and not ext.symptom_candidates and not ext.product_mentions:
            bucket_counts["no_signal_noise"] += 1

    if total_rows < min_rows:
        errors.append(f"total_rows {total_rows} < min_rows {min_rows}")

    text_overlap = split_source_texts["train"] & split_source_texts["val_internal"]
    if text_overlap:
        errors.append(f"train/val_internal source_text leakage: {len(text_overlap)} shared utterance(s)")

    family_overlap = split_families["train"] & split_families["val_internal"]
    if family_overlap:
        errors.append(
            f"train/val_internal scenario_family_id leakage: {sorted(family_overlap)}"
        )

    if enforce_buckets:
        for required_bucket in (
            "turn2_followup",
            "denied_polarity",
            "other_subject",
            "high_risk_symptom",
            "product_mention",
            "no_signal_noise",
        ):
            if bucket_counts[required_bucket] == 0:
                errors.append(f"missing required NLU coverage bucket: {required_bucket}")

    return {
        "passed": len(errors) == 0,
        "input": str(input_path),
        "total_rows": total_rows,
        "split_counts": dict(sorted(split_counts.items())),
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "error_count": len(errors),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Ppopy v3 NLU SFT JSONL dataset.")
    parser.add_argument("--input", type=Path, required=True, help="Path to NLU SFT JSONL.")
    parser.add_argument("--kb-seed", type=Path, default=DEFAULT_KB_SEED_PATH)
    parser.add_argument("--min-rows", type=int, default=1)
    parser.add_argument("--enforce-buckets", action="store_true")
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    result = validate_nlu_jsonl(
        args.input,
        kb_seed_path=args.kb_seed,
        min_rows=args.min_rows,
        enforce_buckets=args.enforce_buckets,
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
