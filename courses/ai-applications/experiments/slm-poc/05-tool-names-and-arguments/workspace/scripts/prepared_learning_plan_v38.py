"""Freeze one next-action learning run on the fully checked360 rows."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.complete_teacher_data_v37r1 import DATA as TEACH,OUT as D37,read,save,digest,verify as teacher_verify
from scripts.next_action_data_v36 import INITIAL,MODEL
OUT=ROOT/'output/diagnostics/prepared-next-action-v38';SEED=380030


def prepare():
    teacher_verify();a=read(D37/'audit.json');revision=read(D37/'revision-audit.json')
    if not a['all_passed'] or not revision['all_passed'] or len(read(TEACH/'train.json'))!=360:raise ValueError('Teacher gate is closed')
    if OUT.exists():raise FileExistsError('V38 protected')
    sources=['demo/prepared_feedback_v38.py','scripts/prepared_learning_plan_v38.py','scripts/prepared_learning_v38.py','scripts/report_prepared_learning_v38.py','tests/test_prepared_feedback_v38.py']
    files=[ROOT/p for p in sources]+[TEACH/p for p in ['protocol.json','build-manifest.json','cases.json','train.json','heldout.json']]+[D37/'audit.json',INITIAL/'adapter_model.safetensors',INITIAL/'adapter_config.json']
    OUT.mkdir(parents=True)
    save(OUT/'plan.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'epochs':6,'lr':1e-4,'effective_batch':4,'rows':360,'updates':540,
      'initial_adapter':str(INITIAL.relative_to(ROOT)),'initial_adapter_sha256':digest(INITIAL/'adapter_model.safetensors'),
      'training':'One final QLoRA adapter from the SAME pre-V36 cosmetics weights, not failed V36 weights. NF4FP16, frozen base, only query/value LoRA, standard categorical CE over candidate scores. All360 rows,6 epochs, no sample dropping, no symptom training, no test checkpoint/prompt/cutoff selection.',
      'runtime':'Unchanged FeedbackSkinSession control flow and actual registered handlers. Shared reversible V37r1 renderer used for training AND every action inference. No scripted action substitution or automatic goal completion. Program duplicate/condition/budget stops are failures for completed tasks.',
      'evaluation':'After final weights fixed, same30 heldout conversations x before/after x gold/parser =120 autonomous episodes. Gold condition supplies authored correct observations; parser condition uses frozen original symptom weights. Parser-mode session cannot access gold observations, expected patches or plans. Also60 fixed gold-prefix judgments before/after, separate from free episodes.',
      'primary':'Gold-condition two-operation order+state+normal-model-stop count must improve. Gold and parser required correct writes cannot decrease, unwanted writes cannot increase. Report all families and both modes. No automatic deployment regardless.',
      'scope':'Small assistant-authored same two tools/five symptoms/empty arguments, heldout phrasings only. Not independent human gold, unknown-tool/domain90, Qwen/STT or actual live user evaluation.',
      'stop':'One fixed run and evaluation. No retries with different prompts/epochs on these30 conversations. Keep live chat, original weights and frozen data unchanged.'})
    print('V38 FROZEN:360 rows,540 updates;120 episodes +120 fixed-prefix judgments',flush=True)


def verify():
    teacher_verify();p=read(OUT/'plan.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V38 changed: '+rel)
    return p
if __name__=='__main__':prepare()
