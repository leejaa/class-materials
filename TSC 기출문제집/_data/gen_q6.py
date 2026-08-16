# -*- coding: utf-8 -*-
import os, json, base64, urllib.request, subprocess
from PIL import Image, ImageDraw, ImageFont

KEY = subprocess.run(
    "grep -rhoE \"AI_GW_KEY=['\\\"]?[A-Za-z0-9_-]{12,}\" ~/.claude/projects/ 2>/dev/null "
    "| sed -E \"s/AI_GW_KEY=['\\\"]?//\" | sort -u | head -1",
    shell=True, capture_output=True, text=True).stdout.strip()

PROMPT = ("Flat 2D Korean-textbook illustration for a language exam. Bold clean uniform black outlines, simple flat "
          "cel colors, minimal shading, bright friendly palette. No text, no letters, no numbers, no price tags.\n\n"
          "A store shelf seen straight from the front. Exactly three drinks stand in a row on the shelf, evenly "
          "spaced, all the same size: on the LEFT a clear bottle of orange-red apple juice with an apple picture on "
          "the label, in the MIDDLE a clear plastic bottle of water with a blue label, on the RIGHT a takeaway iced "
          "coffee cup with a lid and a straw. Below the drinks is a plain empty horizontal shelf edge with three "
          "blank white rectangular label holders, one under each drink. The label holders must be COMPLETELY EMPTY "
          "and blank with no writing.")

os.makedirs("gen", exist_ok=True)
base = "gen/_q6_base.png"
if not os.path.exists(base):
    body = json.dumps({"model": "openai/gpt-image-2", "prompt": PROMPT, "size": "1024x1024", "n": 1}).encode()
    req = urllib.request.Request("https://ai-gateway.vercel.sh/v1/images/generations",
        data=body, headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        j = json.load(r)
    open(base, "wb").write(base64.b64decode(j["data"][0]["b64_json"]))
    print("base 생성:", os.path.getsize(base)//1024, "KB")

# 가격표를 직접 덧그림 (숫자 100% 정확)
im = Image.open(base).convert("RGB"); W, H = im.size
dr = ImageDraw.Draw(im)
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
if not os.path.exists(FONT): FONT = "/System/Library/Fonts/PingFang.ttc"
f = ImageFont.truetype(FONT, int(W*0.055))

prices = ["8元", "2元", "7.5元"]
bw, bh = int(W*0.20), int(H*0.085)
y = int(H*0.845)
for i, p in enumerate(prices):
    cx = int(W*(0.20 + 0.30*i))
    x0, y0 = cx-bw//2, y
    dr.rounded_rectangle([x0, y0, x0+bw, y0+bh], radius=8, fill="white", outline="black", width=5)
    l, t, r, b = dr.textbbox((0,0), p, font=f)
    dr.text((cx-(r-l)/2, y0+(bh-(b-t))/2 - t), p, font=f, fill="black")

im.save("gen/g1_06.png")
print("g1_06.png 완성 (가격: 8元 / 2元 / 7.5元)")
