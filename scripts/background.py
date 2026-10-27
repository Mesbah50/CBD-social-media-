"""CBD brand background (the only background allowed): warm off-white, dot grid,
soft centre glow and scattered light-blue rounded squares. Taken from the owner's reference."""
import random

BG = "#F7F3F2"
DOT = "#D8D3D2"
SQUARES = ["#D3D9F9", "#DDE2F6", "#E5E8F7", "#D4DEF7", "#E2EAF7", "#DEE4F2"]


def svg(w=1080, h=1080, seed=5):
    rnd = random.Random(seed)
    step = 46
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{DOT}"/>'
                   for y in range(step // 2, h, step) for x in range(step // 2, w, step))
    # squares sit near the edges so the centre stays clean
    spots = [(0.07, 0.17), (0.88, 0.13), (0.49, 0.14), (0.91, 0.24), (0.05, 0.31), (0.92, 0.34),
             (0.12, 0.39), (0.85, 0.50), (0.06, 0.57), (0.30, 0.58), (0.61, 0.54), (0.73, 0.62),
             (0.08, 0.73), (0.94, 0.70), (0.36, 0.86), (0.66, 0.80), (0.86, 0.90), (0.18, 0.93)]
    sq = []
    for i, (fx, fy) in enumerate(spots):
        s = rnd.choice([18, 24, 30, 38, 46, 56])
        x, y = fx * w, fy * h
        sq.append(f'<rect x="{x - s / 2:.0f}" y="{y - s / 2:.0f}" width="{s}" height="{s}" rx="{s * 0.22:.0f}" '
                  f'fill="{SQUARES[i % len(SQUARES)]}" fill-opacity="{rnd.uniform(0.6, 0.95):.2f}" '
                  f'transform="rotate({rnd.uniform(-14, 14):.0f} {x:.0f} {y:.0f})"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs><radialGradient id="bgglow" cx="0.5" cy="0.55" r="0.42">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/><stop offset="0.6" stop-color="#FFFFFF" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{dots}'
            f'<rect width="{w}" height="{h}" fill="url(#bgglow)"/>{"".join(sq)}</svg>')


if __name__ == "__main__":
    import pathlib, sys
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "brand/background.svg")
    out.write_text(svg(), encoding="utf-8")
    print("wrote", out)
