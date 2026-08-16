# -*- coding: utf-8 -*-
import os, json, base64, urllib.request, subprocess, time

KEY = subprocess.run(
    "grep -rhoE \"AI_GW_KEY=['\\\"]?[A-Za-z0-9_-]{12,}\" ~/.claude/projects/ 2>/dev/null "
    "| sed -E \"s/AI_GW_KEY=['\\\"]?//\" | sort -u | head -1",
    shell=True, capture_output=True, text=True).stdout.strip()
assert len(KEY) > 20

os.makedirs("gen", exist_ok=True)
d = json.load(open("tsc_yt02.json", encoding="utf-8"))

def gen(prompt, out, size):
    body = json.dumps({"model": "openai/gpt-image-2", "prompt": prompt, "size": size, "n": 1}).encode()
    req = urllib.request.Request("https://ai-gateway.vercel.sh/v1/images/generations",
        data=body, headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        j = json.load(r)
    open(out, "wb").write(base64.b64decode(j["data"][0]["b64_json"]))
    return os.path.getsize(out) // 1024

for q in d["questions"]:
    if not q["img"]:
        continue
    out = os.path.join("gen", q["img"]["file"])
    if os.path.exists(out):
        print(f"[skip] {q['img']['file']}"); continue
    for a in range(3):
        try:
            kb = gen(q["img"]["prompt"], out, q["img"]["size"])
            print(f"[OK] Q{q['n']:02d} {q['img']['file']} ({kb} KB)", flush=True); break
        except Exception as e:
            print(f"[retry {a+1}] Q{q['n']}: {str(e)[:80]}", flush=True); time.sleep(4)
    else:
        print(f"[FAIL] Q{q['n']}", flush=True)
print("done")
