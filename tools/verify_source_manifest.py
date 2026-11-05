"""Verify exact imported files without reading the private source repository."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "docs/source-manifest.json").read_text(encoding="utf-8"))
    failures = []
    seen = set()
    for entry in manifest["files"]:
        relative = Path(entry["path"])
        if relative.is_absolute() or ".." in relative.parts or str(relative) in seen:
            failures.append(entry["path"])
            continue
        seen.add(str(relative))
        path = ROOT / relative
        if path.is_symlink() or not path.is_file():
            failures.append(entry["path"])
            continue
        raw = path.read_bytes()
        if len(raw) != entry["bytes"] or hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            failures.append(entry["path"])
    print(json.dumps({"checked": len(manifest["files"]), "failed": failures}, ensure_ascii=False))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
