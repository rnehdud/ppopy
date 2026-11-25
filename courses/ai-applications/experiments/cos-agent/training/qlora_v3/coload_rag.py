"""Keep actual cached RAG models resident for a concurrent WSL vLLM benchmark."""
import argparse,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]))
from common import dump
def main():
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True);p.add_argument('--stop-file',required=True);a=p.parse_args()
    import torch
    from beauty_agent.rag.qwen import QwenEmbedder,QwenReranker
    marker=Path(a.stop_file);assert not marker.exists(),'stop marker already exists'
    torch.cuda.reset_peak_memory_stats()
    embed=QwenEmbedder(device='cuda',dtype='float16',batch_size=1,revision='97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3',local_files_only=True)
    rerank=QwenReranker(device='cuda',dtype='float16',batch_size=1,revision='e61197ed45024b0ed8a2d74b80b4d909f1255473',local_files_only=True)
    vector=embed.encode(['세안 뒤 보습 시점'],is_query=True)
    score=rerank.score('세안 뒤 보습 시점',['세정 뒤 보습 시점을 확인해요.'],[1.])
    receipt={'status':'resident_until_stop_marker','embedding_signature':embed.signature,'reranker_signature':rerank.signature,
             'embedding_dimension':len(vector[0]),'reranker_score':score,
             'allocated_mib':torch.cuda.memory_allocated()/2**20,'reserved_mib':torch.cuda.memory_reserved()/2**20,
             'peak_allocated_mib':torch.cuda.max_memory_allocated()/2**20,'actual_RAG_inference_executed':True}
    dump(a.receipt,receipt);print('RAG_MODELS_RESIDENT',json.dumps(receipt),flush=True)
    while not marker.exists():time.sleep(1)
if __name__=='__main__':main()
