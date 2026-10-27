"""Creative concept art for CBD posts.

Every post image uses exactly one of seven creative styles:
  exaggeration, animal, material, shape, benefit, contrast, shadow

render(style, spec, accent) -> (svg_inner, overlay_html) for an art panel of
ART_W x ART_H px. Props are flat vector drawings centred on (0, 0) and roughly
200 x 200 at scale 1.
"""
import html
import math
import random

ART_W, ART_H = 1080, 600
STYLES = ("exaggeration", "animal", "material", "shape", "benefit", "contrast", "shadow")

FONT = "A"

# ---------------------------------------------------------------- palettes

BASE = {
    "box": dict(main="#C98F45", dark="#B07A35", light="#E2B06E", accent="#E63946", ink="#0B1B3A", white="#FFFFFF"),
    "container": dict(main="#E63946", dark="#B52632", light="#F26B76", accent="#FFD60A", ink="#7A1820", white="#FFFFFF"),
    "ship": dict(main="#C62F3B", dark="#8E1F28", light="#F3F4F6", accent="#1F6FD1", ink="#0B1B3A", white="#FFFFFF",
                 cargo=["#E63946", "#1F6FD1", "#FFD60A", "#1FA463", "#FF8A00"]),
    "plane": dict(main="#F3F4F6", dark="#9AA7BF", light="#FFFFFF", accent="#1F6FD1", ink="#0B1B3A", white="#FFFFFF"),
    "warehouse": dict(main="#2C3D63", dark="#1A2747", light="#3A4D75", accent="#E63946", ink="#0B1B3A", white="#FFFFFF"),
    "coin": dict(main="#F4C430", dark="#C99A0E", light="#FFE07A", accent="#C99A0E", ink="#7A5A00", white="#FFFFFF"),
    "money": dict(main="#2EAD6B", dark="#1B7A48", light="#7BD6A4", accent="#1B7A48", ink="#0E4A2B", white="#E9FFF2"),
    "cushion": dict(main="#5B8DEF", dark="#3A6AD0", light="#8FB2F7", accent="#FFFFFF", ink="#1E3F8A", white="#FFFFFF"),
    "cloud": dict(main="#FFFFFF", dark="#C9D3E6", light="#FFFFFF", accent="#E3EAF6", ink="#9AA7BF", white="#FFFFFF"),
    "blocks": dict(main="#E63946", dark="#1F6FD1", light="#FFD60A", accent="#1FA463", ink="#FFFFFF", white="#FFFFFF"),
    "magnifier": dict(main="#9AA7BF", dark="#5B6B8C", light="#CFE8FF", accent="#FFFFFF", ink="#0B1B3A", white="#FFFFFF"),
    "question": dict(main="#FFD60A", dark="#C9A800", light="#FFE97A", accent="#0B1B3A", ink="#0B1B3A", white="#FFFFFF"),
    "check": dict(main="#1FA463", dark="#147A48", light="#5BD08F", accent="#FFFFFF", ink="#FFFFFF", white="#FFFFFF"),
    "cross": dict(main="#E63946", dark="#B52632", light="#F26B76", accent="#FFFFFF", ink="#FFFFFF", white="#FFFFFF"),
    "tag": dict(main="#FFD60A", dark="#C9A800", light="#FFE97A", accent="#E63946", ink="#0B1B3A", white="#FFFFFF"),
    "phone": dict(main="#1A2747", dark="#0B1B3A", light="#5CC8FF", accent="#FF8A00", ink="#FFFFFF", white="#FFFFFF"),
    "cart": dict(main="#FF8A00", dark="#C96A00", light="#FFB35C", accent="#0B1B3A", ink="#0B1B3A", white="#FFFFFF"),
    "shop": dict(main="#F3F4F6", dark="#9AA7BF", light="#E63946", accent="#FFFFFF", ink="#0B1B3A", white="#FFFFFF"),
    "lamp": dict(main="#FFB000", dark="#C98500", light="#FFE07A", accent="#5B6B8C", ink="#0B1B3A", white="#FFFFFF"),
    "trophy": dict(main="#F4C430", dark="#C99A0E", light="#FFE07A", accent="#8A5A00", ink="#7A5A00", white="#FFFFFF"),
    "chair": dict(main="#3A4D75", dark="#1A2747", light="#5B6B8C", accent="#5B8DEF", ink="#0B1B3A", white="#FFFFFF"),
    "pan": dict(main="#3B3F46", dark="#1E2126", light="#6B7280", accent="#FFB000", ink="#0B1B3A", white="#FFFFFF"),
    "factory": dict(main="#3A4D75", dark="#2C3D63", light="#5B6B8C", accent="#E63946", ink="#0B1B3A", white="#FFFFFF"),
}

MATERIALS = {
    "gold":    dict(main="#F4C430", dark="#C99A0E", light="#FFE58A", accent="#B8860B", ink="#7A5A00", white="#FFF6D0"),
    "glass":   dict(main="#BFE6FF", dark="#7CC4F0", light="#E8F7FF", accent="#9FD8FF", ink="#3A7FB0", white="#F4FBFF"),
    "steel":   dict(main="#A9B4C2", dark="#6B7686", light="#D5DCE5", accent="#8792A2", ink="#3B4552", white="#E8EDF2"),
    "cloud":   dict(main="#FFFFFF", dark="#DCE4F2", light="#FFFFFF", accent="#EEF2FA", ink="#B8C4D8", white="#FFFFFF"),
    "feather": dict(main="#FFFFFF", dark="#E3E7EF", light="#FFFFFF", accent="#F1F3F8", ink="#C3CAD8", white="#FFFFFF"),
    "ice":     dict(main="#AEEBFF", dark="#6CCCF0", light="#E6FAFF", accent="#8FDFFF", ink="#2E8DB8", white="#F2FDFF"),
    "cotton":  dict(main="#FFF7F2", dark="#EADFD8", light="#FFFFFF", accent="#F6ECE6", ink="#C9B8AE", white="#FFFFFF"),
}

