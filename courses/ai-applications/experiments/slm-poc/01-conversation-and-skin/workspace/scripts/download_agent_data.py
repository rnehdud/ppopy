"""Download pinned public candidates for the Korean Qwen Agent MVP.

No model weights or training jobs are started. Evaluation data stays separate.
Run: python scripts/download_agent_data.py
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
HF_REV = 'c8b54e70bfbdd2fd6be037557e6feaf1abf14f5d'
GH_REV = '5ddb0b5bb37d6423e1f3381ef693cda811a7847e'
HF_REPO = 'heegyu/glaive-function-calling-v2-ko'
GH_REPO = 'kakao/FunctionChat-Bench'


def download(url: str, path: Path) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        temp = path.with_suffix(path.suffix + '.partial')
        req = urllib.request.Request(url, headers={'User-Agent': 'Korean-Agent-MVP-data-fetch/0.1'})
        with urllib.request.urlopen(req, timeout=120) as response, temp.open('wb') as out:
            while chunk := response.read(1024 * 1024):
                out.write(chunk)
        temp.replace(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'url': url,
            'bytes': path.stat().st_size, 'sha256': digest}


def main():
    manifest = {'downloaded_at_utc': datetime.now(timezone.utc).isoformat(), 'sources': []}
    train_dir = RAW / 'glaive-function-calling-v2-ko'
    train_info = {'id': HF_REPO, 'revision': HF_REV, 'purpose': 'training_candidate', 'files': []}
    for filename in ['README.md', 'train.json']:
        print('Obtaining training candidate:', filename, flush=True)
        train_info['files'].append(download(
            f'https://huggingface.co/datasets/{HF_REPO}/resolve/{HF_REV}/{filename}',
            train_dir / filename))
    raw_text = (train_dir / 'train.json').read_text(encoding='utf-8')
    try:
        records = json.loads(raw_text)
        train_info['actual_format'] = 'JSON array'
    except json.JSONDecodeError:
        # The source is named train.json but is newline-delimited JSON.
        records = [json.loads(line) for line in raw_text.splitlines() if line.strip()]
        train_info['actual_format'] = 'JSON Lines (source filename: train.json)'
    if not isinstance(records, list):
        raise ValueError('Unexpected training JSON structure')
    train_info['rows'] = len(records)
    train_info['fields'] = sorted(records[0].keys()) if records else []
    train_info['nonempty_korean_conversations'] = sum(bool(r.get('conversations_ko')) for r in records)
    train_info['schema_note'] = 'Raw candidate only; role, call arguments and conversation quality not yet normalized.'
    manifest['sources'].append(train_info)

    eval_dir = RAW / 'functionchat-bench'
    eval_info = {'id': GH_REPO, 'revision': GH_REV, 'purpose': 'evaluation_only', 'files': [], 'rows': {}}
    filenames = ['README.md', 'LICENSE', 'NOTICE.md',
                 'data/FunctionChat-CallDecision.jsonl', 'data/FunctionChat-Dialog.jsonl',
                 'data/FunctionChat-Singlecall.jsonl', 'data/system_prompt.txt',
                 'data/rubric_call.txt', 'data/rubric_completion.txt',
                 'data/rubric_relevance.txt', 'data/rubric_slot.txt']
    for filename in filenames:
        print('Obtaining evaluation asset:', filename, flush=True)
        eval_info['files'].append(download(
            f'https://raw.githubusercontent.com/{GH_REPO}/{GH_REV}/{filename}', eval_dir / filename))
        if filename.endswith('.jsonl'):
            lines = (eval_dir / filename).read_text(encoding='utf-8').splitlines()
            rows = [json.loads(line) for line in lines if line.strip()]
            eval_info['rows'][filename] = len(rows)
    manifest['sources'].append(eval_info)
    dest = RAW / 'download_manifest.json'
    dest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'manifest': str(dest), 'training_rows': train_info['rows'],
                      'evaluation_rows': eval_info['rows'],
                      'total_bytes': sum(f['bytes'] for source in manifest['sources'] for f in source['files'])},
                     ensure_ascii=False, indent=2), flush=True)


if __name__ == '__main__':
    main()
