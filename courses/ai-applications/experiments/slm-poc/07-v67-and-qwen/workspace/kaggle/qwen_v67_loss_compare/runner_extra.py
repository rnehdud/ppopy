"""Appended to the verified launcher's shared restore utilities by the builder."""
import queue
import tempfile
import threading

OBJECTIVES=['pointwise','relative']

def assemble_comparison(snapshots):
    summary={'status':'partial','primary_metric':'Fixed epoch3 exact (action,target_id) on val221',
             'test_used':False,'previous170_is_not_control':True,'runs':{}}
    loaded={}
    for name,path in snapshots.items():
        if name not in OBJECTIVES:continue
        with zipfile.ZipFile(path) as z:
            names=set(z.namelist())
            get=lambda n:json.loads(z.read(n))
            run={'status':get('status.json') if 'status.json' in names else {'status':'running'}}
            for phase in ['baseline','epoch-01','epoch-02','epoch-03']:
                filename=phase+'/summary.json'
                if filename in names:run[phase]=get(filename)
            if 'best.json' in names:run['best']=get('best.json')
            if 'error.json' in names:run['error']=get('error.json')
            summary['runs'][name]=run
            if run['status']['status']=='completed':
                loaded[name]={'identity':get('identity.json'),'init':get('initial-adapter.json'),
                    'baseline':{get(n)['id']:get(n)['selected'] for n in names if n.startswith('baseline/cases/') and n.endswith('.json')},
                    'final':{get(n)['id']:get(n) for n in names if n.startswith('epoch-03/cases/') and n.endswith('.json')}}
    if set(loaded)!=set(OBJECTIVES):return summary
    control=loaded['pointwise'];relative=loaded['relative']
    ca={k:v for k,v in control['identity'].items() if k!='objective'}
    ra={k:v for k,v in relative['identity'].items() if k!='objective'}
    comparable={'data_config_plan_and_worker_equal':ca==ra,
                'initial_adapter_equal':control['init']==relative['init'],
                'baseline_all221_choices_equal':control['baseline']==relative['baseline'] and len(control['baseline'])==221,
                'final_ids_equal':set(control['final'])==set(relative['final']) and len(control['final'])==221}
    summary['comparability']=comparable
    summary['status']='completed' if all(comparable.values()) else 'completed_needs_comparability_review'
    one=summary['runs']['pointwise']['epoch-03'];two=summary['runs']['relative']['epoch-03']
    summary['fixed_epoch3_comparison']={'pointwise_correct':one['correct'],'relative_correct':two['correct'],'n':221,
        'relative_minus_pointwise':two['correct']-one['correct'],
        'pointwise_wrong_relative_correct':sum(not control['final'][i]['pair_correct'] and relative['final'][i]['pair_correct'] for i in control['final']),
        'pointwise_correct_relative_wrong':sum(control['final'][i]['pair_correct'] and not relative['final'][i]['pair_correct'] for i in control['final']),
        'pointwise_retrieve_correct':one['by_gold_action']['retrieve_evidence']['correct'],
        'relative_retrieve_correct':two['by_gold_action']['retrieve_evidence']['correct'],'retrieve_n':22,
        'pointwise_val_over90':one['val_exceeds_90_percent'],'relative_val_over90':two['val_exceeds_90_percent']}
    summary['claim_scope']='One matched-seed internal-val loss comparison, not a final-test result, generalization guarantee or proof that all errors are caused by loss.'
    return summary

