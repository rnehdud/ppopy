"""Rebuild an evidence plot only; never generate new model answers or verdicts."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 v1=read(HERE/'training_v1_5epoch/epoch_history.json');v2=read(HERE/'training_v2_early_stopping/epoch_history.json')
 rows=read(HERE/'local_replay/semantic_summary.json')['balanced_per_model']
 fig,ax=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
 ax[0].plot([r['epoch'] for r in v1],[r['train_eval_token_loss'] for r in v1],'o-',label='V1 train-eval CE')
 ax[0].plot([r['epoch'] for r in v1],[r['val_token_loss'] for r in v1],'o-',label='V1 val CE')
 ax[0].plot([r['epoch'] for r in v2],[r['val_token_loss'] for r in v2],'x--',label='V2 val CE')
 ax[0].set(xlabel='Epoch',ylabel='Token-weighted CE',title='Actual training logs; LR 1e-4 in both runs');ax[0].legend()
 ax[1].bar(['Base','E1','E2','E3','E4'],[r['PASS'] for r in rows],color='#3a817c')
 ax[1].set(ylabel='PASS / same 26 cases',ylim=(0,26),title='Local WSL raw reading only; NOT Kaggle T4 audit')
 for i,r in enumerate(rows):ax[1].text(i,r['PASS']+.4,str(r['PASS']),ha='center')
 args.output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(args.output,dpi=160)
 print(args.output)
if __name__=='__main__':main()
