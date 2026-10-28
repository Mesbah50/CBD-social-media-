"""CBD import graphics kit (flat, brand colours) — from the owner's Brand Post Guide PDF.

Each function returns SVG markup drawn in a 400x300 box. Used as the fallback visual
inside the photo slot when the Canva photo cannot be made.
"""
BLUE = "#05358B"
RED = "#E40715"
GRAY = "#F0F0F2"
WEDGE = "#5274A4"
WHITE = "#FFFFFF"


def ship(dark=False):
    hull = WHITE if dark else BLUE
    sea = "#3A5E9A" if dark else "#A9B8D1"
    return f'''
<rect x="0" y="232" width="400" height="68" fill="{sea}"/>
<path d="M0 240 Q 50 222 100 236 T 200 236 T 300 236 T 400 232 V300 H0 Z" fill="{sea}"/>
<rect x="88" y="130" width="40" height="34" fill="{RED}"/><rect x="132" y="130" width="40" height="34" fill="{WEDGE}"/>
<rect x="176" y="130" width="40" height="34" fill="{RED}"/><rect x="220" y="130" width="40" height="34" fill="{WEDGE if not dark else GRAY}"/>
<rect x="132" y="92" width="40" height="34" fill="{WEDGE}"/><rect x="176" y="92" width="40" height="34" fill="{BLUE if not dark else GRAY}"/>
<rect x="272" y="96" width="44" height="68" fill="{GRAY if not dark else WHITE}"/><rect x="282" y="110" width="24" height="9" fill="{BLUE}"/>
<rect x="288" y="74" width="10" height="20" fill="{RED}"/>
<path d="M50 166 H350 L326 236 H76 Z" fill="{hull}"/>
<rect x="66" y="184" width="270" height="7" fill="{RED}"/>'''


def containers(dark=False):
    def box(x, y, c):
        ribs = "".join(f'<rect x="{x + 8 + i * 12}" y="{y + 6}" width="4" height="{58}" fill="#000" fill-opacity="0.12"/>' for i in range(9))
        return f'<rect x="{x}" y="{y}" width="120" height="70" fill="{c}"/>{ribs}'
    return (box(140, 40, BLUE if not dark else GRAY) + box(80, 112, RED) + box(202, 112, WEDGE) +
            box(80, 184, BLUE if not dark else WHITE) + box(202, 184, RED) +
            f'<rect x="60" y="256" width="282" height="5" fill="{WEDGE}"/>')


def plane(dark=True):
    c = WHITE if dark else BLUE
    dots = "".join(f'<circle cx="{40 + i * 14}" cy="{250 - (i ** 1.55)}" r="3.4" fill="{c}"/>' for i in range(14))
    return f'''{dots}
<g transform="translate(250 110) rotate(-28)" fill="{c}">
 <path d="M-90 -9 H70 Q100 -9 100 0 Q100 9 70 9 H-90 Z"/>
 <path d="M-10 0 L-55 -78 L-30 -78 L30 0 Z"/><path d="M-10 0 L-55 78 L-30 78 L30 0 Z"/>
 <path d="M-82 0 L-100 -34 L-86 -34 L-62 0 Z"/><path d="M-82 0 L-100 34 L-86 34 L-62 0 Z"/></g>
<rect x="60" y="232" width="56" height="44" fill="{WEDGE if dark else GRAY}"/><rect x="82" y="232" width="10" height="44" fill="{WHITE}"/>
<rect x="290" y="210" width="76" height="62" fill="{RED}"/><rect x="322" y="210" width="12" height="62" fill="{WHITE}"/>'''


