"""합성 파일럿을 텍스트 보존형 메신저 PNG로 표시해요. 데이터 수정·검수 승인은 하지 않아요."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile

from PIL import Image, ImageDraw, ImageFont

COS = Path(__file__).resolve().parents[1]
FONT = Path("C:/Windows/Fonts/NotoSansKR-Regular.ttf")
BOLD = Path("C:/Windows/Fonts/NotoSansKR-Bold.ttf")
W = 1080
BG = "#B5C8D6"
INK = "#202936"

def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def wrapped(text, face, width):
    """실제 글리프 폭으로 줄바꿈해요. 원문의 문장·인용 ID는 삭제하지 않아요."""
    result = []
    for paragraph in text.split("\n"):
        if not paragraph:
            result.append("")
            continue
        line = ""
        for token in re.findall(r"\[[^\]]+\]|\s+|[^\s\[]+", paragraph):
            if token.isspace() and not line:
                continue
            if line and face.getlength(line + token) > width:
                result.append(line.rstrip())
                line = ""
                if token.isspace():
                    continue
            if face.getlength(token) > width:
                for char in token:
                    if line and face.getlength(line + char) > width:
                        result.append(line)
                        line = ""
                    line += char
            else:
                line += token
        result.append(line)
    return result

def draw_case(case, response, number, target, revision=1):
    canvas = Image.new("RGB", (W, 6500), BG)
    d = ImageDraw.Draw(canvas)
    d.rectangle((0, 0, W, 172), fill="#EDF3F6")
    d.rounded_rectangle((42, 43, 116, 117), radius=23, fill="#344B61")
    d.text((63, 52), "P", font=font(43, True), fill="white")
    d.text((140, 35), "Ppopy · 파일럿 대화", font=font(35, True), fill=INK)
    d.text((141, 91), f"R{revision} · {number:02d} / 24   ·   {case['id']}", font=font(25), fill="#536577")
    y = 196
    for line in wrapped(case["title"], font(34, True), W-100):
        d.text((50, y), line, font=font(34, True), fill=INK)
        y += 50
    bucket = {"normal_guidance":"일반 안내", "unknown_or_version":"미상·버전 확인",
              "distractor_or_defense":"방해 문헌·해석 방어", "hold":"개별 권고 보류"}[case["pilot_bucket"]]
    d.text((50,y+6), f"{bucket}   ·   합성 예시   ·   Critic / 사람 미검수", font=font(24), fill="#3C5366")
    y += 70

    def bubble(text, right=False, heading=None):
        nonlocal y
        x = 186 if right else 98
        bw = 844 if right else 900
        face = font(31)
        lines = wrapped(text, face, bw-64)
        bh = 50 + len(lines)*49 + (58 if heading else 0)
        color = "#FEE500" if right else "#FFFFFF"
        d.rounded_rectangle((x,y+4,x+bw,y+bh+4),radius=25, fill="#A2B5C2")
        d.rounded_rectangle((x,y,x+bw,y+bh),radius=25,fill=color)
        if right:
            d.polygon([(x+bw-12,y+18),(x+bw+15,y+11),(x+bw-8,y+44)],fill=color)
        else:
            d.polygon([(x+12,y+18),(x-17,y+11),(x+8,y+44)],fill=color)
        ty=y+22
        if heading:
            d.text((x+32,ty),heading,font=font(29,True),fill="#355772")
            ty += 58
        for line in lines:
            d.text((x+32,ty),line,font=face,fill=INK)
            ty += 49
        y += bh+22

    d.text((W-265,y), "사용자 · 합성 발화",font=font(25,True),fill="#34495B")
    y += 44
    bubble(case["scenario_raw"],True)
    y += 18
    d.rounded_rectangle((30,y,80,y+50),radius=15,fill="#344B61")
    d.text((45,y+3),"P",font=font(27,True),fill="white")
    d.text((98,y+3),"Ppopy · 생성된 응답 원문",font=font(26,True),fill="#34495B")
    y += 64
    for section in response.split("### "):
        if not section.strip():
            continue
        heading, _, body=section.partition("\n")
        bubble(body.strip(),heading=heading.strip())
    y += 9
    footer = "실제 카카오톡 기록이 아닌 합성 데이터 시각화예요.\n별도 사용자 확인과 제품 근거는 HTML의 각 이미지 아래에 있어요.\n모델 입력은 정형 JSON이에요. 구조 통과 ≠ 내용 검수 승인"
    for line in wrapped(footer,font(22),W-100):
        d.text((50,y),line,font=font(22),fill="#3D5365")
        y += 38
    y += 35
    assert y < canvas.height, (case["id"],y)
    canvas.crop((0,0,W,y)).save(target,optimize=True)
    return y

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=COS/"outputs/qlora_v3_pilot_20261125/chat_images")
    args=parser.parse_args()
    out=args.output.resolve()
    if out.exists():
        raise SystemExit(f"기존 산출물을 덮어쓰지 않아요: {out}")
    data=COS/"data/qlora/v2"
    paths=[data/"pilot_24_inputs.json",data/"pilot_24_responses.json",data/"pilot_24.jsonl"]
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    inputs=json.loads(paths[0].read_text(encoding="utf-8"))
    rows=[json.loads(line) for line in paths[2].read_text(encoding="utf-8").splitlines()]
    responses={r["id"]:r["messages"][2]["content"] for r in rows}
    assert len(rows)==len(inputs["cases"])==24
    out.mkdir(parents=True)
    images=[]
    for number,case in enumerate(inputs["cases"],1):
        name=f"{number:02d}_{case['id']}.png"
        height=draw_case(case,responses[case["id"]],number,out/name,revision=inputs.get('plan_revision',1))
        images.append({"id":case["id"],"title":case["title"],"file":name,"width":W,"height":height})
    cards="\n".join(f'<article><h2>{i+1:02d} · {html.escape(c["title"])}</h2><a href="{c["file"]}" target="_blank"><img loading="lazy" src="{c["file"]}" alt="{html.escape(c["title"])}"></a><p>{c["id"]} · 클릭하면 원본 크기로 열려요</p></article>' for i,c in enumerate(images))
    gallery='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ppopy 파일럿 24개 대화</title><style>body{margin:0;background:#f1f5f9;color:#243448;font-family:system-ui,sans-serif}header{max-width:1450px;margin:auto;padding:36px 24px}h1{font-size:30px}header p{line-height:1.8}main{max-width:1500px;margin:auto;padding:0 20px 40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,400px),1fr));gap:24px}article{background:white;border-radius:20px;padding:18px;box-shadow:0 3px 15px #172a4310}h2{font-size:19px;min-height:46px;line-height:1.5}img{width:100%;height:auto;display:block;border-radius:12px}article p{font-size:13px;color:#64748b}a{color:#255f95}</style><header><h1>Ppopy · 합성 파일럿 24개 대화</h1><p>카카오톡형 말풍선으로 읽는 합성 상황과 생성 응답 원문이에요.<br>실제 메신저 기록이 아니며, 모든 사례는 Critic·사람 검수 전이에요. 데이터 내용은 수정하지 않았어요.</p></header><main>'''+cards+'</main></html>'
    from add_pilot_gallery_raw import make_gallery
    gallery = make_gallery(inputs, rows, images)
    (out/"index.html").write_bytes(gallery.encode("utf-8"))
    assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    manifest={"source_sha256":before,"rendering":"원문 보존형 결정적 렌더링. ###는 시각적 제목으로 표시하고 줄바꿈만 조정해요.","human_review":"unreviewed","critic_status":"unreviewed","images":images}
    (out/"manifest.json").write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    archive=out.parent/(out.name+".zip")
    if archive.exists():
        raise SystemExit(f"기존 ZIP을 덮어쓰지 않아요: {archive}")
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.iterdir()):
            z.write(p,arcname="chat_images/"+p.name)
    print(json.dumps({"image_count":len(images),"source_unchanged":True,"output":str(out),"zip":str(archive),"heights":[min(i['height'] for i in images),max(i['height'] for i in images)]},ensure_ascii=False))

if __name__=="__main__":
    main()
