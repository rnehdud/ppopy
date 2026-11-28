"""Compatibility/security regression checks, not a relevance/clinical evaluation."""

import json
import shutil
import subprocess
import sys
from collections import Counter
from hashlib import sha256
from pathlib import Path

import pytest
from pydantic import ValidationError

from beauty_agent.rag.backends import HashFallback, NoOpReranker
from beauty_agent.rag.corpus import (
    export_chunks_jsonl,
    load_chunks_jsonl,
    load_corpus_entries,
)
from beauty_agent.rag.retriever import (
    RetrievalTrace,
    ScoredReference,
    TwoStageReferenceRetriever,
)
from beauty_agent.rag.selection import Layer2Selection
from beauty_agent.slm.prompt_builder import build_messages
from beauty_agent.v3_contracts import ReferenceChunk, SLMRequest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data/rag/layer2"


def entries():
    return load_corpus_entries(PACKAGE / "corpus")


def selection(entry):
    m = entry.chunk.layer2
    return Layer2Selection(
        **{
            k: getattr(m, k)
            for k in ("source_id", "jurisdiction", "document_version", "as_of")
        },
        purpose="source_explanation_only",
    )


def rag(rows, selections=(), **kw):
    return TwoStageReferenceRetriever(
        rows,
        HashFallback(),
        NoOpReranker(),
        threshold=-1,
        layer2_selections=selections,
        **kw,
    )


def test_real_export_92_and_combined_243_without_changing_l1(tmp_path):
    rows = entries()
    assert Counter(e.domain for e in rows) == {"regulatory": 76, "safety_method": 16}
    assert len({e.chunk.layer2.unit_id for e in rows}) == 92
    assert len({e.chunk.layer2.source_id for e in rows}) == 8
    assert not {"L2U-0060", "L2U-0252", "L2U-0595"} & {
        e.chunk.layer2.unit_id for e in rows
    }
    combined = load_corpus_entries(
        ROOT / "data/rag/corpus", additional_corpus_dirs=[PACKAGE / "corpus"]
    )
    assert len(combined) == 243
    assert [e.chunk for e in combined[:151]] == load_chunks_jsonl(
        ROOT / "data/rag/chunks.jsonl"
    )
    for pool in [rows, combined]:
        export_chunks_jsonl(pool, tmp_path / "chunks.jsonl")
        assert load_chunks_jsonl(tmp_path / "chunks.jsonl") == [e.chunk for e in pool]
    with pytest.raises(ValueError, match="Duplicate"):
        load_corpus_entries(
            PACKAGE / "corpus", additional_corpus_dirs=[PACKAGE / "corpus"]
        )


def test_all_metadata_and_unknowns_survive_prompt_and_roundtrip():
    rows = entries()
    unknown = [e for e in rows if "unknown" in e.chunk.layer2.effective_period]
    assert len(unknown) == 22
    for e in rows:
        c = ReferenceChunk.model_validate_json(e.chunk.model_dump_json())
        assert c == e.chunk
        assert sha256(c.text.encode()).hexdigest() == c.layer2.body_sha256
        assert c.evidence_ref == f"ref:{e.domain}-{c.layer2.unit_id}"
    c = unknown[0].chunk
    messages = build_messages(
        SLMRequest(
            mode="solution", rag_chunks=[c], allowed_evidence_refs=[c.evidence_ref]
        )
    )
    payload = json.loads(messages[1]["content"])
    assert payload["rag_chunks"][0]["layer2"] == c.layer2.model_dump()
    assert "현재 법적 적합성" in messages[0]["content"]


@pytest.mark.parametrize(
    "mutation",
    [
        "body",
        "missing_metadata",
        "hold",
        "reference_only",
        "duplicate",
        "hash",
        "extra_file",
        "missing_field",
    ],
)
def test_bad_package_fails_closed(tmp_path, mutation):
    dst = tmp_path / "layer2"
    shutil.copytree(PACKAGE, dst)
    meta = dst / "METADATA.md"
    if mutation == "body":
        p = dst / "corpus/regulatory.md"
        p.write_text(p.read_text().replace("bemotrizinol", "OTHER", 1))
    elif mutation == "missing_metadata":
        meta.unlink()
    elif mutation in {"hold", "reference_only"}:
        meta.write_text(
            meta.read_text().replace(
                "| verification_status | ready |",
                f"| verification_status | {mutation} |",
                1,
            )
        )
    elif mutation == "duplicate":
        meta.write_text(meta.read_text() + meta.read_text())
    elif mutation == "hash":
        p = dst / "CORPUS_MANIFEST.md"
        p.write_text(p.read_text().replace("`64a90fdd", "`74a90fdd", 1))
    elif mutation == "extra_file":
        (dst / "corpus/extra.md").write_text("# Unexpected\n")
    else:
        meta.write_text(
            meta.read_text().replace("| exposure_route | dermal |\n", "", 1)
        )
    with pytest.raises((ValueError, OSError)):
        load_corpus_entries(dst / "corpus")


