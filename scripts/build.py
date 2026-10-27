#!/usr/bin/env python3
"""Render the day's post images from posts/<date>/content.json.

Usage: python3 scripts/build.py posts/2026-10-28/content.json
Writes posts/<date>/post-<slot>.png (1080x1080, 1:1) next to the JSON.
"""
import html
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import creative  # noqa: E402
import background  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1080, 1080

# Six categories: label shown on the image, accent colours, illustration.
CATS = {
    "problem":  {"label": "সমস্যা ও সমাধান", "bg": "#0B1B3A", "accent": "#FFD60A", "badge": "#E63946"},
    "news":     {"label": "ইমপোর্ট নিউজ",     "bg": "#0F2A4A", "accent": "#5CC8FF", "badge": "#1F6FD1"},
    "trending": {"label": "ট্রেন্ডিং প্রোডাক্ট", "bg": "#2A0F2E", "accent": "#FFB000", "badge": "#E63946"},
    "cost":     {"label": "খরচ ও লাভের হিসাব", "bg": "#0C2B24", "accent": "#2EE6A6", "badge": "#1FA463"},
    "alert":    {"label": "সতর্কতা",            "bg": "#2B0E0E", "accent": "#FFD60A", "badge": "#E63946"},
    "idea":     {"label": "বিজনেস আইডিয়া",     "bg": "#0B1B3A", "accent": "#FF8A00", "badge": "#FF8A00"},
}

PLANE = ('<g transform="translate({x} {y}) rotate({r}) scale({s})" fill="#FFFFFF">'
         '<path d="M-70 0 L60 0 Q90 0 90 10 Q90 20 60 20 L-70 20 Z"/>'
         '<path d="M-10 10 L-50 -60 L-28 -60 L30 10 Z"/><path d="M-10 10 L-50 80 L-28 80 L30 10 Z"/>'
         '<path d="M-70 10 L-90 -24 L-76 -24 L-52 10 Z"/><path d="M-70 10 L-90 44 L-76 44 L-52 10 Z"/></g>')


def box(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<ellipse cx="0" cy="150" rx="170" ry="18" fill="#000" fill-opacity="0.35"/>'
            '<polygon points="-150,0 0,-40 150,0 0,40" fill="#E2B06E"/>'
            '<polygon points="-150,0 0,40 0,150 -150,110" fill="#C98F45"/>'
            '<polygon points="0,40 150,0 150,110 0,150" fill="#B07A35"/>'
            '<polygon points="-90,-16 70,26 100,18 -60,-24" fill="#D9C29A"/>'
            '<polygon points="-130,40 -20,68 -20,120 -130,92" fill="#FFFFFF"/>'
            '<text x="-75" y="88" text-anchor="middle" font-size="22" font-weight="800" fill="#E63946" '
            'transform="rotate(14 -75 85)" font-family="A">MADE IN CHINA</text></g>')


def ship(x, y, s=1.0):
    cols = ["#E63946", "#1F6FD1", "#FFD60A", "#1FA463", "#FF8A00", "#E63946", "#1F6FD1"]
    c = "".join(f'<rect x="{-200 + (i % 4) * 78}" y="{-110 + (i // 4) * 50}" width="74" height="46" fill="{cols[i]}"/>'
                for i in range(7))
    return (f'<g transform="translate({x} {y}) scale({s})">{c}'
            '<rect x="120" y="-150" width="60" height="140" fill="#F3F4F6"/><rect x="130" y="-136" width="40" height="18" fill="#0B1B3A"/>'
            '<polygon points="-240,-10 220,-10 190,70 -210,70" fill="#C62F3B"/>'
            '<rect x="-225" y="-10" width="430" height="12" fill="#F3F4F6"/>'
            '<text x="-10" y="48" text-anchor="middle" font-size="28" font-weight="800" fill="#FFF" letter-spacing="4" font-family="A">CARGO</text></g>')


def sea(y):
    wave = " ".join(f"T {i * 60} {y + 18}" for i in range(2, 20))
    return (f'<rect x="0" y="{y}" width="1080" height="400" fill="#123A7A"/>'
            f'<path d="M0 {y + 18} Q 30 {y + 6} 60 {y + 18} {wave}" fill="none" stroke="#4F7FD1" stroke-width="4"/>')


def route(acc):
    return ('<path d="M120 170 Q 540 20 960 150" fill="none" stroke="#FFF" stroke-opacity="0.55" stroke-width="5" stroke-dasharray="18 14"/>'
            '<circle cx="120" cy="170" r="30" fill="#E63946"/><text x="120" y="181" text-anchor="middle" font-size="28" font-weight="800" fill="#FFF" font-family="A">CN</text>'
            '<circle cx="960" cy="150" r="30" fill="#1FA463"/><circle cx="960" cy="150" r="11" fill="#E63946"/>'
            + PLANE.format(x=560, y=75, r=8, s=0.65))