def route(dark=True):
    c = WHITE if dark else BLUE
    pin = lambda x, y, col: (f'<g transform="translate({x} {y})"><path d="M0 0 C -26 -30 -26 -66 0 -66 C 26 -66 26 -30 0 0 Z" fill="{col}"/>'
                             f'<circle cx="0" cy="-42" r="10" fill="{BLUE if col != BLUE else WHITE}"/></g>')
    dots = "".join(f'<circle cx="{70 + i * 16}" cy="{200 - 90 * (1 - ((i - 9) / 9) ** 2)}" r="3.2" fill="{c}"/>' for i in range(19))
    return (dots + pin(62, 228, c) + pin(352, 120, RED) +
            f'<text x="62" y="268" text-anchor="middle" font-family="P" font-weight="700" font-size="22" letter-spacing="2" fill="{c}">CHINA</text>'
            f'<text x="338" y="156" text-anchor="middle" font-family="P" font-weight="700" font-size="20" letter-spacing="1" fill="{c}">BANGLADESH</text>'
            f'<g transform="translate(214 114) rotate(4) scale(0.42)" fill="{c}"><path d="M-90 -9 H70 Q100 -9 100 0 Q100 9 70 9 H-90 Z"/>'
            '<path d="M-10 0 L-55 -78 L-30 -78 L30 0 Z"/><path d="M-10 0 L-55 78 L-30 78 L30 0 Z"/></g>')


def cartons(dark=False):
    return f'''
<rect x="110" y="70" width="96" height="70" fill="{BLUE if not dark else GRAY}"/><rect x="150" y="70" width="18" height="70" fill="{RED}"/>
<rect x="76" y="140" width="146" height="116" fill="{WEDGE}"/><rect x="140" y="140" width="18" height="116" fill="{RED}"/>
<rect x="236" y="186" width="92" height="70" fill="{BLUE if not dark else WHITE}"/><rect x="274" y="186" width="16" height="70" fill="{RED}"/>
<rect x="60" y="256" width="282" height="5" fill="{WEDGE}"/>'''


def truck(dark=False):
    body = BLUE if not dark else WHITE
    return f'''
<rect x="60" y="80" width="190" height="120" rx="12" fill="{body}"/><rect x="60" y="126" width="190" height="12" fill="{RED}"/>
<path d="M256 116 H316 L350 160 V200 H256 Z" fill="{RED}"/><path d="M272 130 H310 L332 158 H272 Z" fill="{WHITE}"/>
<circle cx="116" cy="212" r="28" fill="{WEDGE}"/><circle cx="116" cy="212" r="15" fill="{WHITE}"/>
<circle cx="304" cy="212" r="28" fill="{WEDGE}"/><circle cx="304" cy="212" r="15" fill="{WHITE}"/>
<path d="M40 262 H370" stroke="{WEDGE}" stroke-width="5" stroke-dasharray="22 12"/>'''


def warehouse(dark=True):
    return f'''
<path d="M70 120 L200 40 L330 120 Z" fill="{RED}"/>
<rect x="96" y="120" width="208" height="130" fill="{WHITE if dark else GRAY}"/>
<rect x="114" y="140" width="34" height="22" fill="{WEDGE}"/><rect x="252" y="140" width="34" height="22" fill="{WEDGE}"/>
<rect x="160" y="170" width="80" height="80" fill="{BLUE}"/>
''' + "".join(f'<rect x="166" y="{180 + i * 17}" width="68" height="9" fill="{WHITE}" fill-opacity="0.85"/>' for i in range(4)) + \
        f'<rect x="60" y="250" width="280" height="5" fill="{WEDGE}"/>'


ITEMS = {"ship": ship, "containers": containers, "plane": plane, "route": route,
         "cartons": cartons, "truck": truck, "warehouse": warehouse}


def svg(name, w, h, dark, tile=None):
    """Kit drawing centred in a w x h slot, on a tile of the opposite tone."""
    fn = ITEMS.get(name, ITEMS["containers"])
    tile = tile or (BLUE if dark else GRAY)
    s = min(w / 400, h / 300) * 0.92
    tx, ty = (w - 400 * s) / 2, (h - 300 * s) / 2
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{tile}"/>'
            f'<g transform="translate({tx:.1f} {ty:.1f}) scale({s:.3f})">{fn(dark)}</g></svg>')
