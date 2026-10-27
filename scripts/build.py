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


def hook_html(text, acc, bg):
    """[word] marks the highlighted part of the hook."""
    t = html.escape(text)
    return re.sub(r"\[(.+?)\]",
                  lambda m: f'<span style="background:{acc};color:{bg};padding:0 14px;border-radius:12px;'
                            f'box-decoration-break:clone;-webkit-box-decoration-break:clone">{m.group(1)}</span>', t)


def page(post):
    c = CATS[post["category"]]
    acc, bg = c["accent"], c["bg"]
    if post.get("style") not in creative.STYLES:
        raise ValueError(f"slot {post.get('slot')}: style must be one of {creative.STYLES}")
    art_svg, art_ov = creative.render(post["style"], post.get("art", {}), acc)
    sub = f'<div style="font-size:36px;font-weight:600;color:#D7DEEA;line-height:1.3">{html.escape(post["sub"])}</div>' if post.get("sub") else ""
    pts = ""
    if False and post.get("points"):
        pts = '<div style="display:flex;flex-direction:column;gap:10px">' + "".join(
            f'<div style="display:flex;gap:14px;align-items:center;font-size:29px;font-weight:600">'
            f'<span style="flex:0 0 36px;height:36px;border-radius:50%;background:{acc};color:{bg};display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800">{i + 1}</span>'
            f'<span>{html.escape(p)}</span></div>' for i, p in enumerate(post["points"][:3])) + "</div>"
    hb = 200 if post.get("sub") else 250
    fonts = "".join(
        f'@font-face{{font-family:A;font-weight:{w};src:url({ROOT}/fonts/anek-bangla-bengali-{w}-normal.woff2)}}'
        for w in (500, 600, 700, 800)) + "".join(
        f'@font-face{{font-family:A;font-weight:{w};src:url({ROOT}/fonts/anek-bangla-latin-{w}-normal.woff2);unicode-range:U+0000-00FF}}'
        for w in (500, 600, 700, 800))
    return f"""<html><head><meta charset="utf-8"><style>{fonts}body{{margin:0}}*{{box-sizing:border-box}}</style></head><body>
<div style="width:{W}px;height:{H}px;background:{bg};color:#fff;font-family:A;position:relative;overflow:hidden">
<div style="position:absolute;right:-200px;top:-200px;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle,{acc}33 0%,{acc}00 65%)"></div>
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 70%,rgba(255,255,255,0.07) 0%,rgba(0,0,0,0) 45%,rgba(0,0,0,0.45) 100%)"></div>
<div style="position:absolute;left:0;bottom:80px;width:{creative.ART_W}px;height:{creative.ART_H}px">
 <svg width="{creative.ART_W}" height="{creative.ART_H}" viewBox="0 0 {creative.ART_W} {creative.ART_H}" xmlns="http://www.w3.org/2000/svg" style="position:absolute;left:0;top:0;font-family:A;overflow:visible">{art_svg}</svg>
 {art_ov}
</div>
<div style="position:absolute;left:0;right:0;bottom:90px;height:120px;background:linear-gradient(to bottom,{bg}00,{bg}00)"></div>
<div style="position:relative;padding:48px 60px 0 60px;display:flex;flex-direction:column;gap:18px">
 <div style="display:flex;justify-content:space-between;align-items:center">
  <div style="background:{c['badge']};font-size:32px;font-weight:700;padding:8px 26px;border-radius:999px">{c['label']}</div>
  <div style="background:#FEFEFE;border-radius:18px;padding:4px 8px;display:flex"><img src="{ROOT}/brand/cbd_logo_badge.png" style="width:200px;display:block"></div>
 </div>
 <div id="hookbox" style="height:{hb}px;display:flex;flex-direction:column;justify-content:center">
  <div id="hook" style="font-size:84px;font-weight:800;line-height:1.3">{hook_html(post['hook'], acc, bg)}</div>
 </div>
 {sub}{pts}
</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:80px;background:#060F22;display:flex;align-items:center;justify-content:space-between;padding:0 60px;font-size:30px;font-weight:700">
 <span>সেভ করে রাখুন</span><span style="color:{acc}">বিস্তারিত ক্যাপশনে ↓</span>
</div></div>
<script>document.fonts.ready.then(()=>{{const h=document.getElementById('hook'),b=document.getElementById('hookbox');let s=84;while(h.scrollHeight>b.clientHeight&&s>48){{s-=4;h.style.fontSize=s+'px';}}document.body.dataset.ready=1;}});</script>
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