SHADOW = dict(main="#000", dark="#000", light="#000", accent="#000", ink="#000", white="#000", cargo=["#000"] * 5)


_DEFS = {}


def lg(c1, c2, vertical=True):
    """Register a linear gradient and return its url()."""
    gid = "lg" + str(abs(hash((c1, c2, vertical))) % 10**8)
    if gid not in _DEFS:
        xy = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="1"'
        _DEFS[gid] = (f'<linearGradient id="{gid}" {xy}><stop offset="0" stop-color="{c1}"/>'
                      f'<stop offset="1" stop-color="{c2}"/></linearGradient>')
    return f"url(#{gid})"


def rg(c1, c2):
    gid = "rg" + str(abs(hash((c1, c2))) % 10**8)
    if gid not in _DEFS:
        _DEFS[gid] = (f'<radialGradient id="{gid}" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="{c1}"/>'
                      f'<stop offset="1" stop-color="{c2}"/></radialGradient>')
    return f"url(#{gid})"


def shade(c, f):
    """Lighten (f>0) or darken (f<0) a #rrggbb colour."""
    if not (isinstance(c, str) and c.startswith("#") and len(c) == 7):
        return c
    r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
    if f >= 0:
        r, g, b = (int(v + (255 - v) * f) for v in (r, g, b))
    else:
        r, g, b = (int(v * (1 + f)) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


BASE_DEFS = ('<filter id="ds" x="-30%" y="-30%" width="160%" height="170%">'
             '<feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000" flood-opacity="0.45"/></filter>'
             '<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>'
             '<radialGradient id="floorg"><stop offset="0" stop-color="#000" stop-opacity="0.55"/>'
             '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>')


def pal(name, override=None):
    p = dict(BASE.get(name, BASE["box"]))
    if override:
        p.update(override)
        p.setdefault("cargo", [override["main"], override["light"], override["dark"], override["accent"], override["main"]])
        if "cargo" in BASE.get(name, {}) and override is not SHADOW:
            p["cargo"] = [override["main"], override["light"], override["dark"], override["accent"], override["main"]]
    return p


def T(x, y, s=1.0, rot=0, inner=""):
    r = f" rotate({rot})" if rot else ""
    return f'<g transform="translate({x:.1f} {y:.1f}){r} scale({s:.3f})">{inner}</g>'


def text(x, y, s, size, fill, weight=800, anchor="middle", extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" {extra}>{html.escape(s)}</text>')


# ---------------------------------------------------------------- props

def p_box(p, label="MADE IN CHINA"):
    top, left, right = p["light"], p["main"], p["dark"]
    return (f'<polygon points="-100,-20 0,-55 100,-20 0,15" fill="{lg(shade(top, .25), top)}"/>'
            f'<polygon points="-100,-20 0,15 0,100 -100,65" fill="{lg(shade(left, .1), shade(left, -.12))}"/>'
            f'<polygon points="0,15 100,-20 100,65 0,100" fill="{lg(right, shade(right, -.25))}"/>'
            f'<polygon points="-62,-33 38,2 54,-4 -46,-39" fill="{shade(top, -.18)}"/>'
            f'<polygon points="-50,-37 50,-2 54,-4 -46,-39" fill="#FFFFFF" fill-opacity="0.25"/>'
            f'<polygon points="0,15 0,100 6,98 6,13" fill="#000" fill-opacity="0.12"/>'
            f'<polyline points="-100,-20 0,15 100,-20" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/>'
            f'<polygon points="-86,22 -14,44 -14,82 -86,60" fill="{p["white"]}"/>'
            f'<polygon points="-86,22 -14,44 -14,50 -86,28" fill="{p["accent"]}"/>'
            + text(-50, 62, label.split(" ")[0] if label else "", 12, p["accent"], extra='transform="rotate(17 -50 58)"')
            + text(-50, 76, " ".join(label.split(" ")[1:]) if label else "", 12, p["ink"], extra='transform="rotate(17 -50 72)"')
            + "".join(f'<path d="M{30 + i * 18} {8 - i * 6} l0 26 m6 -2 l0 26" stroke="{shade(right, -.35)}" stroke-width="3"/>' for i in range(3)))


def p_container(p, label="CBD"):
    m = p["main"]
    ridges = "".join(f'<rect x="{-95 + i * 19}" y="-52" width="9" height="104" fill="{lg(shade(m, -.25), shade(m, -.05))}"/>'
                     f'<rect x="{-95 + i * 19}" y="-52" width="2" height="104" fill="#FFFFFF" fill-opacity="0.25"/>' for i in range(10))
    return (f'<polygon points="-110,-60 110,-60 134,-76 -86,-76" fill="{shade(m, .25)}"/>'
            f'<polygon points="110,-60 134,-76 134,44 110,60" fill="{shade(m, -.4)}"/>'
            f'<rect x="-110" y="-60" width="220" height="120" fill="{lg(shade(m, .1), shade(m, -.2))}"/>{ridges}'
            + "".join(f'<rect x="{x}" y="{y}" width="14" height="14" fill="{shade(m, -.5)}"/>' for x in (-110, 96) for y in (-60, 46))
            + f'<rect x="-46" y="-22" width="92" height="40" rx="6" fill="{p["white"]}"/>'
            + text(0, 10, label, 28, p["ink"]))


def p_ship(p):
    c = p.get("cargo", BASE["ship"]["cargo"])
    stack = "".join(f'<rect x="{-90 + (i % 4) * 44}" y="{-62 + (i // 4) * 30}" width="41" height="27" fill="{c[i % len(c)]}"/>'
                    for i in range(8))
    return (stack + f'<rect x="80" y="-90" width="34" height="88" fill="{p["light"]}"/>'
            f'<rect x="86" y="-80" width="22" height="12" fill="{p["ink"]}"/>'
            f'<polygon points="-120,0 130,0 108,52 -100,52" fill="{p["main"]}"/>'
            f'<rect x="-112" y="0" width="236" height="8" fill="{p["light"]}"/>'
            + text(4, 38, "CARGO", 20, p["white"], extra='letter-spacing="3"'))


def p_plane(p):
    return (f'<g fill="{p["main"]}"><path d="M-110 -8 L80 -8 Q120 -8 120 4 Q120 16 80 16 L-110 16 Z"/>'
            f'<path d="M-20 4 L-70 -80 L-42 -80 L40 4 Z"/><path d="M-20 4 L-70 88 L-42 88 L40 4 Z"/>'
            f'<path d="M-110 4 L-132 -40 L-114 -40 L-84 4 Z"/><path d="M-110 4 L-132 48 L-114 48 L-84 4 Z"/></g>'
            f'<rect x="-60" y="-3" width="110" height="6" rx="3" fill="{p["dark"]}"/>'
            f'<path d="M98 -4 Q112 -2 114 4 L98 4 Z" fill="{p["accent"]}"/>')


def p_warehouse(p):
    lines = "".join(f'<line x1="-50" y1="{20 + i * 16}" x2="50" y2="{20 + i * 16}" stroke="{p["light"]}" stroke-width="4"/>' for i in range(5))
    return (f'<polygon points="-110,-30 0,-90 110,-30" fill="{p["light"]}"/>'
            f'<rect x="-110" y="-30" width="220" height="130" fill="{p["main"]}"/>'
            f'<rect x="-80" y="-18" width="160" height="26" rx="4" fill="{p["accent"]}"/>'
            + text(0, 1, "WAREHOUSE", 17, p["white"], extra='letter-spacing="2"')
            + f'<rect x="-50" y="14" width="100" height="86" fill="{p["dark"]}"/>{lines}')


def p_factory(p):
    return (f'<rect x="-100" y="-120" width="26" height="90" fill="{p["light"]}"/>'
            f'<rect x="-60" y="-100" width="22" height="70" fill="{p["light"]}"/>'
            f'<polygon points="-110,-30 -50,-70 -50,-30 10,-70 10,-30 70,-70 70,-30 110,-30 110,100 -110,100" fill="{p["main"]}"/>'
            f'<rect x="-80" y="0" width="160" height="30" rx="4" fill="{p["accent"]}"/>'
            + text(0, 22, "FACTORY", 20, p["white"], extra='letter-spacing="3"')
            + f'<rect x="-30" y="45" width="60" height="55" fill="{p["dark"]}"/>'
            + "".join(f'<rect x="{x}" y="45" width="30" height="24" fill="{p["light"]}"/>' for x in (-90, 60)))


def p_coin(p):
    return (f'<ellipse cx="0" cy="10" rx="90" ry="90" fill="{p["dark"]}"/>'
            f'<circle r="88" fill="{rg(shade(p["main"], .45), p["dark"])}"/>'
            f'<circle r="66" fill="none" stroke="{shade(p["main"], .5)}" stroke-width="5"/>'
            f'<circle r="66" fill="none" stroke="{p["dark"]}" stroke-width="2" stroke-dasharray="4 6"/>'
            + text(0, 30, "৳", 84, p["ink"])
            + f'<path d="M-60 -40 Q-40 -70 -6 -76" fill="none" stroke="#FFFFFF" stroke-opacity="0.7" stroke-width="8" stroke-linecap="round"/>')


def p_money(p):
    return (f'<rect x="-120" y="-62" width="240" height="124" rx="10" fill="{p["main"]}"/>'
            f'<rect x="-104" y="-46" width="208" height="92" rx="6" fill="none" stroke="{p["light"]}" stroke-width="5"/>'
            f'<circle r="34" fill="{p["light"]}"/>' + text(0, 18, "৳", 48, p["ink"])
            + text(-80, -18, "100", 22, p["white"]) + text(80, 36, "100", 22, p["white"]))


def p_cushion(p):
    return (f'<rect x="-110" y="-70" width="220" height="140" rx="60" fill="{p["main"]}"/>'
            f'<rect x="-92" y="-54" width="184" height="108" rx="48" fill="{p["light"]}" fill-opacity="0.45"/>'
            f'<path d="M-70 0 Q0 -30 70 0" fill="none" stroke="{p["dark"]}" stroke-width="6" stroke-dasharray="10 10"/>'
            f'<circle cx="0" cy="-6" r="7" fill="{p["dark"]}"/>')


def p_cloud(p):
    return (f'<g fill="{p["main"]}"><circle cx="-60" cy="10" r="50"/><circle cx="0" cy="-20" r="66"/>'
            f'<circle cx="62" cy="8" r="52"/><rect x="-110" y="10" width="220" height="56" rx="28"/></g>'
            f'<path d="M-100 58 L100 58" stroke="{p["dark"]}" stroke-width="6" stroke-linecap="round"/>')


def p_blocks(p):
    def cube(x, y, c, letter):
        return (f'<rect x="{x}" y="{y}" width="80" height="80" rx="10" fill="{c}"/>'
                f'<rect x="{x + 8}" y="{y + 8}" width="64" height="64" rx="8" fill="#FFFFFF" fill-opacity="0.25"/>'
                + text(x + 40, y + 58, letter, 46, p["ink"]))
    return cube(-90, 10, p["main"], "A") + cube(10, 10, p["dark"], "B") + cube(-40, -72, p["light"], "C")


def p_magnifier(p):
    return (f'<line x1="40" y1="40" x2="100" y2="100" stroke="{p["dark"]}" stroke-width="26" stroke-linecap="round"/>'
            f'<circle cx="-10" cy="-10" r="72" fill="{p["light"]}" fill-opacity="0.55" stroke="{p["main"]}" stroke-width="16"/>'
            f'<path d="M-50 -30 Q-40 -50 -20 -56" fill="none" stroke="{p["accent"]}" stroke-width="8" stroke-linecap="round"/>')


def p_question(p):
    return f'<circle r="90" fill="{p["main"]}"/>' + text(0, 40, "?", 130, p["accent"])


def p_check(p):
    return (f'<circle r="90" fill="{p["main"]}"/><path d="M-42 2 L-10 34 L46 -30" fill="none" stroke="{p["ink"]}" '
            f'stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>')


def p_cross(p):
    return (f'<circle r="90" fill="{p["main"]}"/><path d="M-36 -36 L36 36 M36 -36 L-36 36" stroke="{p["ink"]}" '
            f'stroke-width="20" stroke-linecap="round"/>')


def p_tag(p, label="৳"):
    return (f'<path d="M-110 -50 L50 -50 L110 0 L50 50 L-110 50 Z" fill="{p["main"]}"/>'
            f'<circle cx="62" cy="0" r="12" fill="{p["dark"]}"/>'
            + text(-26, 26, label, 64 if len(label) < 4 else 40, p["ink"]))


def p_phone(p):
    return (f'<rect x="-60" y="-110" width="120" height="220" rx="18" fill="{p["main"]}"/>'
            f'<rect x="-50" y="-92" width="100" height="176" rx="8" fill="{p["light"]}"/>'
            f'<rect x="-36" y="-70" width="72" height="54" rx="6" fill="{p["accent"]}"/>'
            + "".join(f'<rect x="-36" y="{-2 + i * 20}" width="{72 - i * 14}" height="10" rx="5" fill="{p["white"]}"/>' for i in range(4))
            + f'<circle cx="0" cy="98" r="6" fill="{p["dark"]}"/>')


def p_cart(p):
    return (f'<path d="M-110 -70 L-80 -70 L-50 50 L80 50" fill="none" stroke="{p["accent"]}" stroke-width="12" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M-72 -40 L110 -40 L90 30 L-56 30 Z" fill="{p["main"]}"/>'
            + text(18, 8, "1688", 34, p["white"])
            + f'<circle cx="-34" cy="80" r="18" fill="{p["accent"]}"/><circle cx="60" cy="80" r="18" fill="{p["accent"]}"/>')


def p_shop(p):
    stripes = "".join(f'<path d="M{-110 + i * 44} -40 L{-66 + i * 44} -40 L{-66 + i * 44} -10 Q{-88 + i * 44} 8 {-110 + i * 44} -10 Z" '
                      f'fill="{p["light"] if i % 2 == 0 else p["accent"]}"/>' for i in range(5))
    return (f'<rect x="-100" y="-90" width="200" height="190" fill="{p["main"]}"/>'
            f'<rect x="-110" y="-100" width="220" height="60" rx="6" fill="{p["dark"]}"/>'
            + text(0, -60, "SHOP", 30, p["white"], extra='letter-spacing="4"') + stripes
            + f'<rect x="-80" y="20" width="70" height="80" fill="{p["dark"]}"/>'
            f'<rect x="10" y="20" width="70" height="50" fill="#BFE6FF"/>')


def p_lamp(p):
    return (f'<path d="M-70 -20 L-40 -100 L40 -100 L70 -20 Z" fill="{p["main"]}"/>'
            f'<rect x="-8" y="-20" width="16" height="96" fill="{p["accent"]}"/>'
            f'<ellipse cx="0" cy="84" rx="60" ry="14" fill="{p["accent"]}"/>'
            f'<path d="M-70 -20 L-110 70 L110 70 L70 -20 Z" fill="{p["light"]}" fill-opacity="0.25"/>')


def p_trophy(p):
    return (f'<path d="M-60 -90 L60 -90 L52 -10 Q0 40 -52 -10 Z" fill="{p["main"]}"/>'
            f'<path d="M-60 -76 Q-110 -76 -96 -36 Q-84 -10 -50 -20" fill="none" stroke="{p["main"]}" stroke-width="12"/>'
            f'<path d="M60 -76 Q110 -76 96 -36 Q84 -10 50 -20" fill="none" stroke="{p["main"]}" stroke-width="12"/>'
            f'<rect x="-12" y="18" width="24" height="44" fill="{p["dark"]}"/>'
            f'<rect x="-56" y="60" width="112" height="30" rx="6" fill="{p["dark"]}"/>'
            + text(0, -34, "★", 46, p["light"]))


def p_chair(p):
    return (f'<rect x="-60" y="-110" width="120" height="110" rx="20" fill="{p["main"]}"/>'
            f'<rect x="-80" y="0" width="160" height="34" rx="12" fill="{p["light"]}"/>'
            f'<rect x="-8" y="34" width="16" height="50" fill="{p["dark"]}"/>'
            f'<path d="M-60 100 L0 84 L60 100" fill="none" stroke="{p["dark"]}" stroke-width="10" stroke-linecap="round"/>')


def p_pan(p):
    return (f'<ellipse cx="-20" cy="20" rx="90" ry="34" fill="{p["dark"]}"/>'
            f'<ellipse cx="-20" cy="12" rx="90" ry="34" fill="{p["main"]}"/>'
            f'<ellipse cx="-20" cy="12" rx="70" ry="22" fill="{p["light"]}"/>'
            f'<rect x="66" y="0" width="70" height="16" rx="8" fill="{p["dark"]}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{p["accent"]}"/>' for x, y in ((-60, -40), (-20, -60), (20, -44), (-40, -80), (10, -90))))


PROPS = {
    "box": p_box, "container": p_container, "ship": p_ship, "plane": p_plane, "warehouse": p_warehouse,
    "factory": p_factory, "coin": p_coin, "money": p_money, "cushion": p_cushion, "cloud": p_cloud,
    "blocks": p_blocks, "magnifier": p_magnifier, "question": p_question, "check": p_check, "cross": p_cross,
    "tag": p_tag, "phone": p_phone, "cart": p_cart, "shop": p_shop, "lamp": p_lamp, "trophy": p_trophy,
    "chair": p_chair, "pan": p_pan,
}


def prop(name, x, y, s=1.0, rot=0, material=None, shadow=False, label=None):
    name = name if name in PROPS else "box"
    over = SHADOW if shadow else (MATERIALS.get(material) if material else None)
    p = pal(name, over)
    fn = PROPS[name]
    inner = fn(p, label) if (label is not None and name in ("box", "container", "tag")) else fn(p)
    if shadow:
        return T(x, y, s, rot, inner)
    return f'<g filter="url(#ds)">{T(x, y, s, rot, inner)}</g>'


# ---------------------------------------------------------------- animals

def a_ant(c="#D9532B"):
    body = rg(shade(c, .35), shade(c, -.35))
    legs = "".join(f'<path d="M{x} 6 Q{x + d / 2} 20 {x + d} 46" fill="none" stroke="{shade(c, -.4)}" stroke-width="6" stroke-linecap="round"/>'
                   for x, d in ((-40, -22), (-10, 0), (20, 18)))
    return (legs + f'<ellipse cx="-70" cy="0" rx="40" ry="30" fill="{body}"/><ellipse cx="-10" cy="-4" rx="26" ry="20" fill="{body}"/>'
            f'<circle cx="34" cy="-12" r="24" fill="{body}"/><circle cx="42" cy="-18" r="7" fill="#FFFFFF"/><circle cx="44" cy="-18" r="3" fill="#111"/>'
            f'<ellipse cx="-80" cy="-12" rx="14" ry="7" fill="#FFFFFF" fill-opacity="0.35"/>'
            f'<path d="M44 -32 Q60 -64 76 -60 M36 -34 Q44 -70 60 -72" fill="none" stroke="{shade(c, -.4)}" stroke-width="5" stroke-linecap="round"/>')


def a_eagle(c="#6B3E1F"):
    return (f'<path d="M0 0 Q-80 -70 -170 -40 Q-110 -30 -90 0 Q-130 10 -150 40 Q-60 20 0 20 Z" fill="{c}"/>'
            f'<path d="M0 0 Q80 -70 170 -40 Q110 -30 90 0 Q130 10 150 40 Q60 20 0 20 Z" fill="{c}"/>'
            f'<ellipse cx="0" cy="14" rx="30" ry="44" fill="{c}"/><circle cx="0" cy="-34" r="24" fill="#FFFFFF"/>'
            f'<path d="M8 -34 L30 -26 L8 -20 Z" fill="#FFB000"/><circle cx="4" cy="-38" r="4" fill="#0B1B3A"/>'
            f'<path d="M-14 56 L-14 76 M14 56 L14 76" stroke="#FFB000" stroke-width="6" stroke-linecap="round"/>')


def a_owl(c="#8A5A3B"):
    return (f'<ellipse cx="0" cy="20" rx="80" ry="96" fill="{c}"/><ellipse cx="0" cy="44" rx="50" ry="62" fill="#E2C9A6"/>'
            f'<path d="M-70 -50 L-56 -100 L-30 -66 Z M70 -50 L56 -100 L30 -66 Z" fill="{c}"/>'
            f'<circle cx="-30" cy="-30" r="30" fill="#FFFFFF"/><circle cx="30" cy="-30" r="30" fill="#FFFFFF"/>'
            f'<circle cx="-30" cy="-30" r="14" fill="#0B1B3A"/><circle cx="30" cy="-30" r="14" fill="#0B1B3A"/>'
            f'<circle cx="-30" cy="-30" r="34" fill="none" stroke="#0B1B3A" stroke-width="5"/>'
            f'<circle cx="30" cy="-30" r="34" fill="none" stroke="#0B1B3A" stroke-width="5"/>'
            f'<path d="M-6 -6 L0 8 L6 -6 Z" fill="#FFB000"/>')


def a_turtle(c="#2E8B57"):
    return (f'<ellipse cx="-104" cy="20" rx="34" ry="26" fill="#7BC47F"/><circle cx="-112" cy="12" r="5" fill="#0B1B3A"/>'
            f'<ellipse cx="-60" cy="54" rx="20" ry="14" fill="#7BC47F"/><ellipse cx="60" cy="54" rx="20" ry="14" fill="#7BC47F"/>'
            f'<path d="M-90 40 Q0 -100 90 40 Z" fill="{c}"/>'
            f'<path d="M-40 -6 L0 -30 L40 -6 L30 30 L-30 30 Z" fill="#256F46"/>'
            f'<path d="M96 30 L120 40 L96 46 Z" fill="#7BC47F"/>')


def a_snail(c="#C98F45"):
    return (f'<path d="M-120 60 Q-120 30 -80 30 L110 30 Q140 30 140 60 Z" fill="#B9A38A"/>'
            f'<path d="M110 30 L118 -30 M126 32 L140 -24" stroke="#B9A38A" stroke-width="8" stroke-linecap="round"/>'
            f'<circle cx="118" cy="-32" r="7" fill="#0B1B3A"/><circle cx="140" cy="-26" r="7" fill="#0B1B3A"/>')


def a_bee(c="#FFD60A"):
    return (f'<ellipse cx="-20" cy="-50" rx="46" ry="30" fill="#FFFFFF" fill-opacity="0.8"/>'
            f'<ellipse cx="30" cy="-54" rx="40" ry="26" fill="#FFFFFF" fill-opacity="0.8"/>'
            f'<ellipse cx="0" cy="0" rx="80" ry="50" fill="{c}"/>'
            f'<rect x="-30" y="-48" width="18" height="96" fill="#1E2126"/><rect x="10" y="-48" width="18" height="96" fill="#1E2126"/>'
            f'<circle cx="70" cy="-8" r="26" fill="#1E2126"/><circle cx="78" cy="-14" r="6" fill="#FFFFFF"/>'
            f'<path d="M-80 0 L-104 6 L-80 12 Z" fill="#1E2126"/>')


ANIMALS = {"ant": a_ant, "eagle": a_eagle, "owl": a_owl, "turtle": a_turtle, "snail": a_snail, "bee": a_bee}


# ---------------------------------------------------------------- helpers

def floor(y=470, w=900):
    return f'<ellipse cx="540" cy="{y}" rx="{w / 2}" ry="34" fill="url(#floorg)"/>'


GLOW = None  # when set, all glows use this colour


def glow(x, y, r, c, o=0.3):
    c = GLOW or c
    r = r * 0.7 if GLOW else r
    gid = f"g{abs(hash((x, y, r, c))) % 99999}"
    return (f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{c}" stop-opacity="{o}"/>'
            f'<stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})"/>')


def route(x1, y1, x2, y2, lift=120, c="#FFFFFF"):
    mx, my = (x1 + x2) / 2, min(y1, y2) - lift
    return (f'<path d="M{x1} {y1} Q{mx} {my} {x2} {y2}" fill="none" stroke="{c}" stroke-opacity="0.6" '
            f'stroke-width="5" stroke-dasharray="16 13" stroke-linecap="round"/>')


def pill(x, y, label, bg, fg="#FFFFFF", size=30):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;transform:translate(-50%,-50%);background:{bg};color:{fg};'
            f'font-size:{size}px;font-weight:800;padding:6px 22px;border-radius:999px;white-space:nowrap;'
            f'box-shadow:0 8px 20px rgba(0,0,0,.3)">{html.escape(label)}</div>')


