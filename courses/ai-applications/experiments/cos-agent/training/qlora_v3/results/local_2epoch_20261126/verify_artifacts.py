"""공유 raw 자료와 별도 수령한 어댑터를 확인해요. 학습이나 의미 검수는 하지 않아요."""
from pathlib import Path
import argparse
import hashlib
import json


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--weights-root', type=Path, help='epoch-1/ 및 epoch-2/가 들어 있는 별도 가중치 폴더')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'artifact_manifest.json').read_text(encoding='utf-8'))
    errors = []
    for relative, expected in manifest['files'].items():
        path = root / relative
        if not path.is_file():
            errors.append(f'missing: {relative}')
        elif path.stat().st_size != expected['size_bytes'] or digest(path) != expected['sha256']:
            errors.append(f'bytes/hash mismatch: {relative}')
    predictions = []
    id_sets = []
    for tag in ['base', 'epoch-1', 'epoch-2']:
        rows = [json.loads(line) for line in (root / f'raw/{tag}_predictions.jsonl').read_text(encoding='utf-8').splitlines()]
        ids = [r['row_id'] for r in rows]
        if len(rows) != 90 or len(set(ids)) != 90:
            errors.append(f'{tag}: expected 90 distinct outputs')
        for row in rows:
            if row['split'] != 'val_internal' or hashlib.sha256(row['text'].encode('utf-8')).hexdigest() != row['content_sha256']:
                errors.append(f'{tag}/{row["row_id"]}: split/content hash mismatch')
        id_sets.append(set(ids))
        predictions.extend(rows)
    if not all(ids == id_sets[0] for ids in id_sets):
        errors.append('model validation ID sets differ')
    checked_weights = 0
    if args.weights_root is not None:
        metadata = json.loads((root / 'checkpoints/manifest.json').read_text(encoding='utf-8'))
        for checkpoint in metadata['checkpoints']:
            path = args.weights_root / f'epoch-{checkpoint["epoch"]}' / checkpoint['file']
            if not path.is_file():
                errors.append(f'weight missing: {path}')
            elif path.stat().st_size != checkpoint['size_bytes'] or digest(path) != checkpoint['sha256']:
                errors.append(f'weight mismatch: {path}')
            else:
                checked_weights += 1
    print(json.dumps({'files_checked': len(manifest['files']), 'raw_model_responses':len(predictions), 'weights_checked':checked_weights, 'semantic_review_performed':False, 'human_approved':False, 'errors':errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
