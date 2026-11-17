"""Run a real local Qwen conversation; the server must already be running."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.runtime import Agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trace',default='output/runs/interactive/events.jsonl')
    parser.add_argument('--base-url',default='http://127.0.0.1:18080')
    parser.add_argument('--demo',action='store_true')
    args = parser.parse_args()
    # Describe the actual project server; do not label a loaded LoRA as untrained.
    config_path = Path(__file__).resolve().parents[1]/'output/runtime/server_config.json'
    adapter = None
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding='utf-8-sig'))
        if args.base_url.rstrip('/') == f'http://127.0.0.1:{config["port"]}':
            adapter = config.get('adapter')
    agent = Agent(args.trace,base_url=args.base_url,additional_training=bool(adapter),
                  model_description='Official Qwen2.5-3B Q4_K_M'+(' + NF4-trained LoRA' if adapter else ''))
    smoke_path = Path(__file__).resolve().parents[1]/'data/fixtures/smoke.json'
    prompts = [turn['input'] for turn in json.loads(smoke_path.read_text(encoding='utf-8'))[0]['turns']]
    if args.demo:
        for prompt in prompts:
            print('USER:',prompt,flush=True)
            result = agent.turn(prompt)
            print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
            if not result['ok']:
                raise SystemExit(1)
    else:
        print('Korean Qwen Agent. /quit to stop.',flush=True)
        while True:
            try:
                prompt = input('USER> ')
            except EOFError:
                break
            if prompt.strip() == '/quit':
                break
            print(json.dumps(agent.turn(prompt),ensure_ascii=False,indent=2),flush=True)


if __name__ == '__main__':
    main()
