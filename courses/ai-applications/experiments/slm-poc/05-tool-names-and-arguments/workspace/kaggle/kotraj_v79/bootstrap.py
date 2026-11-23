# Kaggle v79: saved8000 evaluation followed by two isolated ablations and control.
EXPECTED_INPUT_SHA256 = '__INPUT_SHA256__'
SESSION_HOURS = 9.0
EVALUATE_ONLY = False

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import zipfile

ROOT = Path('/kaggle/working/kotraj_v79')
OUT = ROOT/'results'
RESULT = Path('/kaggle/working/kotraj-v79-results.zip')
START = time.time()


def hardware_probe(report_path=None):
    """Check the assigned hardware before installing packages or touching model data."""
    report={'CUDA_VISIBLE_DEVICES':os.environ.get('CUDA_VISIBLE_DEVICES'),
            'NVIDIA_VISIBLE_DEVICES':os.environ.get('NVIDIA_VISIBLE_DEVICES')}
    try:
        result=subprocess.run(['nvidia-smi','-L'],text=True,capture_output=True,timeout=20)
        report.update(returncode=result.returncode,stdout=result.stdout.strip(),stderr=result.stderr.strip())
    except (OSError,subprocess.TimeoutExpired) as error:
        report['error']=str(error)
    report['gpu_assigned']=report.get('returncode')==0 and any(
        line.strip().startswith('GPU ') for line in report.get('stdout','').splitlines())
    report_path=report_path or OUT/'hardware-probe.json'
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,indent=2),encoding='utf-8')
    if not report['gpu_assigned']:
        raise RuntimeError('No NVIDIA GPU was detected by nvidia-smi in this Kaggle session. '
            'Select Settings > Accelerator > GPU T4 x2, restart the session, then Save & Run All. '
            'Notebook metadata alone does not confirm GPU allocation. See hardware-probe.json.')
    print('Assigned hardware:',report['stdout'],flush=True)
    return report


