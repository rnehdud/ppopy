"""가중치·학습 없이 공식 Qwen 토크나이저로 파일럿 호환성을 실측해요."""
from __future__ import annotations

import csv
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import statistics

from huggingface_hub import HfApi, hf_hub_download
from transformers import AutoTokenizer

COS = Path(__file__).resolve().parents[1]
MODEL = "Qwen/Qwen3-4B-Instruct-2507"

def main():
    source = COS / "data/qlora/v2/pilot_24.jsonl"
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=COS / "outputs/qlora_v3_pilot_20261125/qwen3_4b_2507_compatibility")
    out = parser.parse_args().output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines()]
    revision = HfApi().model_info(MODEL).sha
    tokenizer = AutoTokenizer.from_pretrained(MODEL,revision=revision,trust_remote_code=False)
    config_path = hf_hub_download(MODEL,"config.json",revision=revision)
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    measurements = []
    for row in rows:
        messages = row["messages"]
        rendered = tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=False)
        full = tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=False,return_dict=False)
        prefix = tokenizer.apply_chat_template(messages[:2],tokenize=True,add_generation_prompt=True,return_dict=False)
        prompt_text = tokenizer.apply_chat_template(messages[:2],tokenize=False,add_generation_prompt=True)
        assert rendered.startswith(prompt_text), row['id']
        encoded = tokenizer(rendered,add_special_tokens=False,return_offsets_mapping=True)
        assert encoded['input_ids'] == full
        # 경계 근처 BPE 병합을 고려해 전체 토큰열의 문자 오프셋으로 측정해요.
        boundary = next(i for i,(_,end) in enumerate(encoded['offset_mapping']) if end > len(prompt_text))
        prefix_matches = full[:len(prefix)] == prefix
        assert all(m["content"] in rendered for m in messages), row["id"]
        assert tokenizer.decode(tokenizer.encode(messages[2]["content"],add_special_tokens=False)) == messages[2]["content"]
        measurements.append({"id":row["id"],"split":row["split"],"mode":row["mode"],"total_tokens":len(full),"prompt_tokens":boundary,
                             "completion_tokens_with_end":len(full)-boundary,"assistant_text_tokens":len(tokenizer.encode(messages[2]["content"],add_special_tokens=False)),
                             "prompt_prefix_matches":prefix_matches,"ends_with_im_end":rendered.endswith("<|im_end|>\n")})
    total = [m["total_tokens"] for m in measurements]
    prompt = [m["prompt_tokens"] for m in measurements]
    completion = [m["completion_tokens_with_end"] for m in measurements]
    def stats(values):
        return {"min":min(values),"median":statistics.median(values),"max":max(values),"sum":sum(values)}
    report={"model":MODEL,"revision":revision,"dataset_sha256":before,"rows":len(rows),
            "library_versions":{p:importlib.metadata.version(p) for p in ["transformers","tokenizers","huggingface_hub"]},
            "config_max_position_embeddings":config.get("max_position_embeddings"),"eos_token":tokenizer.eos_token,"eos_token_id":tokenizer.eos_token_id,
            "native_template_has_generation_blocks":"{% generation" in tokenizer.chat_template or "{%generation" in tokenizer.chat_template,
            "native_template_has_think_literal":"<think>" in tokenizer.chat_template,
            "total_tokens":stats(total),"prompt_tokens":stats(prompt),"completion_tokens_with_end":stats(completion),
            "truncation_if_right_truncated":{str(limit):{"rows_exceeding":sum(m["total_tokens"]>limit for m in measurements),
                                                    "rows_losing_entire_assistant":sum(m["prompt_tokens"]>=limit for m in measurements)} for limit in [1024,2048,4096,8192]},
            "all_prompt_prefixes_match":all(m["prompt_prefix_matches"] for m in measurements),
            "all_end_markers_present":all(m["ends_with_im_end"] for m in measurements),
            "content_preserved_in_template":True,"assistant_text_token_roundtrip":True,
            "duplicate_answers":len(rows)-len({r["messages"][2]["content"] for r in rows}),
            "training_executed":False,"weights_downloaded":False,"gpu_memory_tested":False,"independent_content_reviewed":False}
    assert before == hashlib.sha256(source.read_bytes()).hexdigest()
    (out/"report.json").write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    with (out/"per_row_tokens.csv").open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(measurements[0])); writer.writeheader(); writer.writerows(measurements)
    # 외부 문서가 아니라 합성 1행에 모델 제어 토큰을 적용한 표시예요.
    example=tokenizer.apply_chat_template(rows[0]["messages"],tokenize=False,add_generation_prompt=False)
    (out/"first_row_chat_template.txt").write_bytes(example.encode("utf-8"))
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

if __name__ == "__main__":
    main()