def art(cat, acc):
    """Bottom illustration, 1080 x 470, drawn per category. Always carries import elements."""
    if cat == "problem":
        body = (sea(330) + ship(700, 330, 0.85) + route(acc) +
                '<g transform="translate(190 230)"><circle r="78" fill="#E63946"/><path d="M-30 -30 L30 30 M30 -30 L-30 30" stroke="#FFF" stroke-width="16" stroke-linecap="round"/></g>'
                '<path d="M290 230 L380 230" stroke="#FFF" stroke-width="10" stroke-linecap="round"/><path d="M360 205 L390 230 L360 255" fill="none" stroke="#FFF" stroke-width="10" stroke-linecap="round"/>'
                '<g transform="translate(470 230)"><circle r="78" fill="#1FA463"/><path d="M-34 0 L-8 26 L36 -24" fill="none" stroke="#FFF" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>')
    elif cat == "news":
        body = (sea(360) + ship(770, 360, 0.8) + route(acc) +
                '<g transform="translate(170 215)"><rect width="380" height="230" rx="14" fill="#F3F4F6"/>'
                f'<rect width="380" height="64" rx="14" fill="{acc}"/><text x="190" y="46" text-anchor="middle" font-size="40" font-weight="800" fill="#0B1B3A" font-family="A">NEWS</text>'
                '<rect x="24" y="90" width="150" height="110" fill="#9AA7BF"/>'
                + "".join(f'<rect x="196" y="{94 + i * 26}" width="{160 - (i % 2) * 40}" height="12" rx="6" fill="#9AA7BF"/>' for i in range(5))
                + '<rect x="24" y="206" width="330" height="12" rx="6" fill="#9AA7BF"/></g>')
    elif cat == "trending":
        body = (route(acc) + box(330, 270, 1.15) +
                f'<path d="M560 380 L680 290 L760 330 L930 170" fill="none" stroke="{acc}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M880 160 L940 160 L940 220" fill="none" stroke="{acc}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<g transform="translate(560 200)"><polygon points="0,-46 13,-14 48,-14 20,6 30,40 0,20 -30,40 -20,6 -48,-14 -13,-14" fill="{acc}"/></g>')
    elif cat == "cost":
        rows = "".join(f'<rect x="40" y="{40 + i * 46}" width="170" height="16" rx="8" fill="#9AA7BF"/>'
                       f'<rect x="250" y="{40 + i * 46}" width="90" height="16" rx="8" fill="#5B6B8C"/>' for i in range(4))
        body = (route(acc) + box(800, 280, 1.0) +
                f'<g transform="translate(170 215)"><rect width="380" height="250" rx="16" fill="#F3F4F6"/>{rows}'
                f'<rect x="40" y="226" width="300" height="4" fill="#0B1B3A"/></g>'
                f'<g transform="translate(560 330)"><circle r="62" fill="{acc}"/><text y="24" text-anchor="middle" font-size="72" font-weight="800" fill="#0B1B3A" font-family="A">৳</text></g>')
    elif cat == "alert":
        body = (sea(360) + ship(780, 360, 0.75) + route(acc) +
                f'<g transform="translate(300 290)"><polygon points="0,-150 165,130 -165,130" fill="{acc}" stroke="#0B1B3A" stroke-width="10" stroke-linejoin="round"/>'
                '<rect x="-14" y="-60" width="28" height="120" rx="12" fill="#0B1B3A"/><circle cx="0" cy="96" r="17" fill="#0B1B3A"/></g>')
    else:  # idea
        body = (sea(360) + ship(800, 360, 0.75) + route(acc) + box(560, 330, 0.7) +
                f'<g transform="translate(240 260)"><circle cy="-30" r="110" fill="{acc}" fill-opacity="0.25"/><circle cy="-30" r="80" fill="{acc}"/>'
                '<rect x="-36" y="46" width="72" height="22" rx="6" fill="#C9D3E6"/><rect x="-30" y="72" width="60" height="18" rx="6" fill="#9AA7BF"/>'
                '<path d="M-20 -30 L0 0 L20 -30" fill="none" stroke="#FFF" stroke-width="8" stroke-linecap="round"/></g>')
    return f'<svg width="1080" height="370" viewBox="0 0 1080 470" preserveAspectRatio="xMidYMax meet" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


BRAND_BLUE = "#02378F"
BRAND_RED = "#E70611"
HL_RED = "#FF3340"     # brighter red for text on black boxes


