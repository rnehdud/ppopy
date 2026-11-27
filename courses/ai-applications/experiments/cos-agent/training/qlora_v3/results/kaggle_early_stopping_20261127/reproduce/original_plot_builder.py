import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent/'kaggle_raw_review_20261127'
s=json.loads((O/'semantic_summary.json').read_text(encoding='utf-8'));r=s['balanced_per_model']
h=json.loads((O/'kaggle_v2/qlora_early_stopping_lr1e4_20261127/epoch_history.json').read_text(encoding='utf-8'))
fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
x=range(5);labels=['Base','E1','E2','E3','E4']
axes[0].bar(x,[a['PASS'] for a in r],color=['#64748b','#7094b1','#168068','#7094b1','#7094b1'])
axes[0].set(xticks=list(x),xticklabels=labels,ylim=(0,26),ylabel='Direct-reading PASS / same 26 cases',title='Local replay only: 130 paired answers')
for i,a in enumerate(r):axes[0].text(i,a['PASS']+.5,str(a['PASS']),ha='center')
axes[1].plot([a['epoch'] for a in h],[a['val_token_loss'] for a in h],'o-',label='Validation CE')
axes[1].plot([a['epoch'] for a in h],[a['train_eval_token_loss'] for a in h],'o-',label='Train-eval CE')
axes[1].set(xticks=[1,2,3,4],xlabel='Saved epoch',ylabel='Assistant-token-weighted CE',title='Actual Kaggle v2 training log (90 val rows)')
axes[1].axvline(2,color='#168068',ls='--',alpha=.6);axes[1].legend()
fig.suptitle('Interim evidence: NOT the Kaggle T4 free-generation audit',fontsize=13)
fig.text(.5,-.03,'26 ordered cases: cleansing 20 + moisturizing 6; no HOLD or sun cases. E2 is provisional, not a final sweet spot.',ha='center',fontsize=9)
fig.savefig(O/'interim_local_review_and_loss.png',dpi=160,bbox_inches='tight')
print(O/'interim_local_review_and_loss.png')
