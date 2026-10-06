import json, sys, html
from playwright.sync_api import sync_playwright

# usage: python3 render_post.py post.json out.png
d = json.load(open(sys.argv[1]))
e = lambda s: html.escape(s)
LOGO = "https://raw.githubusercontent.com/Brispest88/brispest-social/main/assets/logo.png"
points = "".join(f'<li><span class="tick">&#10003;</span>{e(p)}</li>' for p in d["points"])
page = f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;font-family:Inter,Arial,sans-serif;background:#F4F6FA;display:flex;flex-direction:column}}
.top{{background:#0F2341;color:#fff;padding:64px 80px 56px;flex:0 0 auto}}
.badge{{display:inline-block;background:#E3262E;color:#fff;font-weight:800;font-size:28px;letter-spacing:3px;padding:12px 26px;border-radius:40px;text-transform:uppercase}}
h1{{font-size:84px;line-height:1.04;font-weight:900;margin-top:32px;letter-spacing:-2px}}
h1 .red{{color:#FF4A4F}}
.sub{{font-size:32px;line-height:1.35;margin-top:24px;color:#C9D3E6;font-weight:500}}
.mid{{flex:1;padding:44px 80px;display:flex;align-items:center}}
.card{{width:100%;background:#fff;border-radius:28px;padding:40px 50px 20px;box-shadow:0 8px 30px rgba(15,35,65,.08)}}
.card h2{{font-size:34px;color:#0F2341;font-weight:800;margin-bottom:26px;text-transform:uppercase;letter-spacing:1px}}
ul{{list-style:none}}
li{{font-size:32px;color:#1B2A44;line-height:1.3;margin:0 0 22px;display:flex;gap:22px;font-weight:500}}
.tick{{flex:0 0 46px;height:46px;border-radius:50%;background:#E3262E;color:#fff;font-size:26px;display:flex;align-items:center;justify-content:center;margin-top:-2px}}
.cta{{margin:0 80px 36px;background:#E3262E;color:#fff;border-radius:22px;padding:24px 40px;display:flex;justify-content:space-between;align-items:center;gap:24px}}
.cta b{{font-size:30px;font-weight:800;line-height:1.2}} .cta span{{font-size:48px;font-weight:900;white-space:nowrap}}
.foot{{background:#fff;padding:30px 80px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #E3E8F0}}
.logo{{height:80px;width:auto;display:block}}
.url{{text-align:right;color:#0F2341}} .url b{{font-size:32px;display:block}} .url small{{font-size:20px;letter-spacing:3px;color:#5A6780;font-weight:700}}
</style></head><body>
<div class="top"><span class="badge">{e(d["badge"])}</span>
<h1>{e(d["headline"])} <span class="red">{e(d["headline_red"])}</span></h1>
<p class="sub">{e(d["sub"])}</p></div>
<div class="mid"><div class="card"><h2>{e(d["points_title"])}</h2><ul>{points}</ul></div></div>
<div class="cta"><b>{e(d.get("cta","Call or text BrisPest"))}</b><span>0485 038 314</span></div>
<div class="foot"><img class="logo" src="{LOGO}" alt="BrisPest">
<div class="url"><b>brispest.com.au</b><small>COMMERCIAL · RESIDENTIAL · BRISBANE CBD</small></div></div>
</body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(page, wait_until="networkidle")
    h = pg.evaluate('document.documentElement.scrollHeight')
    if h > 1350: sys.exit(f'TOO LONG: {h}px > 1350px - shorten the text and re-run')
    pg.screenshot(path=sys.argv[2])
    b.close()
print("saved", sys.argv[2])
