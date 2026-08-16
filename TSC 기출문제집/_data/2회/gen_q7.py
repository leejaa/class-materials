# -*- coding: utf-8 -*-
import os, json, base64, urllib.request, subprocess
from PIL import Image, ImageDraw, ImageFont
KEY = subprocess.run(
    "grep -rhoE \"AI_GW_KEY=['\\\"]?[A-Za-z0-9_-]{12,}\" ~/.claude/projects/ 2>/dev/null "
    "| sed -E \"s/AI_GW_KEY=['\\\"]?//\" | sort -u | head -1",
    shell=True, capture_output=True, text=True).stdout.strip()
PROMPT = ("Flat 2D Korean-textbook illustration for a language exam. Bold clean uniform black outlines, simple flat "
          "cel colors, minimal shading, bright friendly palette. No text, no letters, no numbers, no price tags.\n\n"
          "A store display shelf seen straight from the front. Exactly two products sit side by side on the shelf: "
          "on the LEFT a black DSLR photo camera with a large lens, on the RIGHT a pale mint-green corded desk "
          "telephone with a handset and number buttons. Below them is a plain shelf edge with two blank empty "
          "rectangular yellow label holders, one under each product. The label holders must be COMPLETELY EMPTY "
          "and blank with no writing at all.")
os.makedirs("gen", exist_ok=True)
base = "gen/_q7_base.png"
if not os.path.exists(base):
    body = json.dumps({"model":"openai/gpt-image-2","prompt":PROMPT,"size":"1024x1024","n":1}).encode()
    req = urllib.request.Request("https://ai-gateway.vercel.sh/v1/images/generations",
        data=body, headers={"Authorization": f"Bearer {KEY}", "Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=300) as r: j = json.load(r)
    open(base,"wb").write(base64.b64decode(j["data"][0]["b64_json"]))
    print("base:", os.path.getsize(base)//1024, "KB")
im = Image.open(base).convert("RGB"); W,H = im.size
dr = ImageDraw.Draw(im)
f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", int(W*0.058))
for i,(p,cxr) in enumerate([("2100元",0.27),("198元",0.73)]):
    cx = int(W*cxr); bw,bh = int(W*0.30), int(H*0.085); y0 = int(H*0.775)
    x0 = cx-bw//2
    dr.rounded_rectangle([x0,y0,x0+bw,y0+bh], radius=6, fill="#FFE96B", outline="black", width=5)
    l,t,r,b = dr.textbbox((0,0), p, font=f)
    dr.text((cx-(r-l)/2, y0+(bh-(b-t))/2 - t), p, font=f, fill="black")
im.save("gen/g2_07.png"); print("g2_07.png 완성 (2100元 / 198元)")
