"""Fetch the pinned official Qwen baseline and tokenizer, without training."""
import hashlib
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GGUF_REPO = 'Qwen/Qwen2.5-3B-Instruct-GGUF'
GGUF_REV = '7dabda4d13d513e3e842b20f0d435c732f172cbe'
FILENAME = 'qwen2.5-3b-instruct-q4_k_m.gguf'
TOKENIZER_REV = 'aa8e72537993ba99e69dfaafa59ed015b17504d1'


def get_json(url):
    with urllib.request.urlopen(url, timeout=60) as res:
        return json.load(res)


def fetch(url, target, expected_size=None):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and (expected_size is None or target.stat().st_size == expected_size):
        return
    partial = target.with_suffix(target.suffix + '.partial')
    for attempt in range(4):
        have = partial.stat().st_size if partial.exists() else 0
        headers = {'User-Agent': 'Qwen-stateful-mvp/0.1'}
        if have:
            headers['Range'] = f'bytes={have}-'
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as res:
                append = have > 0 and res.status == 206
                if not append:
                    have = 0
                last_report = time.monotonic()
                with partial.open('ab' if append else 'wb') as out:
                    while chunk := res.read(4*1024*1024):
                        out.write(chunk)
                        have += len(chunk)
                        if time.monotonic() - last_report > 15:
                            print(f'{target.name}: {have/1024**2:.0f} MiB', flush=True)
                            last_report = time.monotonic()
            if expected_size is not None and partial.stat().st_size != expected_size:
                raise ValueError(f'Unexpected download size: {partial.stat().st_size} != {expected_size}')
            partial.replace(target)
            return
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2)


def main():
    model_dir = ROOT / 'models' / 'qwen2.5-3b-instruct'
    files = get_json(f'https://huggingface.co/api/models/{GGUF_REPO}/tree/{GGUF_REV}')
    info = next(x for x in files if x['path'] == FILENAME)
    target = model_dir / FILENAME
    print(f'Downloading official {GGUF_REPO}: {info["size"]/1024**3:.2f} GiB', flush=True)
    fetch(f'https://huggingface.co/{GGUF_REPO}/resolve/{GGUF_REV}/{FILENAME}', target, info['size'])
    print('Verifying model checksum...', flush=True)
    with target.open('rb') as model_file:
        digest = hashlib.file_digest(model_file, 'sha256').hexdigest()
    expected = info.get('lfs', {}).get('oid')
    if expected and digest != expected:
        raise ValueError('Model SHA256 mismatch')
    tokenizer_repo = 'Qwen/Qwen2.5-3B-Instruct'
    tok_info = get_json(f'https://huggingface.co/api/models/{tokenizer_repo}/revision/{TOKENIZER_REV}')
    tok_rev = tok_info['sha']
    tok_dir = model_dir / 'tokenizer'
    selected = ['config.json', 'tokenizer_config.json', 'tokenizer.json', 'vocab.json', 'merges.txt', 'LICENSE', 'README.md']
    available = {x['rfilename'] for x in tok_info['siblings']}
    for filename in selected:
        if filename in available:
            print('Tokenizer/metadata:', filename, flush=True)
            fetch(f'https://huggingface.co/{tokenizer_repo}/resolve/{tok_rev}/{filename}', tok_dir / filename)
    tokenizer_config = json.loads((tok_dir/'tokenizer_config.json').read_text(encoding='utf-8'))
    (model_dir/'chat_template.jinja').write_text(tokenizer_config['chat_template'],encoding='utf-8')
    manifest = {'model_repo':GGUF_REPO, 'model_revision':GGUF_REV, 'filename':FILENAME,
                'bytes':target.stat().st_size, 'sha256':digest, 'lfs_sha256_verified':bool(expected),
                'tokenizer_repo':tokenizer_repo,'tokenizer_revision':tok_rev,
                'quantization':'Q4_K_M','adapter':None,'additional_training':False}
    (model_dir/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,indent=2),flush=True)


if __name__ == '__main__':
    main()
