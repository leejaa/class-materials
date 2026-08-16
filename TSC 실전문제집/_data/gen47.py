#!/usr/bin/env python3
"""제6·7부분 이미지 생성 (Vercel AI Gateway + gpt-image-2).
사용법: AI_GW_KEY=... python3 gen47.py 제6부분 실전1회
       AI_GW_KEY=... python3 gen47.py 제7부분         (제7 스토리 전체)
tsc47_data.json 의 prompt 필드에서 읽어 ../생성이미지/ 에 저장(재활용).
"""
import os, sys, json, base64, urllib.request, time
HERE=os.path.dirname(os.path.abspath(__file__)); BASE=os.path.dirname(HERE)
DATA=os.path.join(HERE,"tsc47_data.json"); IMGDIR=os.path.join(BASE,"생성이미지")
URL="https://ai-gateway.vercel.sh/v1/images/generations"

def gen_one(prompt,out,key,size="1024x1024"):
    body=json.dumps({"model":"openai/gpt-image-2","prompt":prompt,"size":size,"n":1}).encode()
    req=urllib.request.Request(URL,data=body,headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=240) as r: data=json.load(r)
    open(out,"wb").write(base64.b64decode(data["data"][0]["b64_json"]))
    return os.path.getsize(out)

def main():
    key=os.environ.get("AI_GW_KEY")
    if not key: sys.exit("AI_GW_KEY required")
    part=sys.argv[1]; rnd=sys.argv[2] if len(sys.argv)>2 else None
    d=json.load(open(DATA,encoding="utf-8"))
    items=[]
    if part=="제7부분":
        for r,it in d["제7부분"].items(): items.append(it)
    else:
        block=d[part]
        rounds=[rnd] if rnd else list(block.keys())
        for r in rounds:
            for it in block[r]: items.append(it)
    os.makedirs(IMGDIR,exist_ok=True)
    size="1536x1024" if part=="제7부분" else "1024x1024"
    for it in items:
        out=os.path.join(IMGDIR,it["image"])
        for a in range(3):
            try:
                sz=gen_one(it["prompt"],out,key,size); print(f"[OK] {it['image']} ({sz//1024}KB)"); break
            except Exception as e:
                print(f"[retry {a+1}] {it['image']}: {e}"); time.sleep(3)
        else: print(f"[FAIL] {it['image']}")

if __name__=="__main__": main()
