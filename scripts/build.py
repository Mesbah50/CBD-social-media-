#!/usr/bin/env python3
"""Render the day's posts in the CBD Brand Post Guide style (owner's PDF, from 29 Oct 2026).

Usage: python3 scripts/build.py posts/<date>/content.json
For every post writes, next to the JSON:
  post-<slot>.png     finished 1080x1080 image with the flat kit drawing in the photo slot (fallback)
  overlay-<slot>.png  same layout with a transparent rounded hole where the photo goes (Canva step)
  slot-<slot>.json    the photo slot rectangle + Canva aspect ratio for that layout
"""
import html
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import kit  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
W = H = 1080

# Brand Post Guide colours (only these).
BLUE, RED, GRAY, WEDGE, WHITE = "#05358B", "#E40715", "#F0F0F2", "#5274A4", "#FFFFFF"

CATS = {  # category -> (default layout, English tag, default kit drawing)
    "problem": ("list", "PROBLEM & SOLUTION", "cartons"),
    "news":    ("hero", "IMPORT NEWS", "route"),
    "learn":   ("list", "LEARN IMPORT", "containers"),
    "cost":    ("vs", "COST & PROFIT", "ship"),
    "alert":   ("notice", "ALERT", "warehouse"),
    "idea":    ("hero", "BUSINESS IDEA", "plane"),
}

# Photo slot per layout: left, top, width, height, radius, Canva aspect ratio, slot on dark tile?
SLOTS = {
    "hero":   (60, 540, 960, 380, 28, "LANDSCAPE_2_1", False),
    "list":   (60, 420, 420, 510, 28, "PORTRAIT_4_5", True),
    "vs":     (60, 500, 960, 420, 28, "LANDSCAPE_2_1", False),
    "notice": (60, 580, 960, 340, 28, "LANDSCAPE_2_1", True),
}

FOOT_LEFT = "WhatsApp: 01606481782"
FOOT_RIGHT = "China Bond BD"


def fonts():
    out = []
    for fam, files in (("A", [f"anek-bangla-bengali-{w}" for w in (600, 700, 800)] + [f"anek-bangla-latin-{w}" for w in (600, 700, 800)]),
                       ("Hd", [f"hind-siliguri-bengali-{w}" for w in (400, 500, 600, 700)] + [f"hind-siliguri-latin-{w}" for w in (400, 500, 600, 700)]),
                       ("P", [f"poppins-latin-{w}" for w in (400, 500, 600, 700, 800)])):
        for f in files:
            w = f.rsplit("-", 1)[1]
            rng = ";unicode-range:U+0000-00FF,U+2000-206F" if "latin" in f and fam != "P" else ""
            out.append(f"@font-face{{font-family:{fam};font-weight:{w};src:url({ROOT}/fonts/{f}-normal.woff2){rng}}}")
    return "".join(out)


def latin(t):
    """Wrap runs of English words in Poppins (guide: English text is always Poppins)."""
    return re.sub(r"([A-Za-z0-9][A-Za-z0-9 &/.,:+\-']*[A-Za-z0-9.]|[A-Za-z])",
                  lambda m: f'<span style="font-family:P;font-weight:inherit">{m.group(1)}</span>'
                  if re.search(r"[A-Za-z]", m.group(1)) else m.group(1), t)


def hook_html(text, dark):
    """[word] = the one highlight. Dark bg: white text in a red pill. Light bg: red text."""
    t = latin(html.escape(text))
    if dark:
        rep = r'<span class="hl">\1</span>'
    else:
        rep = rf'<span style="color:{RED}">\1</span>'
    return re.sub(r"\[(.+?)\]", rep, t)


def dots(x, y, cols, rows, color, op):
    return "".join(f'<circle cx="{x + c * 34}" cy="{y + r * 34}" r="3.2" fill="{color}" fill-opacity="{op}"/>'
                   for r in range(rows) for c in range(cols))


