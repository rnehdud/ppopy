"""Evaluate all three already-trained adapters sequentially on local Qwen3."""
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
CONDITIONS=['sns_only','skin_only','mixed']


def ps(script,*args):
    subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'scripts'/script),*args],
                   cwd=ROOT,check=True)


def health():
    for _ in range(60):
        try:
            with urllib.request.urlopen('http://127.0.0.1:18081/health',timeout=3) as response:
                if json.load(response).get('status')=='ok':return
        except (urllib.error.URLError,TimeoutError):pass
        time.sleep(2)
    raise TimeoutError('Qwen3 server did not become ready')


def main():
    for name in CONDITIONS:
        path=ROOT/'output/training/aihub_ablation_v1'/name/'comparison.json'
        if not path.exists():raise FileNotFoundError('Training not finished: '+name)
    for name in CONDITIONS:
        destination=ROOT/'output/runs'/('aihub-ablation-v1-'+name)
        if destination.exists():
            if (destination/'results.json').exists() and (destination/'metadata.json').exists():
                print('Already evaluated:',name,flush=True)
                continue
            raise FileExistsError('Incomplete evaluation directory; preserve and inspect: '+str(destination))
        adapter=ROOT/'adapters'/('aihub-ablation-v1-'+name)
        gguf=adapter/'adapter-f32.gguf'
        if not gguf.exists():
            print('Converting adapter:',name,flush=True)
            with (adapter/'conversion.log').open('w',encoding='utf-8') as log:
                subprocess.run([str(ROOT/'.venv-train/Scripts/python.exe'),str(ROOT/'tmp/llama-converter/convert_lora_to_gguf.py'),
                                '--base',str(ROOT/'models/qwen3-4b-instruct-2507/tokenizer'),
                                '--outfile',str(gguf),'--outtype','f32',str(adapter)],cwd=ROOT,check=True,
                               stdout=log,stderr=subprocess.STDOUT)
        with gguf.open('rb') as f:
            if f.read(4)!=b'GGUF' or gguf.stat().st_size<1000000:
                raise ValueError('Invalid or incomplete GGUF adapter: '+str(gguf))
        print('Evaluating:',name,flush=True)
        ps('start_qwen3.ps1','-LoraPath',str(gguf.relative_to(ROOT)))
        try:
            health()
            with urllib.request.urlopen('http://127.0.0.1:18081/lora-adapters',timeout=10) as response:
                loaded=json.load(response)
            if isinstance(loaded,dict):loaded=loaded.get('data',loaded.get('value',[]))
            if not any(Path(x['path']).resolve()==gguf.resolve() and x['scale']==1.0 for x in loaded):
                raise ValueError('Expected adapter is not loaded')
            subprocess.run([sys.executable,str(ROOT/'scripts/evaluate_qwen3.py'),'--trained',
                            '--output',str(destination.relative_to(ROOT))],cwd=ROOT,check=True)
        finally:
            ps('stop_qwen3.ps1')
    subprocess.run([sys.executable,str(ROOT/'scripts/summarize_aihub_ablation.py')],cwd=ROOT,check=True)
    ps('start_qwen3.ps1')
    health()
    print('Finished. Unadapted Qwen3 server restored.',flush=True)


if __name__=='__main__':main()
