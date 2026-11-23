# Kaggle only. Import the generated notebook and Run All.
EXPECTED_MANIFEST_SHA256 = '__MANIFEST_SHA256__'
SESSION_HOURS = 9.0

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
import venv
import zipfile

ROOT=Path('/kaggle/working/qwen_v67_reranker')
OUT=ROOT/'results'
RESULT=Path('/kaggle/working/qwen-v67-kaggle-results.zip')

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')

def restore(source,marker,destination,expected):
    source=Path(source);z=zipfile.ZipFile(source) if source.is_file() else None
    try:
        raw=z.read(marker) if z else (source/marker).read_bytes()
        m=json.loads(raw)
        if marker=='bundle_manifest.json':assert hashlib.sha256(raw).hexdigest()==expected
        else:assert m['bundle_sha256']==expected
        for name,digest in m['files'].items():
            target=(destination/name).resolve();target.relative_to(destination.resolve())
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():assert sha(target)==digest,'Existing file changed: '+name;continue
            if z:
                with z.open(name) as src,target.open('xb') as dst:shutil.copyfileobj(src,dst)
            else:
                origin=(source/name).resolve();origin.relative_to(source.resolve());shutil.copyfile(origin,target)
            assert sha(target)==digest,'Copied file mismatch: '+name
        if marker=='bundle_manifest.json':(destination/marker).write_bytes(raw)
    finally:
        if z:z.close()

def find(marker,archive_name,expected,resume=False):
    matches=[]
    for path in Path('/kaggle/input').rglob(marker):
        try:
            raw=path.read_bytes();m=json.loads(raw)
            ok=m.get('bundle_sha256')==expected if resume else hashlib.sha256(raw).hexdigest()==expected
            if ok:matches.append(path.parent)
        except (OSError,ValueError):pass
    for path in Path('/kaggle/input').rglob(archive_name):
        try:
            with zipfile.ZipFile(path) as z:raw=z.read(marker)
            m=json.loads(raw);ok=m.get('bundle_sha256')==expected if resume else hashlib.sha256(raw).hexdigest()==expected
            if ok:matches.append(path)
        except (OSError,ValueError,KeyError,zipfile.BadZipFile):pass
    if not matches:return None
    # The same input may be attached as a ZIP and expanded; prefer expanded.
    if not resume:return sorted(matches,key=lambda p:(p.is_file(),str(p)))[0]
    if len(matches)!=1:raise RuntimeError('Attach only one previous qwen-v67 result for resume: '+str(matches))
    return matches[0]

def archive():
    OUT.mkdir(parents=True,exist_ok=True)
    files={p.relative_to(OUT).as_posix():sha(p) for p in OUT.rglob('*') if p.is_file() and not p.name.endswith('.tmp')}
    marker={'bundle_sha256':EXPECTED_MANIFEST_SHA256,'files':files,
            'artifact_type':'training-or-evaluation-output' if (OUT/'baseline/summary.json').exists() else 'setup-diagnostics','test_used':False}
    tmp=RESULT.with_suffix('.zip.tmp')
    with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,compresslevel=1) as z:
        for n in files:z.write(OUT/n,n)
        z.writestr('qwen-v67-resume.json',json.dumps(marker,indent=2))
    tmp.replace(RESULT)
    print(('RESULT ZIP' if marker['artifact_type']!='setup-diagnostics' else 'DIAGNOSTIC ZIP: NOT A TRAINING RESULT'),RESULT,'bytes:',RESULT.stat().st_size,flush=True)
    print('Save the notebook version OUTPUT before ending this Kaggle session.',flush=True)