def rounded_rect_path(x, y, w, h, r):
    return (f"M{x + r} {y} H{x + w - r} A{r} {r} 0 0 1 {x + w} {y + r} V{y + h - r} A{r} {r} 0 0 1 {x + w - r} {y + h} "
            f"H{x + r} A{r} {r} 0 0 1 {x} {y + h - r} V{y + r} A{r} {r} 0 0 1 {x + r} {y} Z")


def logo(left=60, top=52, bg=WHITE):
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:236px;height:94px;border-radius:24px;background:{bg};'
            f'display:flex;align-items:center;justify-content:center"><img src="{ROOT}/brand/cbd_logo_transparent.png" style="width:196px"></div>')


def tag(text, color, top=84):
    return (f'<div style="position:absolute;right:64px;top:{top}px;font-family:P;font-weight:600;font-size:24px;'
            f'letter-spacing:4px;color:{color}">{html.escape(text)}</div>')


def footer(band, text_c, sub_c):
    return (f'<div style="position:absolute;left:0;top:960px;width:{W}px;height:120px;background:{band};display:flex;'
            f'align-items:center;justify-content:space-between;padding:0 64px">'
            f'<div style="font-family:P;font-weight:600;font-size:30px;color:{text_c}">{FOOT_LEFT}</div>'
            f'<div style="font-family:P;font-weight:500;font-size:28px;color:{sub_c}">{FOOT_RIGHT}</div></div>')


def swoosh(d, width=6):
    return (f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="{width}" stroke-linecap="round"/></svg>')


def headline(post, dark, left, top, width, height, size, color):
    return (f'<div class="fit" data-min="52" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;'
            f'display:flex;flex-direction:column;justify-content:flex-start">'
            f'<div class="t" style="font-family:A;font-weight:800;font-size:{size}px;line-height:1.28;color:{color}">'
            f'{hook_html(post["hook"], dark)}</div></div>')


def sub_line(post, color, left, top, width, size=34):
    s = post.get("sub", "")
    if not s:
        return ""
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px;font-family:Hd;font-weight:500;'
            f'font-size:{size}px;line-height:1.3;color:{color}">{latin(html.escape(s))}</div>')


def photo_slot(layout, post, overlay):
    x, y, w, h, r, _, dark_tile = SLOTS[layout]
    if overlay:
        return ""
    name = post.get("fallback") or CATS[post["category"]][2]
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;overflow:hidden">'
            f'{kit.svg(name, w, h, dark_tile, WHITE if layout == "vs" else None)}</div>')


def layer(bg_html, layout, overlay):
    """Background layers; in overlay mode a rounded hole is cut where the photo goes."""
    if not overlay:
        return f'<div style="position:absolute;inset:0">{bg_html}</div>'
    x, y, w, h, r, *_ = SLOTS[layout]
    clip = f"M0 0 H{W} V{H} H0 Z " + rounded_rect_path(x, y, w, h, r)
    return f'<div style="position:absolute;inset:0;clip-path:path(evenodd, \'{clip}\')">{bg_html}</div>'