def test_stable_ids_under_reordering(tmp_path):
    dst = tmp_path / "layer2"
    shutil.copytree(PACKAGE, dst)
    p = dst / "corpus/regulatory.md"
    text = p.read_text()
    preamble, *sections = text.split("\n## ")
    p.write_text(preamble + "\n## " + "\n## ".join(reversed(sections)))
    before = {e.chunk.evidence_ref: e.chunk for e in entries()}
    after = {e.chunk.evidence_ref: e.chunk for e in load_corpus_entries(dst / "corpus")}
    assert before == after


def test_scope_filter_before_top_k_and_reranker_and_again_at_select():
    rows = entries()
    target = next(e for e in rows if e.chunk.layer2.unit_id == "L2U-0001")
    selector = selection(target)
    r = rag(rows, [selector])
    captured = []

    def ranked(query, documents, prior_scores):
        captured.extend(documents)
        return [1.0] * len(documents)

    r.reranker.score = ranked
    result = r.retrieve("SCCS systemic exposure dose absorption")
    assert result.chunks and captured
    assert all(selector.matches(c) for c in result.chunks)
    eligible = {e.embedding_text for e in rows if selector.matches(e.chunk)}
    assert set(captured) <= eligible
    blocked = next(e for e in rows if not selector.matches(e.chunk))
    forged = RetrievalTrace(
        (ScoredReference(blocked.chunk.evidence_ref, 1, 1),), 0, 0, 0, 0
    )
    assert r.select(forged).chunks == []
    default = rag(rows)
    default.reranker.score = lambda *a: pytest.fail("ineligible docs reached reranker")
    assert default.retrieve("SCCS").chunks == []


@pytest.mark.parametrize(
    "field", ["source_id", "jurisdiction", "document_version", "as_of"]
)
def test_wrong_scope_returns_no_l2(field):
    rows = entries()
    data = selection(rows[0]).model_dump()
    data[field] = "mismatch"
    assert rag(rows, [Layer2Selection(**data)]).retrieve("sunscreen").chunks == []


def test_product_safety_purpose_rejected():
    data = selection(entries()[0]).model_dump()
    data["purpose"] = "current_product_safety"
    with pytest.raises(ValidationError):
        Layer2Selection(**data)


@pytest.mark.parametrize("mode", ["hold", "nlu"])
def test_non_solution_still_bypasses_backends(mode):
    rows = entries()
    r = rag(rows, [selection(rows[0])])
    r.embedder.encode = lambda *a, **kw: pytest.fail("non-solution called embedder")
    assert r.retrieve_for_request(SLMRequest(mode=mode)).chunks == []


def test_jsonl_and_mutable_input_cannot_drop_or_forge_metadata():
    c = entries()[0].chunk
    for field, value in [
        ("layer2", None),
        ("text", "modified"),
        ("evidence_ref", "ref:cleansing-001"),
    ]:
        data = c.model_dump()
        data[field] = value
        with pytest.raises(ValidationError):
            ReferenceChunk.model_validate(data)
    rows = entries()
    rows[0].chunk.layer2.verification_status = "hold"
    with pytest.raises(ValidationError):
        rag(rows)


def test_persisted_index_roundtrip_and_metadata_drift(tmp_path):
    rows = entries()
    selected = selection(rows[0])
    r = rag(rows, [selected])
    r.save(tmp_path)
    restored = rag(rows, [selected], build=False)
    restored.load(tmp_path)
    assert restored.retrieve("sunscreen") == r.retrieve("sunscreen")
    rows[0].chunk.layer2.as_of = "changed version context"
    with pytest.raises(ValueError, match="manifest"):
        rag(rows, build=False).load(tmp_path)


def test_cli_export_build_and_query(tmp_path):
    chunks = tmp_path / "chunks.jsonl"
    index = tmp_path / "index"

    def run(script, *args):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), *map(str, args)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)

    common = ["--additional-corpus", PACKAGE / "corpus"]
    exported = run("export_rag_chunks.py", *common, "--output", chunks)
    assert exported["total_chunks"] == 243
    built = run("build_rag_index.py", *common, "--chunks", chunks, "--output", index)
    assert built["count"] == 243
    result = run(
        "query_rag.py",
        "systemic exposure dose SCCS",
        *common,
        "--chunks",
        chunks,
        "--index",
        index,
        "--source-unit",
        "L2U-0001",
        "--threshold",
        -1,
    )
    assert any(c.get("layer2") for c in result["result"]["chunks"])
    assert all(
        c.get("layer2", {}).get("permitted_use", "source_explanation_only")
        == "source_explanation_only"
        for c in result["result"]["chunks"]
    )


def test_cannot_bypass_audit_by_retagging_as_layer1(tmp_path):
    dst = tmp_path / "layer2"
    shutil.copytree(PACKAGE, dst)
    path = dst / "corpus/regulatory.md"
    path.write_text(path.read_text().replace("[regulatory]", "[cleansing]"))
    with pytest.raises(ValueError, match="checksum"):
        load_corpus_entries(dst / "corpus")