def archive():
    OUT.mkdir(parents=True,exist_ok=True)
    # Workers atomically replace their own ZIPs. Copy each through an open file
    # handle into a stable staging area before hashing/archiving its contents.
    with tempfile.TemporaryDirectory(prefix='v67-loss-snapshot-') as temporary:
        staging=Path(temporary);snapshots={}
        for name in OBJECTIVES:
            source=OUT/(name+'-results.zip')
            if source.exists():
                target=staging/source.name
                with source.open('rb') as src,target.open('wb') as dst:shutil.copyfileobj(src,dst)
                snapshots[name]=target
        comparison=assemble_comparison(snapshots)
        save(OUT/'comparison.json',comparison)
        files={name+'-results.zip':p for name,p in snapshots.items()}
        for path in OUT.glob('*.json'):
            if path.name=='qwen-v67-loss-compare-resume.json':continue
            staged=staging/path.name;shutil.copyfile(path,staged);files[path.name]=staged
        packages=OUT/'runtime-packages.txt'
        if packages.exists():
            staged=staging/packages.name;shutil.copyfile(packages,staged);files[packages.name]=staged
        marker={'bundle_sha256':EXPECTED_MANIFEST_SHA256,'files':{n:sha(p) for n,p in files.items()},
            'artifact_type':'loss-comparison-output' if snapshots else 'setup-diagnostics','test_used':False}
        tmp=RESULT.with_suffix('.zip.tmp')
        # Nested result ZIPs are already compressed; avoid recompressing them.
        with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_STORED) as z:
            for name,path in files.items():z.write(path,name)
            z.writestr('qwen-v67-loss-compare-resume.json',json.dumps(marker,indent=2))
        tmp.replace(RESULT)
    print('SAVE COMPARISON OUTPUT:',RESULT,'bytes:',RESULT.stat().st_size,'status:',comparison['status'],flush=True)
    print('Save the notebook version OUTPUT before ending the session.',flush=True)

