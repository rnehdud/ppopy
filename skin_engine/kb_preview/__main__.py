"""python -m skin_engine.kb_preview INPUT.json (stdout only; no network/storage)."""
import argparse
import json
from .engine import PreviewEngine

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input')
    args=parser.parse_args()
    with open(args.input,encoding='utf-8') as source: request=json.load(source)
    print(json.dumps(PreviewEngine().evaluate(request),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
