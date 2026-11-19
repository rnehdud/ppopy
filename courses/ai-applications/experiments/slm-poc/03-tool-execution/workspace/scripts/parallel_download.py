"""Resumable SHA256-verified range transfer for large public artifacts."""
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request


def range_download(url,target,size,expected_sha,workers=6,chunk_size=8*1024*1024):
    target=Path(target)
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        with target.open('rb') as stream:
            actual=hashlib.file_digest(stream,'sha256').hexdigest()
        if actual==expected_sha:
            return
        raise ValueError('Existing target checksum mismatch; not overwriting')
    # Probe before starting any transfer. Never treat an ignored Range as a chunk.
    probe=urllib.request.Request(url,headers={'Range':'bytes=0-0','User-Agent':'stateful-agent-data/0.1'})
    with urllib.request.urlopen(probe,timeout=60) as response:
        if response.status!=206 or response.headers.get('Content-Range')!=f'bytes 0-0/{size}':
            raise ValueError(f'Server does not support exact byte ranges: {response.status}, {response.headers.get("Content-Range")}')
        response.read()
    parts=target.parent/(target.name+'.parts')
    parts.mkdir(exist_ok=True)
    prefix=target.with_suffix(target.suffix+'.partial')
    prefix_size=prefix.stat().st_size if prefix.exists() else 0
    spans=[(n,start,min(start+chunk_size,size)) for n,start in enumerate(range(0,size,chunk_size))]
    done_bytes=0
    def one(span):
        n,start,end=span
        part=parts/f'{n:05d}.part'
        if part.exists() and part.stat().st_size==end-start:
            return end-start
        if end<=prefix_size:
            with prefix.open('rb') as source:
                source.seek(start)
                data=source.read(end-start)
            part.write_bytes(data)
            return len(data)
        for attempt in range(5):
            try:
                # Distinct range URLs prevent a proxy from reusing a cached 0-0 probe.
                separator='&' if '?' in url else '?'
                ranged_url=url+separator+f'range_part={n}'
                req=urllib.request.Request(ranged_url,headers={'Range':f'bytes={start}-{end-1}',
                        'User-Agent':'stateful-agent-data/0.1'})
                with urllib.request.urlopen(req,timeout=120) as res:
                    if res.status!=206 or res.headers.get('Content-Range')!=f'bytes {start}-{end-1}/{size}':
                        raise ValueError('Unexpected range response')
                    data=res.read(end-start+1)
                if len(data)!=end-start:
                    raise ValueError('Incomplete byte range')
                part.write_bytes(data)
                return len(data)
            except Exception:
                if attempt==4:
                    raise
                time.sleep(1+attempt)
    start_time=last_report=time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures=[pool.submit(one,span) for span in spans]
        for future in as_completed(futures):
            done_bytes+=future.result()
            if time.monotonic()-last_report>15:
                elapsed=time.monotonic()-start_time
                print(f'{target.name}: {done_bytes/1024**2:.0f}/{size/1024**2:.0f} MiB, {done_bytes/1024**2/elapsed:.1f} MiB/s',flush=True)
                last_report=time.monotonic()
    assembled=target.with_suffix(target.suffix+'.assembled')
    with assembled.open('wb') as stream:
        for n,start,end in spans:
            stream.write((parts/f'{n:05d}.part').read_bytes())
    with assembled.open('rb') as stream:
        actual=hashlib.file_digest(stream,'sha256').hexdigest()
    if actual!=expected_sha:
        raise ValueError('Assembled SHA256 mismatch')
    assembled.replace(target)
    for n,start,end in spans:
        (parts/f'{n:05d}.part').unlink()
    parts.rmdir()
    if prefix.exists():
        prefix.unlink()
    print(f'Verified {target.name}',flush=True)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls=[]
    def handle_starttag(self,tag,attrs):
        if tag=='a':
            self.urls.extend(v for k,v in attrs if k=='href')


def torch_wheel():
    from packaging.version import Version
    url='https://download.pytorch.org/whl/cu128/torch/'
    with urllib.request.urlopen(url,timeout=60) as response:
        text=response.read().decode()
    parser=Links()
    parser.feed(text)
    choices=[]
    for link in parser.urls:
        filename=urllib.parse.unquote(urllib.parse.urlparse(link).path.rsplit('/',1)[-1])
        match=re.fullmatch(r'torch-(.+)-cp311-cp311-win_amd64.whl',filename)
        if match:
            version=Version(match[1])
            if not version.is_prerelease and version.base_version=='2.11.0':
                choices.append((version,urllib.parse.urljoin(url,link),filename))
    if not choices:
        raise ValueError('Pinned torch 2.11.0 CUDA 12.8 CPython 3.11 Windows wheel not found')
    version,link,filename=max(choices)
    base,fragment=urllib.parse.urldefrag(link)
    digest=urllib.parse.parse_qs(fragment)['sha256'][0]
    with urllib.request.urlopen(urllib.request.Request(base,method='HEAD'),timeout=60) as response:
        size=int(response.headers['Content-Length'])
    return {'url':base,'filename':filename,'version':str(version),'bytes':size,'sha256':digest}


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    metadata=torch_wheel()
    print(json.dumps(metadata,indent=2),flush=True)
    dest=root/'tmp/training_wheels'
    dest.mkdir(parents=True,exist_ok=True)
    (dest/'torch_wheel.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    range_download(metadata['url'],dest/metadata['filename'],metadata['bytes'],metadata['sha256'],workers=12)
