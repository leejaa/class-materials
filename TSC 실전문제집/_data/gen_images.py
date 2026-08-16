#!/usr/bin/env python3
"""TSC 문제 그림 생성기 (Vercel AI Gateway + gpt-image-2).
사용법:
  AI_GW_KEY=... python3 gen_images.py 실전1회            # 라운드 전체
  AI_GW_KEY=... python3 gen_images.py 실전1회 8 9        # 특정 문항만(1-based)
프롬프트는 tsc_test_data.json 의 각 문항 prompt 필드에서 읽음(재현/재활용용).
결과는 ../생성이미지/<파일명(image 필드)>.
"""
import os, sys, json, base64, urllib.request, time

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(HERE, "tsc_test_data.json")
IMGDIR = os.path.join(BASE, "생성이미지")
URL = "https://ai-gateway.vercel.sh/v1/images/generations"

def gen_one(prompt, out_path, key):
    body = json.dumps({
        "model": "openai/gpt-image-2",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1,
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    b64 = data["data"][0]["b64_json"]
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64))
    return os.path.getsize(out_path)

def main():
    key = os.environ.get("AI_GW_KEY")
    if not key:
        sys.exit("AI_GW_KEY env var required")
    if len(sys.argv) < 2:
        sys.exit("usage: gen_images.py <round> [qnum ...]")
    rnd = sys.argv[1]
    qsel = set(int(x) for x in sys.argv[2:]) if len(sys.argv) > 2 else None
    with open(DATA, encoding="utf-8") as f:
        d = json.load(f)
    items = d["rounds"][rnd]
    os.makedirs(IMGDIR, exist_ok=True)
    for i, it in enumerate(items, 1):
        if qsel and i not in qsel:
            continue
        out = os.path.join(IMGDIR, it["image"])
        for attempt in range(3):
            try:
                sz = gen_one(it["prompt"], out, key)
                print(f"[OK] {it['image']}  ({sz//1024} KB)")
                break
            except Exception as e:
                print(f"[retry {attempt+1}] {it['image']}: {e}")
                time.sleep(3)
        else:
            print(f"[FAIL] {it['image']}")

if __name__ == "__main__":
    main()
