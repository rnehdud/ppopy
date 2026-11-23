#!/usr/bin/env python3
"""Deterministically extract eligible v67 recycling seeds (request_draft -> solution, hold -> hold).

Strictly excludes:
- v67-sft-test-internal.jsonl (zero evaluation leakage)
- Non-eligible actions (ask_user, confirm_candidate, resolve_conflict, retrieve_evidence)
- Forbidden card B-P07

Outputs a clean seed JSONL with preserved split, group_id, source_scenario_id, source_turn_id,
and structured judgment context ready for Stage-1/Stage-2 QLoRA dataset generation.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from collections import Counter
from typing import Any

COS_AGENT_DIR = pathlib.Path(__file__).resolve().parents[1]
ACTION_TO_MODE = {"request_draft": "solution", "hold": "hold"}


def extract_v67_seeds(v67_dir: pathlib.Path) -> tuple[list[dict[str, Any]], dict[str, int]]:
    seeds: list[dict[str, Any]] = []
    stats: Counter[str] = Counter()

    for split_name, filename in (
        ("train", "v67-sft-train.jsonl"),
        ("val_internal", "v67-sft-val-internal.jsonl"),
    ):
        path = v67_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Required v67 split file not found: {path}")
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            action = row.get("output", {}).get("action") if isinstance(row.get("output"), dict) else None
            mode = ACTION_TO_MODE.get(action or "")
            if mode is None:
                stats["skipped_action"] += 1
                continue
            card_ids = [c for c in row.get("card_ids", []) if c != "B-P07"]
            if not card_ids:
                stats["skipped_forbidden_card"] += 1
                continue

            inp = row.get("input", {})
            out = row.get("output", {})
            seed = {
                "mode": mode,
                "split": split_name,
                "source_origin": "recycled_v67",
                "source_scenario_id": row["scenario_id"],
                "source_turn_id": row["id"],
                "group_id": row["group_id"],
                "scenario_family_id": row.get("group_id") or row["scenario_id"],
                "card_ids": card_ids,
                "v67_action": action,
                "v67_target_id": out.get("target_id"),
                "v67_reason_summary": out.get("reason_summary"),
                "v67_hold_signals": inp.get("hold_signals", []),
                "v67_observations": inp.get("observations", {}),
                "v67_evidence": inp.get("evidence", {}),
                "v67_message": inp.get("message", ""),
            }
            seeds.append(seed)
            stats[f"{split_name}_{mode}"] += 1
            stats["total_extracted"] += 1

    return seeds, dict(stats)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract eligible v67 QLoRA recycling seeds.")
    parser.add_argument(
        "--v67-dir",
        type=pathlib.Path,
        default=COS_AGENT_DIR / "data" / "action_policy" / "v67",
        help="Path to data/action_policy/v67 directory.",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=COS_AGENT_DIR / "outputs" / "v67_qlora_seeds.jsonl",
        help="Output JSONL path for extracted seeds.",
    )
    args = parser.parse_args(argv)

    seeds, stats = extract_v67_seeds(args.v67_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "\n".join(json.dumps(s, ensure_ascii=False) for s in seeds) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "stats": stats}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