def L_hero(post, ov):
    tagtxt = post.get("tag") or CATS[post["category"]][1]
    bg = (f'<div style="position:absolute;inset:0;background:{BLUE}"></div>'
          f'<div style="position:absolute;left:640px;top:-120px;width:620px;height:620px;border-radius:50%;background:#FFFFFF;opacity:.06"></div>'
          f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{dots(0, 470, 9, 3, WHITE, .14)}</svg>')
    cta = (f'<div style="position:absolute;left:60px;top:880px;height:72px;padding:0 34px;border-radius:40px;background:{RED};'
           f'display:flex;align-items:center;gap:14px;font-family:Hd;font-weight:600;font-size:32px;color:{WHITE};'
           f'box-shadow:0 6px 18px rgba(0,0,0,.25)">বিস্তারিত ক্যাপশনে <span style="font-family:P">&#8595;</span></div>')
    return (layer(bg, "hero", ov) + logo() + tag(tagtxt, GRAY) +
            headline(post, True, 60, 178, 960, 270, 96, WHITE) +
            sub_line(post, GRAY, 60, 462, 960) +
            photo_slot("hero", post, ov) + cta + footer(WHITE, BLUE, WEDGE))


def L_list(post, ov):
    tagtxt = post.get("tag") or CATS[post["category"]][1]
    bg = (f'<div style="position:absolute;inset:0;background:{GRAY}"></div>'
          f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{dots(760, 34, 9, 5, WEDGE, .35)}</svg>')
    pts = post.get("points") or []
    nums = "০১ ০২ ০৩ ০৪".split()
    n = max(1, min(4, len(pts)))
    gap = 18
    ch = (510 - gap * (n - 1)) / n
    cards = ""
    for i, p in enumerate(pts[:4]):
        top = 420 + i * (ch + gap)
        ic = RED if i == n - 1 else BLUE
        cards += (f'<div style="position:absolute;left:510px;top:{top:.0f}px;width:510px;height:{ch:.0f}px;border-radius:24px;background:{WHITE};'
                  f'display:flex;align-items:center;gap:20px;padding:0 26px">'
                  f'<div style="flex:none;width:62px;height:62px;border-radius:50%;background:{ic};color:{WHITE};display:flex;align-items:center;'
                  f'justify-content:center;font-family:A;font-weight:800;font-size:30px">{nums[i]}</div>'
                  f'<div class="fit" data-min="22" style="flex:1;height:{ch - 20:.0f}px;display:flex;align-items:center">'
                  f'<div class="t" style="font-family:Hd;font-weight:600;font-size:31px;line-height:1.25;color:{BLUE}">{latin(html.escape(p))}</div></div></div>')
    sw = swoosh("M600 158 C 760 148, 900 142, 1020 138", 5)
    return (layer(bg, "list", ov) + logo() + tag(tagtxt, WEDGE) + sw +
            headline(post, False, 60, 182, 960, 150, 84, BLUE) +
            sub_line(post, WEDGE, 60, 344, 960, 32) +
            photo_slot("list", post, ov) + cards + footer(BLUE, WHITE, GRAY))


def L_vs(post, ov):
    a = post.get("art") or {}
    lt, rt = a.get("left", {}), a.get("right", {})
    bg = (f'<div style="position:absolute;left:0;top:0;width:540px;height:{H}px;background:{BLUE}"></div>'
          f'<div style="position:absolute;left:540px;top:0;width:540px;height:{H}px;background:{GRAY}"></div>'
          f'<svg width="{W}" height="{H}" style="position:absolute;left:0;top:0">{dots(0, 380, 6, 3, WHITE, .14)}{dots(820, 380, 8, 3, WEDGE, .35)}</svg>')

    def side(s, x, dark):
        lab = html.escape(s.get("tag", ""))
        title = html.escape(s.get("label", ""))
        subt = html.escape(s.get("sub", ""))
        c, sc = (WHITE, GRAY) if dark else (BLUE, WEDGE)
        return (f'<div style="position:absolute;left:{x}px;top:180px;width:440px">'
                f'<div style="font-family:P;font-weight:600;font-size:22px;letter-spacing:4px;color:{sc}">{lab}</div>'
                f'<div class="fit" data-min="40" style="height:150px;margin-top:6px"><div class="t" style="font-family:A;font-weight:800;'
                f'font-size:68px;line-height:1.15;color:{c}">{latin(title)}</div></div>'
                f'<div style="font-family:Hd;font-weight:500;font-size:30px;color:{sc};margin-top:4px">{latin(subt)}</div></div>')
    vs = (f'<div style="position:absolute;left:490px;top:450px;width:100px;height:100px;border-radius:50%;background:{RED};'
          f'border:6px solid {WHITE};display:flex;align-items:center;justify-content:center;font-family:P;font-weight:800;'
          f'font-size:34px;color:{WHITE};box-shadow:0 6px 18px rgba(0,0,0,.2)">VS</div>')
    return (layer(bg, "vs", ov) + logo() + side(lt, 60, True) + side(rt, 600, False) +
            photo_slot("vs", post, ov) + vs + footer(WHITE, BLUE, WEDGE))


def L_notice(post, ov):
    head = post.get("notice_title") or "সতর্কতা"
    tagtxt = post.get("tag") or CATS[post["category"]][1]
    bell = (f'<svg width="90" height="90" viewBox="0 0 24 24" style="position:absolute;right:64px;top:56px" fill="none" stroke="{WHITE}" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>'
            '<path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>')
    bg = (f'<div style="position:absolute;inset:0;background:{WHITE}"></div>'
          f'<div style="position:absolute;left:0;top:0;width:{W}px;height:200px;background:{RED}"></div>'
          f'<svg width="{W}" height="200" style="position:absolute;left:0;top:0">{dots(620, 20, 13, 5, WHITE, .18)}</svg>')
    title = (f'<div style="position:absolute;left:64px;top:46px;font-family:A;font-weight:800;font-size:84px;line-height:1.2;color:{WHITE}">'
             f'{html.escape(head)}</div>')
    route = (f'<svg width="{W}" height="120" style="position:absolute;left:0;top:236px">'
             + "".join(f'<circle cx="{470 + i * 16}" cy="{60 - 6 * (i / 22)}" r="3" fill="{BLUE}"/>' for i in range(23))
             + f'<circle cx="466" cy="60" r="7" fill="{RED}"/></svg>')
    return (layer(bg, "notice", ov) + title + bell + logo(60, 236, GRAY) + route +
            tag(tagtxt, WEDGE, 268) +
            headline(post, False, 60, 360, 960, 200, 76, BLUE) +
            photo_slot("notice", post, ov) + footer(BLUE, WHITE, GRAY))


LAYOUTS = {"hero": L_hero, "list": L_list, "vs": L_vs, "notice": L_notice}


def layout_of(post):
    return post.get("layout") or CATS[post["category"]][0]


def page(post, overlay=False):
    lay = layout_of(post)
    body = LAYOUTS[lay](post, overlay)
    return f"""<html><head><meta charset="utf-8"><style>{fonts()}
body{{margin:0;background:transparent}}*{{box-sizing:border-box}}
.hl{{background:{RED};color:{WHITE};border-radius:18px;padding:0 24px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
</style></head><body><div style="width:{W}px;height:{H}px;position:relative;overflow:hidden;font-family:Hd">{body}</div>
<script>document.fonts.ready.then(()=>{{for(const b of document.querySelectorAll('.fit')){{const t=b.querySelector('.t');
let s=parseFloat(getComputedStyle(t).fontSize);const m=+b.dataset.min;
while((t.scrollHeight>b.clientHeight||t.scrollWidth>b.clientWidth)&&s>m){{s-=2;t.style.fontSize=s+'px';}}}}
document.body.dataset.ready=1;}});</script></body></html>"""


def main(path):
    path = pathlib.Path(path).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    out = path.parent
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for post in data["posts"]:
            n = post["slot"]
            for ov, name in ((False, f"post-{n}.png"), (True, f"overlay-{n}.png")):
                f = out / f"_tmp-{n}.html"
                f.write_text(page(post, ov), encoding="utf-8")
                pg.goto("file://" + str(f))
                pg.wait_for_selector("body[data-ready]", timeout=20000)
                pg.screenshot(path=str(out / name), omit_background=ov)
                f.unlink()
            x, y, w, h, r, ar, _ = SLOTS[layout_of(post)]
            (out / f"slot-{n}.json").write_text(json.dumps(
                {"layout": layout_of(post), "left": x, "top": y, "width": w, "height": h, "aspectRatio": ar}), encoding="utf-8")
            print("rendered", out / f"post-{n}.png", "+ overlay")
        b.close()


if __name__ == "__main__":
    main(sys.argv[1])