def main():
    started=time.time();assert Path('/kaggle/working').is_dir(),'Use this launcher in Kaggle'
    assert 0<SESSION_HOURS<=10
    ROOT.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    try:
        hardware=subprocess.run(['nvidia-smi','-L'],capture_output=True,text=True,timeout=20)
    except OSError as error:raise RuntimeError('No NVIDIA GPU. Set Accelerator: GPU T4 x2 and restart.') from error
    hardware_report={'returncode':hardware.returncode,'stdout':hardware.stdout,'stderr':hardware.stderr}
    save(OUT/('startup-hardware-'+str(int(started*1000))+'.json'),hardware_report)
    if hardware.returncode!=0 or 'GPU ' not in hardware.stdout:raise RuntimeError('No GPU assigned. Select GPU T4 x2 and restart; notebook metadata alone is not sufficient.')
    print(hardware.stdout,flush=True)
    source=find('bundle_manifest.json','qwen-v67-kaggle-input.zip',EXPECTED_MANIFEST_SHA256)
    if not source:raise FileNotFoundError('Add Input: upload qwen-v67-kaggle-input.zip as a Kaggle Dataset, attach it, and rerun.')
    restore(source,'bundle_manifest.json',ROOT,EXPECTED_MANIFEST_SHA256)
    if not (OUT/'identity.json').exists():
        prior=find('qwen-v67-resume.json','qwen-v67-kaggle-results.zip',EXPECTED_MANIFEST_SHA256,resume=True)
        if prior:restore(prior,'qwen-v67-resume.json',OUT,EXPECTED_MANIFEST_SHA256);print('RESTORED',prior,flush=True)
    save(OUT/'hardware-probe.json',hardware_report)
    env_root=Path('/tmp')/('qwen-v67-env-'+EXPECTED_MANIFEST_SHA256[:12])
    python=env_root/'bin/python'
    if not python.exists():
        print('Creating isolated environment WITHOUT ensurepip. Notebook packages will not change.',flush=True)
        venv.EnvBuilder(with_pip=False,system_site_packages=False).create(env_root)
    assert 'include-system-site-packages = false' in (env_root/'pyvenv.cfg').read_text().lower()
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    env.update(PYTHONNOUSERSITE='1',PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false',
               USE_TF='0',USE_FLAX='0',HF_HUB_CACHE='/tmp/qwen-v67-hf-cache',PIP_CACHE_DIR='/tmp/qwen-v67-pip-cache',HF_HUB_DISABLE_XET='1')
    # Do not replace the CUDA visibility mapping supplied by Kaggle.
    pip_env=env.copy();pip_env.pop('PYTHONNOUSERSITE',None)
    pip=[sys.executable,'-m','pip','--python',str(python)]
    if not (env_root/'installed.json').exists():
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','wrapt==2.0.1'],env=pip_env,check=True)
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off',
            'torch==2.11.0','--index-url','https://download.pytorch.org/whl/cu128'],env=pip_env,check=True)
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','-r',str(ROOT/'app/requirements.txt')],env=pip_env,check=True)
        subprocess.run(pip+['check'],env=pip_env,check=True)
        save(env_root/'installed.json',{'input_manifest':EXPECTED_MANIFEST_SHA256})
    report_code='import json,torch; r={"torch":torch.__version__,"build_cuda":torch.version.cuda,"available":torch.cuda.is_available()}; print(json.dumps(r),flush=True); assert r["available"],"Private PyTorch cannot use CUDA"; print(torch.cuda.get_device_name(0)); torch.ones(1,device="cuda")'
    probe=subprocess.run([str(python),'-I','-c',report_code],env=env,capture_output=True,text=True,timeout=90)
    save(OUT/'private-gpu-probe.json',{'returncode':probe.returncode,'stdout':probe.stdout,'stderr':probe.stderr})
    if probe.returncode:raise RuntimeError('Private CUDA check failed; see private-gpu-probe.json: '+probe.stdout+probe.stderr)
    print(probe.stdout,flush=True)
    packages=subprocess.check_output(pip+['freeze'],env=pip_env,text=True)
    (OUT/'runtime-packages.txt').write_text(packages,encoding='utf8')
    deadline=started+SESSION_HOURS*3600-180
    if time.time()>=deadline:raise RuntimeError('Setup exhausted session budget; rerun with saved input/cache before training.')
    # -I removes app from sys.path. Execute through runpy with only this trusted
    # app directory inserted, while excluding user-site and PYTHONPATH hooks.
    code='import runpy,sys;sys.path.insert(0,sys.argv[1]);sys.argv=sys.argv[2:];runpy.run_path(sys.argv[0],run_name="__main__")'
    command=[str(python),'-I','-u','-c',code,str(ROOT/'app'),str(ROOT/'app/train.py'),'--root',str(ROOT),'--out',str(OUT),'--deadline',str(deadline)]
    print('QLoRA: train1980 only. Baseline and epochs1-3: full val221. Test NOT included. One T4 is used.',flush=True)
    with (OUT/'worker.stdout.log').open('a',encoding='utf8') as log:
        process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
        for line in process.stdout:print(line,end='',flush=True);log.write(line);log.flush()
        if process.wait()!=0:raise RuntimeError('Training worker failed. Inspect error.json / worker.stdout.log; ZIP may contain diagnostics, not a completed model.')

if __name__=='__main__':
    try:main()
    except Exception as error:
        save(OUT/'launcher-error.json',{'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc(),'completed':False})
        raise
    finally:archive()
