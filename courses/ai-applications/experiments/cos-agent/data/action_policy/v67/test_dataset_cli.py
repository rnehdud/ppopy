"""Bundle integrity and split-preserving export regression tests (stdlib)."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import dataset_cli as cli


class BundleTests(unittest.TestCase):
    def test_verify_and_split_exports(self):
        result = cli.verify()
        self.assertEqual(result['turns'], 2453)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for split, expected in [('train', 1980), ('val_internal', 221), ('test_internal', 252)]:
                path = root / (split + '.jsonl')
                cli.export(cli.ROOT, split, 'messages', path)
                rows = cli.read_rows(path)
                self.assertEqual(len(rows), expected)
                self.assertEqual([m['role'] for m in rows[0]['messages']], ['system', 'user', 'assistant'])
                json.loads(rows[0]['messages'][1]['content'])
                json.loads(rows[0]['messages'][2]['content'])
                with self.assertRaises(FileExistsError):
                    cli.export(cli.ROOT, split, 'messages', path)
            sets = []
            for split in cli.SPLIT_FILES:
                path = root / ('afa-' + split + '.jsonl')
                cli.export(cli.ROOT, split, 'afa-scenarios', path)
                scenarios = cli.read_rows(path)
                self.assertTrue(all(s['split'] == split and s['source_pool_split'] == 'train' for s in scenarios))
                sets.append({s['scenario_id'] for s in scenarios})
            for i, first in enumerate(sets):
                for second in sets[i+1:]:
                    self.assertTrue(first.isdisjoint(second))
            self.assertEqual(len(set.union(*sets)), 1025)

    def test_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('v67-sft-manifest.json', 'canonical-candidates-v67.jsonl'):
                shutil.copyfile(cli.ROOT / name, root / name)
            with (root / 'canonical-candidates-v67.jsonl').open('ab') as stream:
                stream.write(b'\n')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                cli.verify(root)

    def test_policy_violation_rejected_even_with_updated_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ('v67-sft-manifest.json', 'canonical-candidates-v67.jsonl', *cli.SPLIT_FILES.values()):
                shutil.copyfile(cli.ROOT / name, root / name)
            path = root / 'v67-sft-train.jsonl'
            rows = cli.read_rows(path)
            rows[0]['input']['production_enabled'] = True
            path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
            manifest = json.loads((root / 'v67-sft-manifest.json').read_text(encoding='utf-8'))
            manifest['train_sha256'] = cli.digest(path)
            (root / 'v67-sft-manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'production boundary'):
                cli.verify(root)


if __name__ == '__main__':
    unittest.main()