def sparkles(pts, c="#FFFFFF"):
    return "".join(f'<path transform="translate({x} {y}) scale({s})" d="M0 -20 L5 -5 L20 0 L5 5 L0 20 L-5 5 L-20 0 L-5 -5 Z" fill="{c}"/>'
                   for x, y, s in pts)


# ---------------------------------------------------------------- styles

def s_exaggeration(a, acc):
    mode = a.get("mode", "stream")
    src, eff = a.get("source", "box"), a.get("effect", "coin")
    out, ov = [glow(540, 300, 420, acc, 0.25), floor(500, 640)], ""
    if mode == "giant":
        out.append(prop(src, 250, 400, 0.55))
        out.append(prop(eff, 650, 280, 2.3))
        out.append('<path d="M330 400 L420 360" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="10 10"/>')
    elif mode == "lift":
        out.append(prop(src, 540, 430, 0.6))
        out.append(prop(eff, 540, 190, 1.9))
        out += [f'<path d="M{x} 320 L{x} 370" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-opacity="0.7"/>' for x in (470, 540, 610)]
    else:  # stream: small source erupts into a fountain of the effect
        rnd = random.Random(a.get("seed", 7))
        out.append(f'<path d="M500 380 L330 60 L750 60 L580 380 Z" fill="{GLOW or acc}" fill-opacity="0.16"/>')
        items = []
        for i in range(26):
            t = rnd.random()
            spread = 60 + t * 300
            x = 540 + rnd.uniform(-1, 1) * spread
            y = 360 - t * 270 + rnd.uniform(-15, 15)
            items.append((y, x, 0.24 + t * 0.32, rnd.uniform(-35, 35)))
        for y, x, sc, r in sorted(items, reverse=True):
            out.append(prop(eff, x, y, sc, r))
        out.append(prop(src, 540, 420, 0.9))
    if a.get("label"):
        ov += pill(540, 530, a["label"], acc, "#0B1B3A")
    return "".join(out), ov


