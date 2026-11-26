"""Finish local measurement after a separately launched, real training process.

No uploads, Git operations or external messages. This is orchestration, not a
substitute for actual semantic review or human approval.
"""
import argparse,json,os,shlex,subprocess,sys,time
from pathlib import Path
from common import dump
HERE=Path(__file__).resolve().parent;COS=HERE.parents[1]

def wsl_path(value):
    path=Path(value).resolve().as_posix()
    assert path[1:3]==':/',path
    return '/mnt/'+path[0].lower()+path[2:]

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--model-path',required=True)
    p.add_argument('--training-pid',type=int);p.add_argument('--vllm-env',required=True)
    p.add_argument('--client-in-wsl',action='store_true',help='Measure WSL loopback explicitly, not Windows forwarding.')
    p.add_argument('--vllm-build-root');p.add_argument('--port',type=int,default=8018)
    p.add_argument('--gpu-fraction',type=float,default=.60);p.add_argument('--report',required=True)
    p.add_argument('--concurrency',type=int,default=1)
    p.add_argument('--speed-probe-baseline')
    a=p.parse_args();root=Path(a.run).resolve();report=Path(a.report).resolve()
    status=root/'pipeline_status.json';server=None
    def state(stage,**extra):
        value={'stage':stage,'timestamp_ms':int(time.time()*1000),'upload_executed':False,**extra}
        dump(status,value);print(json.dumps(value),flush=True)
    def command(stage,args):
        state(stage);log=root/(stage+'.log')
        with log.open('w',encoding='utf-8') as f:
            subprocess.run(args,cwd=COS,stdout=f,stderr=subprocess.STDOUT,check=True)
    stop_helper=root/'stop_own_vllm.py';pidfile=root/'vllm_server.pid'
    stop_helper.write_text('''import os,signal,sys
from pathlib import Path
p=Path(sys.argv[1])
if p.exists():
    pid=int(p.read_text().strip())
    try:
        cmd=Path(f"/proc/{pid}/cmdline").read_bytes()
        assert sys.argv[2].encode() in cmd and b"vllm" in cmd, "Not this task server; left untouched"
        assert os.getpgid(pid)==pid, "Not own isolated process group; left untouched"
        os.killpg(pid,signal.SIGTERM)
    except FileNotFoundError: pass
''',encoding='utf-8',newline='\n')
    try:
        import psutil
        if not (root/'training_complete.json').exists():
            assert a.training_pid,'training PID required while training is incomplete'
            process=psutil.Process(a.training_pid)
            assert 'train.py' in ' '.join(process.cmdline()) and str(root.name) in ' '.join(process.cmdline())
            state('waiting_for_actual_training',training_pid=a.training_pid)
            while not (root/'training_complete.json').exists():
                if not process.is_running():raise RuntimeError('training process stopped before completion receipt')
                time.sleep(5)
            process.wait(timeout=120)
        # Receipt is written only after both saved adapters and validation losses.
        complete=json.loads((root/'training_complete.json').read_text(encoding='utf-8'))
        assert complete['training_executed'] and complete['optimizer_steps']==204
        assert all((root/f'epoch-{i}'/'adapter_model.safetensors').stat().st_size>0 for i in [1,2])
        if pidfile.exists():raise RuntimeError('existing server PID receipt; inspect before starting another server')
        import httpx
        url=f'http://127.0.0.1:{a.port}/v1'
        # A firewall can DROP an unused localhost port, causing ConnectTimeout.
        # Check ownership/listeners instead of treating HTTP timeout as occupancy.
        assert not any(c.status=='LISTEN' and c.laddr.port==a.port for c in psutil.net_connections(kind='tcp')),'Windows port already listening; left untouched'
        subprocess.run(['wsl','-d','Ubuntu','--',a.vllm_env+'/bin/python','-c',
            'import socket,sys; s=socket.socket(); s.bind(("127.0.0.1",int(sys.argv[1]))); s.close()',str(a.port)],check=True)
        assert 1<=a.concurrency<=4,'measured local profiles are limited to 1..4'
        env_args=['env','PPOPY_VLLM_ENV='+a.vllm_env,'PPOPY_ADAPTER_ALIAS=ppopy-epoch-1',
            'PPOPY_MAX_NUM_SEQS='+str(a.concurrency)]
        if a.vllm_build_root:env_args+=['PPOPY_VLLM_BUILD_ROOT='+a.vllm_build_root]
        args=env_args+['bash',wsl_path(HERE/'serve_vllm.sh'),wsl_path(a.model_path),
            wsl_path(root/'epoch-1'),str(a.port),str(a.gpu_fraction),wsl_path(root/'epoch-2')]
        wrapper=root/'start_own_vllm.sh'
        wrapper.write_text('#!/usr/bin/env bash\nset -euo pipefail\necho $$ > '+shlex.quote(wsl_path(pidfile))+'\nexec '+shlex.join(args)+'\n',encoding='utf-8',newline='\n')
        state('starting_actual_wsl_vllm',gpu_fraction=a.gpu_fraction,concurrency=a.concurrency)
        with (root/'vllm_server.log').open('w',encoding='utf-8') as log:
            server=subprocess.Popen(['wsl','-d','Ubuntu','--','setsid','--wait','bash',wsl_path(wrapper)],stdout=log,stderr=subprocess.STDOUT)
            start=time.monotonic()
            while True:
                if server.poll() is not None:raise RuntimeError('WSL vLLM exited; inspect vllm_server.log')
                try:
                    if a.client_in_wsl:
                        probe=subprocess.run(['wsl','-d','Ubuntu','--',a.vllm_env+'/bin/python','-c',
                            'import httpx,sys; r=httpx.get(sys.argv[1],timeout=2,trust_env=False); r.raise_for_status(); print(r.text)',url+'/models'],capture_output=True,text=True)
                        if probe.returncode==0:
                            models=json.loads(probe.stdout);break
                    else:
                        response=httpx.get(url+'/models',timeout=2,trust_env=False)
                        if response.status_code==200:models=response.json();break
                except httpx.RequestError:pass
                if time.monotonic()-start>900:raise TimeoutError('WSL vLLM did not become ready within 900s')
                time.sleep(3)
            dump(root/'vllm_startup.json',{'elapsed_s':time.monotonic()-start,'models':models,
                'client_network_path':'WSL loopback' if a.client_in_wsl else 'Windows localhost forwarding',
                'server_max_num_seqs':a.concurrency,
                'gpu_fraction':a.gpu_fraction,'startup_is_separate_from_request_latency':True})
            client_python=(['wsl','-d','Ubuntu','--',a.vllm_env+'/bin/python'] if a.client_in_wsl else [sys.executable])
            client_path=wsl_path if a.client_in_wsl else str
            if a.speed_probe_baseline:
                command('throughput_probe',client_python+[client_path(HERE/'benchmark_throughput.py'),
                    '--baseline',client_path(a.speed_probe_baseline),'--output',client_path(root/'throughput_probe.json'),
                    '--concurrency',str(a.concurrency),'--base-url',url])
            command('vllm_quality',client_python+[client_path(HERE/'evaluate_vllm.py'),'--run',client_path(root),'--base-url',url,'--concurrency',str(a.concurrency)])
            selection=json.loads((root/'selection.json').read_text(encoding='utf-8'))
            alias='ppopy-'+selection['checkpoint']
            command('http_benchmark',client_python+[client_path(HERE/'benchmark_http.py'),'--base-url',url,
                '--output',client_path(root/'http'),'--adapter-model',alias,'--backend',
                'WSL vLLM; server_max_num_seqs='+str(a.concurrency)+'; benchmark_client_concurrency=1; client network path: '+('WSL loopback' if a.client_in_wsl else 'Windows localhost forwarding')])
            for tag,pred in [('base',root/'base/predictions.jsonl'),('epoch-1',root/'epoch-1/evaluation/predictions.jsonl'),
                    ('epoch-2',root/'epoch-2/evaluation/predictions.jsonl')]:
                command('review_pack_'+tag,[sys.executable,str(HERE/'review_pack.py'),'--predictions',str(pred),
                    '--output',str(root/(tag+'_review_request.jsonl'))])
            command('measured_report',[sys.executable,str(HERE/'report.py'),'--run',str(root),'--output',str(report),'--http',str(root/'http')])
        state('measurements_complete_semantic_review_pending',checkpoint=selection['checkpoint'],
            model_responses=270,human_approved=False,semantic_review_complete=False)
    except BaseException as exc:
        state('failed',error_type=type(exc).__name__,error=str(exc));raise
    finally:
        if server is not None:
            result=subprocess.run(['wsl','-d','Ubuntu','--',a.vllm_env+'/bin/python',wsl_path(stop_helper),
                wsl_path(pidfile),wsl_path(root)],capture_output=True,text=True)
            dump(root/'server_cleanup.json',{'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
            try:server.wait(timeout=30)
            except subprocess.TimeoutExpired:server.terminate()

if __name__=='__main__':main()