def worker_environment(source):
    env=dict(source);env.pop('PYTHONPATH',None)
    env.update(PIP_CACHE_DIR='/tmp/kotraj-pip-cache',HF_HUB_CACHE='/tmp/kotraj-hf-cache',
               PYTHONNOUSERSITE='1',PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false')
    # Keep the platform's CUDA visibility mapping. Native selects device0 within that mapping.
    return env


def private_gpu_probe(python,env):
    code='''import json,sys,torch
r={"python":sys.executable,"torch":torch.__version__,"torch_cuda_build":torch.version.cuda,
   "cuda_available":torch.cuda.is_available(),"device_count":torch.cuda.device_count()}
try:
    torch.cuda.init()
    r["device_name"]=torch.cuda.get_device_name(0)
    torch.empty(1,device="cuda")
    r["allocation_ok"]=True
except Exception as e:
    r["initialization_error"]=type(e).__name__+": "+str(e)
print("KOTRAJ_GPU_REPORT="+json.dumps(r))
'''
    result=subprocess.run([str(python),'-c',code],env=env,text=True,capture_output=True,timeout=90)
    matches=[line.split('=',1)[1] for line in result.stdout.splitlines() if line.startswith('KOTRAJ_GPU_REPORT=')]
    report=json.loads(matches[-1]) if matches else {}
    report.update(returncode=result.returncode,stderr=result.stderr.strip())
    (OUT/'private-gpu-probe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    if not (report.get('cuda_available') and report.get('allocation_ok')):
        raise RuntimeError('An NVIDIA GPU was detected, but the private PyTorch environment cannot use CUDA. '
            'See private-gpu-probe.json for the exact PyTorch build and initialization error. '
            +report.get('initialization_error',report.get('stderr','No probe output.')))
    print('Private PyTorch GPU:',report['device_name'],'torch:',report['torch'],flush=True)
    return report


def resume_has_progress(source,manifest=None):
    z=zipfile.ZipFile(source) if source.is_file() else None
    try:
        m=manifest or json.loads(z.read('resume-v79.json') if z else (source/'resume-v79.json').read_bytes())
        if m.get('artifact_type')=='setup-diagnostics':return False
        for name in m['files']:
            if name.endswith('/predictions.jsonl'):
                size=z.getinfo(name).file_size if z else (source/name).stat().st_size
                if size:return True
            if name.endswith('/state.json'):
                state=json.loads(z.read(name) if z else (source/name).read_bytes())
                if state.get('count',0)>0:return True
        return False
    finally:
        if z:z.close()


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()


def install(source, marker, expected=None):
    z=zipfile.ZipFile(source) if source.is_file() else None
    try:
        raw=z.read(marker) if z else (source/marker).read_bytes()
        if expected:assert hashlib.sha256(raw).hexdigest()==expected
        m=json.loads(raw)
        if marker=='resume-v79.json':assert m['input_manifest_sha256']==EXPECTED_INPUT_SHA256
        for name,digest in m['files'].items():
            target=(ROOT/name).resolve(); target.relative_to(ROOT.resolve())
            if marker=='resume-v79.json':target.relative_to(OUT.resolve())
            if target.exists():
                assert sha(target)==digest,'Existing output differs: '+name
                continue
            target.parent.mkdir(parents=True,exist_ok=True)
            if z:
                with z.open(name) as src,target.open('xb') as dst:shutil.copyfileobj(src,dst)
            else:
                origin=(source/name).resolve();origin.relative_to(source.resolve())
                shutil.copyfile(origin,target)
            assert sha(target)==digest,name
        if marker=='manifest.json':
            target=ROOT/'manifest.json'
            if target.exists():assert target.read_bytes()==raw
            else:target.write_bytes(raw)
    finally:
        if z:z.close()


def find(marker, archive, expected=None):
    matches=[]
    for p in Path('/kaggle/input').rglob(marker):
        try:
            m=json.loads(p.read_text(encoding='utf-8'))
            if (sha(p)==expected if expected else m.get('input_manifest_sha256')==EXPECTED_INPUT_SHA256 and resume_has_progress(p.parent,m)):matches.append(p.parent)
        except (OSError,ValueError):pass
    archives=list(Path('/kaggle/input').rglob(archive))
    if marker=='resume-v79.json':
        archives+=list(Path('/kaggle/input').rglob('kotraj-v79-validation-resume.zip'))
    for p in archives:
        try:
            with zipfile.ZipFile(p) as z:raw=z.read(marker)
            m=json.loads(raw)
            if (hashlib.sha256(raw).hexdigest()==expected if expected else m.get('input_manifest_sha256')==EXPECTED_INPUT_SHA256 and resume_has_progress(p,m)):matches.append(p)
        except (OSError,ValueError,KeyError,zipfile.BadZipFile):pass
    if not matches:return None
    if marker=='manifest.json':return sorted(matches,key=lambda p:(p.is_file(),str(p)))[0]
    assert len(matches)==1,'Multiple resume results; attach only the latest v79 result'
    return matches[0]


def archive():
    OUT.mkdir(parents=True,exist_ok=True)
    files={p.relative_to(ROOT).as_posix():sha(p) for p in OUT.rglob('*') if p.is_file() and p.suffix!='.tmp'}
    tmp=RESULT.with_suffix('.zip.tmp')
    progress=any(p.stat().st_size for p in OUT.rglob('predictions.jsonl')) or any(
        json.loads(p.read_text(encoding='utf-8')).get('count',0)>0 for p in OUT.rglob('state.json'))
    artifact_type='run-output' if progress else 'setup-diagnostics'
    with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=3) as z:
        for name in files:z.write(ROOT/name,name)
        z.writestr('resume-v79.json',json.dumps({'input_manifest_sha256':EXPECTED_INPUT_SHA256,'files':files,
                                               'artifact_type':artifact_type,'test_read':False}))
    tmp.replace(RESULT)
    label='SAVE OUTPUT' if progress else 'DIAGNOSTIC ZIP ONLY (NO EVALUATION/TRAINING RESULT)'
    print(label+':',RESULT,'bytes:',RESULT.stat().st_size,flush=True)


def main():
    assert Path('/kaggle/working').is_dir()
    # A new session may have different GPU UUIDs. Do not create a conflicting
    # canonical runtime file before restoring hash-verified previous output.
    hardware=hardware_probe(OUT/('startup-'+str(int(START*1000)))/'hardware-probe.json')
    source=find('manifest.json','kotraj-v79-input.zip',EXPECTED_INPUT_SHA256)
    assert source,'Add Input: upload kotraj-v79-input.zip (includes saved8000 weights)'
    ROOT.mkdir(parents=True,exist_ok=True)
    install(source,'manifest.json',EXPECTED_INPUT_SHA256)
    if not (OUT/'identity.json').exists():
        prior=find('resume-v79.json','kotraj-v79-results.zip')
        if prior:install(prior,'resume-v79.json')
    (OUT/'hardware-probe.json').write_text(json.dumps(hardware,indent=2),encoding='utf-8')
    spec=importlib.util.spec_from_file_location('v76_environment',ROOT/'app/environment.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    env_root=Path('/tmp')/('kotraj-v79-env-'+EXPECTED_INPUT_SHA256[:8])
    python=helper.private_python(env_root)
    env=worker_environment(os.environ)
    pip_env=env.copy();pip_env.pop('PYTHONNOUSERSITE',None)
    pip=helper.managed_pip(python)
    if not (env_root/'wrapt-fix1.json').exists():
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','wrapt==2.0.1'],env=pip_env,check=True)
        (env_root/'wrapt-fix1.json').write_text('{"wrapt":"2.0.1"}')
    if not (env_root/'installed.json').exists():
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','torch==2.11.0',
                        '--index-url','https://download.pytorch.org/whl/cu128'],env=pip_env,check=True)
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off',
                        '-r',str(ROOT/'app/requirements.txt')],env=pip_env,check=True)
        (env_root/'installed.json').write_text(EXPECTED_INPUT_SHA256)
    OUT.mkdir(parents=True,exist_ok=True)
    packages=subprocess.check_output(helper.managed_pip(python)+['freeze'],env=pip_env,text=True)
    (OUT/'runtime-packages.txt').write_text(packages,encoding='utf-8')
    private_gpu_probe(python,env)
    remaining=SESSION_HOURS-(time.time()-START)/3600
    command=[str(python),'-u',str(ROOT/'app/experiment.py'),'--root',str(ROOT),'--out',str(OUT),'--hours',str(max(remaining,0.001))]
    if EVALUATE_ONLY:command.append('--evaluate-only')
    print('First: saved8000 val240. Then: control / ratio-only / short-output-only. Test is NOT included.',flush=True)
    with (OUT/'worker.stdout.log').open('a',encoding='utf-8') as log:
        process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                                 text=True,encoding='utf-8',errors='replace')
        for line in process.stdout:print(line,end='',flush=True);log.write(line);log.flush()
        assert process.wait()==0,'Worker failed; see saved error.json and worker.stdout.log'


if __name__=='__main__':
    try:main()
    except Exception as error:
        import traceback
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/'bootstrap-error.json').write_text(json.dumps({'error':str(error),'traceback':traceback.format_exc()}),encoding='utf-8')
        raise
    finally:archive()