def s_animal(a, acc):
    an, obj = a.get("animal", "ant"), a.get("object", "container")
    draw = ANIMALS.get(an, a_ant)
    out, ov = [glow(540, 300, 420, acc, 0.22)], ""
    if an == "eagle":
        out.append(route(120, 420, 960, 400, 260))
        out.append(T(540, 170, 1.1, 0, draw()))
        out.append('<path d="M525 255 L520 290 M555 255 L560 290" stroke="#FFB000" stroke-width="5"/>')
        out.append(prop(obj, 540, 360, 0.85))
    elif an == "owl":
        out.append(floor(500, 760))
        out.append(T(330, 320, 1.25, 0, draw()))
        out.append(prop(obj, 740, 360, 1.1))
        out.append(prop("magnifier", 660, 300, 0.9, -20))
    elif an in ("turtle", "snail"):
        out.append(floor(480, 700))
        if an == "snail":
            out.append(T(540, 420, 1.4, 0, draw()))
            out.append(prop(obj, 520, 300, 1.1))
        else:
            out.append(T(540, 400, 1.6, 0, draw()))
            out.append(prop(obj, 540, 240, 0.9))
    elif an == "bee":
        out.append(route(160, 300, 920, 280, 160))
        out.append(T(540, 200, 1.1, 0, draw()))
        out.append(f'<path d="M540 250 L540 300" stroke="#1E2126" stroke-width="4"/>')
        out.append(prop(obj, 540, 380, 0.7))
    else:  # ant carrying something far bigger than itself
        out.append(floor(490, 720))
        out.append(prop(obj, 560, 230, 1.55, -4))
        out.append(T(560, 440, 1.7, 0, draw()))
    if a.get("label"):
        ov += pill(540, 530, a["label"], acc, "#0B1B3A")
    return "".join(out), ov