def hook_html(text):
    """[word] marks the highlighted (red) part of the hook."""
    t = html.escape(text)
    return re.sub(r"\[(.+?)\]", lambda m: f'<span style="color:{HL_RED}">{m.group(1)}</span>', t)


def page(post):
    c = CATS[post["category"]]
    if post.get("style") not in creative.STYLES:
        raise ValueError(f"slot {post.get('slot')}: style must be one of {creative.STYLES}")
    creative.GLOW = "#6F9BFF"
    art_svg, art_ov = creative.render(post["style"], post.get("art", {}), BRAND_RED)
    bg_svg = background.svg(W, H)
    sub = html.escape(post.get("sub", "")) or "বিস্তারিত ক্যাপশনে ↓"
    fonts = "".join(
        f'@font-face{{font-family:A;font-weight:{w};src:url({ROOT}/fonts/anek-bangla-bengali-{w}-normal.woff2)}}'
        for w in (500, 600, 700, 800)) + "".join(
        f'@font-face{{font-family:A;font-weight:{w};src:url({ROOT}/fonts/anek-bangla-latin-{w}-normal.woff2);unicode-range:U+0000-00FF}}'
        for w in (500, 600, 700, 800))
    k = 0.84  # art scale inside the frame
    return f"""<html><head><meta charset="utf-8"><style>{fonts}body{{margin:0}}*{{box-sizing:border-box}}
.hook{{display:inline;background:#0E0E0E;color:#FFFFFF;padding:6px 26px;line-height:1.52;
  box-decoration-break:clone;-webkit-box-decoration-break:clone}}</style></head><body>
<div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;font-family:A;color:#0E0E0E">
 <div style="position:absolute;inset:0">{bg_svg}</div>
 <!-- brand blue block (where the reference has its colour panel) -->
 <div style="position:absolute;left:190px;top:150px;width:850px;height:440px;background:{BRAND_BLUE}"></div>
 <div style="position:absolute;left:190px;top:150px;width:850px;height:10px;background:{BRAND_RED}"></div>
 <!-- quote mark -->
 <div style="position:absolute;left:30px;top:150px;font-size:230px;font-weight:800;line-height:1;color:{BRAND_RED};font-family:Georgia,serif">&ldquo;</div>
 <!-- logo -->
 <div style="position:absolute;right:40px;top:34px;display:flex"><img src="{ROOT}/brand/cbd_logo_badge.png" style="width:210px;display:block"></div>
 <!-- creative concept -->
 <div style="position:absolute;left:160px;top:110px;width:{creative.ART_W * k:.0f}px;height:{creative.ART_H * k:.0f}px;clip-path:inset(40px -60px -120px -60px)">
  <div style="position:absolute;left:0;top:0;width:{creative.ART_W}px;height:{creative.ART_H}px;transform:scale({k});transform-origin:0 0">
   <svg width="{creative.ART_W}" height="{creative.ART_H}" viewBox="0 0 {creative.ART_W} {creative.ART_H}" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0;font-family:A;overflow:visible">{art_svg}</svg>
   {art_ov}
  </div>
 </div>
 <!-- hook: stacked black boxes -->
 <div id="hookbox" style="position:absolute;left:44px;top:560px;width:700px;height:360px;display:flex;align-items:flex-start">
  <div id="hook" style="font-size:78px;font-weight:800"><span class="hook">{hook_html(post['hook'])}</span></div>
 </div>
 <!-- attribution-style footer: red bar, category, sub line -->
 <div style="position:absolute;left:50px;bottom:40px;display:flex;gap:18px;align-items:stretch">
  <div style="width:6px;background:{BRAND_RED}"></div>
  <div style="display:flex;flex-direction:column;gap:2px">
   <div style="font-size:38px;font-weight:800;color:{BRAND_BLUE};line-height:1.2">{c['label']}</div>
   <div style="font-size:28px;font-weight:600;color:#333;line-height:1.25">{sub}</div>
  </div>
 </div>
</div>
<script>document.fonts.ready.then(()=>{{const h=document.getElementById('hook'),b=document.getElementById('hookbox');let s=78;
while(h.scrollHeight>b.clientHeight&&s>38){{s-=2;h.style.fontSize=s+'px';}}document.body.dataset.ready=1;}});</script>
</body></html>"""


def main(path):
    path = pathlib.Path(path).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    out_dir = path.parent
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for post in data["posts"]:
            f = out_dir / f"_tmp-{post['slot']}.html"
            f.write_text(page(post), encoding="utf-8")
            pg.goto("file://" + str(f))
            pg.wait_for_selector("body[data-ready]", timeout=15000)
            pg.screenshot(path=str(out_dir / f"post-{post['slot']}.png"))
            f.unlink()
            print("rendered", out_dir / f"post-{post['slot']}.png")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
