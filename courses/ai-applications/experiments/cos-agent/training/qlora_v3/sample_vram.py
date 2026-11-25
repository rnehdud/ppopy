"""Physical device occupancy sampler; includes desktop/other processes, not just torch."""
import argparse,csv,datetime,subprocess,time
from pathlib import Path
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--stop-file',required=True)
    p.add_argument('--interval',type=float,default=2.);a=p.parse_args()
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);stop=Path(a.stop_file)
    assert not stop.exists() and not out.exists(),'choose a new measurement path'
    with out.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['time_utc','memory_used_mib','memory_total_mib','gpu_util_percent','temperature_c','power_w'])
        while not stop.exists():
            result=subprocess.run(['nvidia-smi','--query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu,power.draw','--format=csv,noheader,nounits'],capture_output=True,text=True,check=True)
            values=next(csv.reader(result.stdout.splitlines()))
            writer.writerow([datetime.datetime.now(datetime.timezone.utc).isoformat(),*[v.strip() for v in values]]);f.flush()
            time.sleep(a.interval)
if __name__=='__main__':main()