def s_material(a, acc):
    obj, mat = a.get("object", "box"), a.get("material", "gold")
    out, ov = [glow(540, 290, 380, MATERIALS.get(mat, MATERIALS["gold"])["main"], 0.35), floor(490, 560)], ""
    s = a.get("scale", 1.9)
    if mat in ("cloud", "cotton"):
        out.append('<g filter="url(#soft)">' + prop(obj, 540, 300, s, material=mat) + "</g>")
        out.insert(0, '<defs><filter id="soft"><feGaussianBlur stdDeviation="2"/></filter></defs>')
        out += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" fill-opacity="0.9"/>' for x, y, r in
                ((350, 380, 40), (400, 410, 30), (720, 390, 44), (680, 420, 30), (540, 440, 36))]
    else:
        if mat == "glass":
            out += [prop("box", x, 330, 0.55) for x in (440, 540, 640)]
        out.append(f'<g opacity="{0.72 if mat == "glass" else 1}">' + prop(obj, 540, 300, s, material=mat) + "</g>")
    if mat == "gold":
        out.append(sparkles([(380, 160, 1.4), (720, 140, 1.1), (760, 330, 0.9), (330, 340, 0.8)], "#FFF6D0"))
    elif mat in ("glass", "ice"):
        out.append('<path d="M420 140 L470 140 L360 420 L310 420 Z M500 140 L520 140 L410 420 L390 420 Z" fill="#FFFFFF" fill-opacity="0.35"/>')
        if mat == "ice":
            out += [f'<path transform="translate({x} {y})" d="M0 -14 Q10 0 0 10 Q-10 0 0 -14 Z" fill="#AEEBFF"/>' for x, y in ((420, 470), (650, 480), (560, 500))]
    elif mat == "steel":
        out += [f'<circle cx="{x}" cy="{y}" r="7" fill="#6B7686"/>' for x, y in ((380, 200), (700, 200), (380, 400), (700, 400))]
    elif mat == "feather":
        out += [T(x, y, 0.6, r, '<path d="M0 -60 Q30 -20 0 60 Q-30 -20 0 -60 Z" fill="#FFFFFF"/><path d="M0 -60 L0 70" stroke="#C3CAD8" stroke-width="3"/>')
                for x, y, r in ((300, 160, -30), (790, 200, 25), (760, 430, -10))]
    if a.get("label"):
        ov += pill(540, 530, a["label"], acc, "#0B1B3A")
    return "".join(out), ov


