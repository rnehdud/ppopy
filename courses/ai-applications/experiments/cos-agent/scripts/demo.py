"""Run after starting the API. Uses synthetic JSON only."""
import json
from pathlib import Path

import httpx

payload = json.loads((Path(__file__).resolve().parents[1] / "examples/turn.json").read_text(encoding="utf-8"))
response = httpx.post("http://127.0.0.1:8000/v1/agent/turn", json=payload, timeout=20)
response.raise_for_status()
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