def main():
    started=time.time();assert Path('/kaggle/working').is_dir(),'Run this notebook in Kaggle'
    assert 0<SESSION_HOURS<=10
    ROOT.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    hardware=subprocess.run(['nvidia-smi','-L'],capture_output=True,text=True,timeout=20)
    save(OUT/('startup-hardware-'+str(int(started*1000))+'.json'),{'stdout':hardware.stdout,'stderr':hardware.stderr,'returncode':hardware.returncode})
    if hardware.returncode or 'GPU ' not in hardware.stdout:raise RuntimeError('No GPU assigned. Select Accelerator: GPU T4 x2 and restart.')
    source=find('bundle_manifest.json','qwen-v67-loss-compare-input.zip',EXPECTED_MANIFEST_SHA256)
    if not source:raise FileNotFoundError('Upload qwen-v67-loss-compare-input.zip as a Kaggle Dataset and Add Input.')
    restore(source,'bundle_manifest.json',ROOT,EXPECTED_MANIFEST_SHA256)
    if not any((OUT/name/'identity.json').exists() for name in OBJECTIVES):
        prior=find('qwen-v67-loss-compare-resume.json','qwen-v67-loss-compare-results.zip',EXPECTED_MANIFEST_SHA256,resume=True)
        if prior:
            restore(prior,'qwen-v67-loss-compare-resume.json',OUT,EXPECTED_MANIFEST_SHA256)
            for name in OBJECTIVES:
                nested=OUT/(name+'-results.zip')
                if nested.exists():restore(nested,'qwen-v67-resume.json',OUT/name,EXPECTED_MANIFEST_SHA256)
            print('RESTORED previous paired experiment:',prior,flush=True)
    env_root=Path('/tmp')/('qwen-v67-loss-env-'+EXPECTED_MANIFEST_SHA256[:12])
    python=env_root/'bin/python'
    if not python.exists():venv.EnvBuilder(with_pip=False,system_site_packages=False).create(env_root)
    assert 'include-system-site-packages = false' in (env_root/'pyvenv.cfg').read_text().lower()
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    env.update(PYTHONNOUSERSITE='1',PYTHONUNBUFFERED='1',TOKENIZERS_PARALLELISM='false',USE_TF='0',USE_FLAX='0',
               HF_HUB_CACHE='/tmp/qwen-v67-hf-cache',PIP_CACHE_DIR='/tmp/qwen-v67-pip-cache',HF_HUB_DISABLE_XET='1')
    pip_env=env.copy();pip_env.pop('PYTHONNOUSERSITE',None)
    pip=[sys.executable,'-m','pip','--python',str(python)]
    if not (env_root/'installed.json').exists():
        print('Installing separate CUDA environment. Notebook packages are unchanged.',flush=True)
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','wrapt==2.0.1'],env=pip_env,check=True)
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','torch==2.11.0','--index-url','https://download.pytorch.org/whl/cu128'],env=pip_env,check=True)
        subprocess.run(pip+['install','--disable-pip-version-check','--progress-bar','off','-r',str(ROOT/'app/requirements.txt')],env=pip_env,check=True)
        subprocess.run(pip+['check'],env=pip_env,check=True);save(env_root/'installed.json',{'manifest':EXPECTED_MANIFEST_SHA256})
    probe_code='import json,torch; assert torch.cuda.is_available(),"CUDA unavailable in private environment"; n=torch.cuda.device_count(); r={"torch":torch.__version__,"cuda":torch.version.cuda,"device_count":n,"devices":[torch.cuda.get_device_name(i) for i in range(n)]}; print("GPU_REPORT="+json.dumps(r)); [torch.ones(1,device="cuda:"+str(i)) for i in range(n)]'
    probe=subprocess.run([str(python),'-I','-c',probe_code],env=env,capture_output=True,text=True,timeout=90)
    save(OUT/'private-gpu-probe.json',{'stdout':probe.stdout,'stderr':probe.stderr,'returncode':probe.returncode})
    if probe.returncode:raise RuntimeError('CUDA probe failed: '+probe.stdout+probe.stderr)
    report=json.loads(next(s.split('=',1)[1] for s in probe.stdout.splitlines() if s.startswith('GPU_REPORT=')))
    print(report,flush=True)
    (OUT/'runtime-packages.txt').write_text(subprocess.check_output(pip+['freeze'],env=pip_env,text=True),encoding='utf8')
    deadline=started+SESSION_HOURS*3600-240
    if time.time()>=deadline:raise RuntimeError('Setup exhausted session budget; no training started.')
    capacity=min(report['device_count'],2)
    pending=[name for name in OBJECTIVES if not ((OUT/name/'status.json').exists() and json.loads((OUT/name/'status.json').read_text())['status']=='completed')]
    save(OUT/'runner-status.json',{'status':'running','parallel_workers':capacity,'pending':pending,'test_used':False})
    events=queue.Queue();active={};failed=[]
    runpy_code='import runpy,sys;sys.path.insert(0,sys.argv[1]);sys.argv=sys.argv[2:];runpy.run_path(sys.argv[0],run_name="__main__")'
    def launch(name,gpu):
        folder=OUT/name;folder.mkdir(exist_ok=True)
        command=[str(python),'-I','-u','-c',runpy_code,str(ROOT/'app'),str(ROOT/'app/train.py'),
                 '--root',str(ROOT),'--out',str(folder),'--deadline',str(deadline),'--objective',name,'--gpu',str(gpu)]
        process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace')
        active[name]=(process,gpu)
        def reader():
            with (folder/'worker.stdout.log').open('a',encoding='utf8') as log:
                for line in process.stdout:
                    log.write(line);log.flush();events.put((name,'line',line))
            events.put((name,'exit',process.wait()))
        threading.Thread(target=reader,daemon=True).start()
        print('START',name,'GPU',gpu,flush=True)
    for gpu in range(capacity):
        if pending:launch(pending.pop(0),gpu)
    while active:
        try:name,kind,value=events.get(timeout=1)
        except queue.Empty:continue
        if kind=='line':
            print('['+name+'] '+value,end='',flush=True)
            if value.startswith('SAVE OUTPUT:'):archive()
        else:
            _,gpu=active.pop(name)
            if value:failed.append({'objective':name,'returncode':value})
            archive()
            if pending and time.time()<deadline:launch(pending.pop(0),gpu)
    incomplete=[name for name in OBJECTIVES if not ((OUT/name/'status.json').exists() and json.loads((OUT/name/'status.json').read_text())['status']=='completed')]
    save(OUT/'runner-status.json',{'status':'failed' if failed else 'partial_time_budget' if incomplete else 'completed',
        'failed':failed,'incomplete':incomplete,'parallel_workers':capacity,'test_used':False})
    if failed:raise RuntimeError('A condition failed; inspect its nested result ZIP error.json. Other saved results are preserved.')
    if incomplete:print('PARTIAL: save output, attach it with the original input, and rerun to resume.',flush=True)

if __name__=='__main__':
    try:main()
    except Exception as error:
        save(OUT/'launcher-error.json',{'type':type(error).__name__,'message':str(error),'traceback':traceback.format_exc(),'completed':False})
        raise
    finally:archive()