def shape_points(shape, n):
    pts = []
    if shape == "check":
        a, b, c = (270, 280), (450, 450), (830, 70)
        n1 = n // 3
        pts = [(a[0] + (b[0] - a[0]) * i / n1, a[1] + (b[1] - a[1]) * i / n1) for i in range(n1)]
        pts += [(b[0] + (c[0] - b[0]) * i / (n - n1 - 1), b[1] + (c[1] - b[1]) * i / (n - n1 - 1)) for i in range(n - n1)]
    elif shape == "heart":
        for i in range(n):
            t = 2 * math.pi * i / n
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((540 + x * 14, 250 - y * 14))
    elif shape == "arrow":
        shaft = n * 2 // 3
        pts = [(540, 470 - i * 380 / shaft) for i in range(shaft)]
        head = n - shaft
        for i in range(head):
            k = (i // 2 + 1) / (head / 2)
            pts.append((540 + (-1 if i % 2 == 0 else 1) * 150 * k, 90 + 150 * k))
    elif shape == "graph":
        knots = [(200, 440), (380, 330), (520, 380), (720, 200), (880, 80)]
        segs = len(knots) - 1
        for i in range(n):
            t = i / (n - 1) * segs
            k = min(int(t), segs - 1)
            f = t - k
            (x1, y1), (x2, y2) = knots[k], knots[k + 1]
            pts.append((x1 + (x2 - x1) * f, y1 + (y2 - y1) * f))
    elif shape == "circle":
        pts = [(540 + 210 * math.cos(2 * math.pi * i / n), 270 + 210 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    elif shape == "taka":
        # ৳-like mark built from strokes: stem, curl, crossbar
        stem = [(470, 120 + i * 32) for i in range(10)]
        bowl = [(470 + 120 * math.sin(math.pi * i / 9), 360 + 90 * (1 - math.cos(math.pi * i / 9)) - 90) for i in range(10)]
        bar = [(380 + i * 40, 190) for i in range(6)]
        top = [(470 - 60 * math.cos(math.pi * i / 5), 120 - 50 * math.sin(math.pi * i / 5)) for i in range(5)]
        pts = (stem + bowl + bar + top)[:n] if n < 31 else stem + bowl + bar + top
    return pts


def s_shape(a, acc):
    unit, shape = a.get("unit", "box"), a.get("shape", "check")
    out, ov = [glow(540, 270, 420, acc, 0.22)], ""
    if shape == "stairs":
        for step in range(5):
            for k in range(step + 1):
                out.append(prop(unit, 220 + step * 150, 470 - k * 85, 0.42))
        out.append(T(860, 30, 0.5, 0, '<path d="M0 0 L0 80 L60 40 Z" fill="#FFD60A"/><rect x="-6" y="-10" width="8" height="140" fill="#FFFFFF"/>'))
    else:
        n = a.get("count", {"check": 18, "heart": 26, "arrow": 20, "graph": 18, "circle": 18, "taka": 31}.get(shape, 18))
        rnd = random.Random(3)
        for x, y in shape_points(shape, n):
            out.append(prop(unit, x, y, a.get("unit_scale", 0.36), rnd.uniform(-12, 12)))
    if a.get("label"):
        ov += pill(540, 530, a["label"], acc, "#0B1B3A")
    return "".join(out), ov


def s_benefit(a, acc):
    obj = a.get("object", "box")
    calls = (a.get("callouts") or [])[:4]
    out, ov = [glow(540, 270, 330, acc, 0.35), floor(470, 420), prop(obj, 540, 280, a.get("scale", 1.55))], ""
    spots = [(70, 70, 360, 190), (70, 300, 360, 330), (1010, 70, 720, 190), (1010, 300, 720, 330)]
    for i, label in enumerate(calls):
        bx, by, ax, ay = spots[i]
        left = bx < 540
        out.append(f'<path d="M{ax} {ay} L{(ax + (-60 if left else 60))} {by + 40}" stroke="{acc}" stroke-width="5" fill="none"/>'
                   f'<circle cx="{ax}" cy="{ay}" r="10" fill="{acc}"/>')
        align = "left:%dpx" % bx if left else "right:%dpx" % (ART_W - bx)
        ov += (f'<div style="position:absolute;{align};top:{by}px;max-width:300px;background:#FFFFFF;color:#0B1B3A;'
               f'border-left:10px solid {acc};border-radius:14px;padding:12px 18px;font-size:30px;font-weight:800;'
               f'line-height:1.25;box-shadow:0 10px 24px rgba(0,0,0,.35)">✓ {html.escape(label)}</div>')
    return "".join(out), ov


def arrange(objs, cx, mode):
    out = []
    n = len(objs)
    if mode == "messy":
        rnd = random.Random(11)
        for i in range(max(n, 6)):
            o = objs[i % n]
            out.append(prop(o, cx + rnd.uniform(-170, 170), rnd.uniform(200, 440), rnd.uniform(0.38, 0.6), rnd.uniform(-35, 35)))
    elif n == 1:
        out.append(prop(objs[0], cx, 320, 1.25))
    else:
        for i, o in enumerate(objs[:3]):
            dx = (i - (min(n, 3) - 1) / 2) * 150
            out.append(prop(o, cx + dx, 330 + (i % 2) * 20, 0.62))
    return "".join(out)


def s_contrast(a, acc):
    L, R = a.get("left", {}), a.get("right", {})
    out = ['<defs><filter id="gray"><feColorMatrix type="saturate" values="0.05"/></filter></defs>',
           '<rect x="40" y="50" width="500" height="470" fill="#000" fill-opacity="0.22"/>',
           f'<rect x="540" y="50" width="500" height="470" fill="#FFFFFF" fill-opacity="0.06"/>',
           '<line x1="540" y1="60" x2="540" y2="520" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="14 12"/>',
           '<g filter="url(#gray)" opacity="0.8">' + arrange(L.get("objects", ["box"]), 270, L.get("arrange", "messy")) + "</g>",
           arrange(R.get("objects", ["box"]), 810, R.get("arrange", "neat")),
           prop("cross", 270, 470, 0.38), prop("check", 810, 470, 0.38)]
    ov = pill(270, 60, L.get("label", "আগে"), "#5B6B8C") + pill(810, 60, R.get("label", "এখন"), "#1FA463")
    return "".join(out), ov


def s_shadow(a, acc):
    obj, sh = a.get("object", "box"), a.get("shadow", "ship")
    out = [glow(150, 120, 360, "#FFF3C4", 0.45),
           '<rect x="40" y="470" width="1000" height="50" fill="#000" fill-opacity="0.18"/>',
           f'<polygon points="330,470 420,470 1000,470 900,470" fill="#000" fill-opacity="0.2"/>',
           f'<path d="M340 472 L980 300 L980 472 Z" fill="#000" fill-opacity="0.18"/>',
           '<g opacity="0.42">' + prop(sh, 700, 270, a.get("shadow_scale", 2.1), shadow=True) + "</g>",
           prop(obj, 330, 400, a.get("scale", 0.8))]
    ov = pill(540, 530, a["label"], acc, "#0B1B3A") if a.get("label") else ""
    return "".join(out), ov


FUNCS = {"exaggeration": s_exaggeration, "animal": s_animal, "material": s_material, "shape": s_shape,
         "benefit": s_benefit, "contrast": s_contrast, "shadow": s_shadow}


def render(style, spec, accent):
    if style not in FUNCS:
        raise ValueError(f"style must be one of {STYLES}, got {style!r}")
    _DEFS.clear()
    body, ov = FUNCS[style](spec or {}, accent)
    stage = ""
    return f"<defs>{BASE_DEFS}{''.join(_DEFS.values())}</defs>{stage}{body}", ov
