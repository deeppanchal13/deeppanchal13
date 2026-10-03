#!/usr/bin/env python3
"""
Generates every custom pixel-art SVG used by README.md into ../assets/.
Edit the COLORS / SECTIONS below, run `python tools/generate_assets.py`, commit the result.
No dependencies (pure Python 3).
"""
import os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

# ---------------- COLORS (change these to re-theme everything) ----------------
BG    = "#070b07"   # page / banner background
PANEL = "#0b120b"   # boxed sections
LINE  = "#1f3a1f"   # thin borders + grid
GREEN = "#00ff66"   # neon accent
DIM   = "#0c5c2c"   # dark green (glitch layer)
TEXT  = "#e6efe6"   # main light text
MUTE  = "#6f8a6f"   # muted text
MONO  = "'Courier New', Consolas, 'DejaVu Sans Mono', monospace"

# ---------------- 5x7 PIXEL FONT ----------------
F = {
 "A":"01110 10001 10001 11111 10001 10001 10001","B":"11110 10001 10001 11110 10001 10001 11110",
 "C":"01110 10001 10000 10000 10000 10001 01110","D":"11110 10001 10001 10001 10001 10001 11110",
 "E":"11111 10000 10000 11110 10000 10000 11111","F":"11111 10000 10000 11110 10000 10000 10000",
 "G":"01110 10001 10000 10111 10001 10001 01111","H":"10001 10001 10001 11111 10001 10001 10001",
 "I":"01110 00100 00100 00100 00100 00100 01110","J":"00111 00010 00010 00010 00010 10010 01100",
 "K":"10001 10010 10100 11000 10100 10010 10001","L":"10000 10000 10000 10000 10000 10000 11111",
 "M":"10001 11011 10101 10101 10001 10001 10001","N":"10001 11001 10101 10011 10001 10001 10001",
 "O":"01110 10001 10001 10001 10001 10001 01110","P":"11110 10001 10001 11110 10000 10000 10000",
 "Q":"01110 10001 10001 10001 10101 10010 01101","R":"11110 10001 10001 11110 10100 10010 10001",
 "S":"01111 10000 10000 01110 00001 00001 11110","T":"11111 00100 00100 00100 00100 00100 00100",
 "U":"10001 10001 10001 10001 10001 10001 01110","V":"10001 10001 10001 10001 10001 01010 00100",
 "W":"10001 10001 10001 10101 10101 11011 10001","X":"10001 01010 00100 00100 00100 01010 10001",
 "Y":"10001 10001 01010 00100 00100 00100 00100","Z":"11111 00001 00010 00100 01000 10000 11111",
 "0":"01110 10001 10011 10101 11001 10001 01110","1":"00100 01100 00100 00100 00100 00100 01110",
 "2":"01110 10001 00001 00110 01000 10000 11111","3":"11110 00001 00001 01110 00001 00001 11110",
 "-":"00000 00000 00000 11111 00000 00000 00000"," ":"00000 00000 00000 00000 00000 00000 00000",
 "/":"00001 00010 00010 00100 01000 01000 10000",".":"00000 00000 00000 00000 00000 01100 01100",
}


def text_w(t, s):
    return len(t) * 6 * s - s


def pix_path(t, x, y, s):
    d = []
    for i, ch in enumerate(t.upper()):
        rows = F.get(ch, F[" "]).split()
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                if v == "1":
                    d.append(f"M{x + (i*6 + c)*s} {y + r*s}h{s}v{s}h-{s}z")
    return "".join(d)


def pix(t, x, y, s, fill, extra=""):
    return f'<path d="{pix_path(t, x, y, s)}" fill="{fill}" {extra}/>'


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges" role="img">\n<defs>{defs}</defs>\n{body}\n</svg>\n')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def noise(x0, x1, y0, y1, size, seed, dens_fn, blink=0.12):
    rnd = random.Random(seed)
    out = []
    for x in range(x0, x1, size):
        for y in range(y0, y1, size):
            p = dens_fn((x - x0) / max(1, (x1 - x0)))
            if rnd.random() < p:
                col = rnd.choice([GREEN, GREEN, DIM, DIM, LINE, TEXT])
                op = round(rnd.uniform(0.25, 0.9), 2)
                if rnd.random() < blink:
                    dur = round(rnd.uniform(1.2, 3.5), 1)
                    out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{col}" opacity="{op}">'
                               f'<animate attributeName="opacity" values="{op};0;{op}" dur="{dur}s" repeatCount="indefinite"/></rect>')
                else:
                    out.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{col}" opacity="{op}"/>')
    return "\n".join(out)


GRID_DEFS = (f'<pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">'
             f'<path d="M10 0H0V10" fill="none" stroke="{LINE}" stroke-width="0.5" opacity="0.55"/></pattern>'
             f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
             f'<rect width="4" height="1" fill="#000" opacity="0.28"/></pattern>')


def chip(x, y, s, color):
    """small original pixel 'microchip' sprite, 9x9 grid"""
    cells = []
    for r in range(9):
        for c in range(9):
            body = 1 <= r <= 7 and 1 <= c <= 7
            hollow = 3 <= r <= 5 and 3 <= c <= 5
            pin = (r in (0, 8) and c in (2, 4, 6)) or (c in (0, 8) and r in (2, 4, 6))
            if (body and not hollow) or pin or (r == 4 and c == 4):
                cells.append(f"M{x + c*s} {y + r*s}h{s}v{s}h-{s}z")
    return f'<path d="{"".join(cells)}" fill="{color}"/>'


# ================= HEADER =================
def header():
    W, H = 830, 310
    name = "DEEP PANCHAL"
    s = 10
    nx = (W - text_w(name, s)) // 2
    ny = 88
    kt = "0;0.03;0.06;0.09;0.62;0.65;0.68;0.71;1"
    glitch_a = "0,0;-8,0;6,0;0,0;0,0;7,-2;-5,2;0,0;0,0"
    glitch_b = "0,0;5,2;-6,0;0,0;0,0;-7,2;4,-2;0,0;0,0"
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
         noise(0, W, 30, 62, 10, 7, lambda t: 0.5 * abs(2 * t - 1) ** 2.2 + 0.03),
         noise(0, W, 262, 310, 10, 11, lambda t: 0.55 * abs(2 * t - 1) ** 1.8 + 0.04)]
    # terminal bar
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="28" fill="{PANEL}" stroke="{LINE}"/>')
    for i, c in enumerate([GREEN, DIM, LINE]):
        b.append(f'<rect x="{12 + i*16}" y="9" width="10" height="10" fill="{c}"/>')
    b.append(f'<text x="70" y="19" font-family="{MONO}" font-size="12" fill="{MUTE}">deeppanchal13@github:~/profile $ ./run --whoami</text>')
    b.append(f'<text x="{W-14}" y="19" text-anchor="end" font-family="{MONO}" font-size="12" fill="{GREEN}">[ ONLINE ]'
             f'<animate attributeName="opacity" values="1;1;0.3;1" dur="2.4s" repeatCount="indefinite"/></text>')
    # sprites
    b.append(chip(16, 90, 3, GREEN))
    b.append(chip(W - 16 - 27, 90, 3, GREEN))
    # glitch layers behind main name
    b.append(f'<g>{pix(name, nx, ny, s, DIM)}<animateTransform attributeName="transform" type="translate" calcMode="discrete" '
             f'values="{glitch_a}" keyTimes="{kt}" dur="4.6s" repeatCount="indefinite"/></g>')
    b.append(f'<g opacity="0.55">{pix(name, nx, ny, s, MUTE)}<animateTransform attributeName="transform" type="translate" calcMode="discrete" '
             f'values="{glitch_b}" keyTimes="{kt}" dur="4.6s" repeatCount="indefinite"/></g>')
    b.append(pix(name, nx + 4, ny + 4, s, GREEN))   # hard pixel shadow
    b.append(pix(name, nx, ny, s, TEXT))             # main
    # tear band
    b.append(f'<rect x="0" y="100" width="{W}" height="5" fill="{BG}" opacity="0">'
             f'<animate attributeName="y" calcMode="discrete" values="100;100;118;92;100" keyTimes="0;0.6;0.7;0.78;1" dur="4.6s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" calcMode="discrete" values="0;0;1;1;0" keyTimes="0;0.6;0.7;0.78;1" dur="4.6s" repeatCount="indefinite"/></rect>')
    # subtitle
    b.append(f'<text x="{W//2}" y="196" text-anchor="middle" font-family="{MONO}" font-size="17" letter-spacing="2" font-weight="bold" fill="{GREEN}">'
             f'FULL-STACK / FRONTEND DEVELOPER • CSE STUDENT • BUILDER</text>')
    b.append(f'<rect x="60" y="214" width="{W-120}" height="1" fill="{LINE}"/>')
    for i in range(0, W - 120, 20):
        b.append(f'<rect x="{60 + i}" y="212" width="4" height="5" fill="{LINE}"/>')
    prompt = "&gt; B.Tech CSE · 2nd year · building real-world software"
    plen = len("> B.Tech CSE · 2nd year · building real-world software")
    b.append(f'<text x="60" y="246" font-family="{MONO}" font-size="15" fill="{TEXT}">{prompt}</text>')
    cx = 60 + int(plen * 9.02) + 6
    b.append(f'<rect x="{cx}" y="233" width="9" height="15" fill="{GREEN}"><animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="{LINE}"/>')
    save("header.svg", svg(W, H, "\n".join(b), GRID_DEFS))


# ================= SECTION HEADINGS =================
SECTIONS = [("h-about.svg", "ABOUT ME"), ("h-what.svg", "WHAT I DO"), ("h-vision.svg", "VISION"),
            ("h-beyond.svg", "BEYOND CODE"), ("h-achievements.svg", "ACHIEVEMENTS"), ("h-projects.svg", "PROJECTS"),
            ("h-skills.svg", "SKILL SET"), ("h-activity.svg", "GITHUB ACTIVITY"), ("h-connect.svg", "CONNECT")]


def heading(fname, label, idx):
    W, H, s = 830, 48, 3
    tw = text_w(label, s)
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="{PANEL}" stroke="{LINE}"/>']
    for i in range(2):
        for j in range(2):
            b.append(f'<rect x="{14 + i*7}" y="{13 + j*7}" width="6" height="6" fill="{GREEN if (i+j)%2==0 else DIM}"/>')
    b.append(pix(label, 40, 14, s, TEXT))
    lx = 40 + tw + 18
    b.append(f'<text x="{lx}" y="29" font-family="{MONO}" font-size="11" fill="{MUTE}">// SEC_{idx:02d}</text>')
    nx0 = lx + 80
    b.append(noise(nx0, W - 12, 6, 42, 6, 100 + idx, lambda t: 0.04 + 0.6 * t ** 1.5, blink=0.15))
    save(fname, svg(W, H, "\n".join(b)))


# ================= BEYOND CODE =================
def beyond():
    W, tw, th, gap, s = 830, 197, 84, 14, 3
    items = [("CRICKET", "// field"), ("CHESS", "// board"), ("BADMINTON", "// court"), ("VOLLEYBALL", "// team sport"),
             ("MUSIC", "// playlist"), ("BHAJANS", "// devotional"), ("GARBA", "// dance")]
    H = th * 2 + gap
    b = []
    for k in range(8):
        x = (k % 4) * (tw + gap)
        y = (k // 4) * (th + gap)
        b.append(f'<rect x="{x+0.5}" y="{y+0.5}" width="{tw-1}" height="{th-1}" fill="{PANEL}" stroke="{LINE}"/>')
        b.append(f'<rect x="{x+10}" y="{y+10}" width="6" height="6" fill="{GREEN}"/>')
        b.append(f'<text x="{tw+x-10}" y="{y+17}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTE}">{k+1:02d}</text>')
        if k < 7:
            lab, sub = items[k]
            b.append(pix(lab, x + 10, y + 32, s, TEXT))
            b.append(f'<text x="{x+10}" y="{y+th-12}" font-family="{MONO}" font-size="12" fill="{GREEN}">{sub}</text>')
        else:
            b.append(pix("ENGLISH", x + 10, y + 32, s, GREEN))
            b.append(f'<text x="{x+10}" y="{y+th-22}" font-family="{MONO}" font-size="11" fill="{MUTE}">// speaking skills</text>')
            bx, by = x + 10, y + th - 14
            b.append(f'<rect x="{bx}" y="{by}" width="{tw-20}" height="6" fill="none" stroke="{LINE}"/>')
            b.append(f'<rect x="{bx+1}" y="{by+1}" width="30" height="4" fill="{GREEN}">'
                     f'<animate attributeName="x" values="{bx+1};{bx+tw-20-31};{bx+1}" dur="2.6s" repeatCount="indefinite"/></rect>')
    save("beyond-code.svg", svg(W, H, "\n".join(b)))


# ================= VISION FLOW =================
def vision():
    W, H, bw, bh = 830, 96, 240, 72
    xs = [0, 295, 590]
    labels = [("CONCEPT", "// the idea"), ("DEVELOPMENT", "// build + learn"), ("WORKING PRODUCT", "// ship it")]
    b = []
    for i, (x, (lab, sub)) in enumerate(zip(xs, labels)):
        y = 12
        b.append(f'<rect x="{x+0.5}" y="{y+0.5}" width="{bw-1}" height="{bh-1}" fill="{PANEL}" stroke="{GREEN if i==2 else LINE}"/>')
        b.append(f'<rect x="{x+12}" y="{y+12}" width="6" height="6" fill="{GREEN}"/>')
        b.append(pix(lab, x + 12, y + 28, 2, TEXT if i < 2 else GREEN))
        b.append(f'<text x="{x+12}" y="{y+bh-12}" font-family="{MONO}" font-size="12" fill="{MUTE}">{sub}</text>')
    for i in range(2):
        x0 = xs[i] + bw + 6
        cy = 12 + bh // 2
        for k in range(3):
            b.append(f'<rect x="{x0 + k*8}" y="{cy-3}" width="6" height="6" fill="{GREEN}" opacity="0.2">'
                     f'<animate attributeName="opacity" values="0.2;1;0.2" dur="1.6s" begin="{k*0.3}s" repeatCount="indefinite"/></rect>')
        # arrow head (pixel triangle)
        hx = x0 + 26
        for j, wdt in enumerate((6, 12, 18, 12, 6)):
            b.append(f'<rect x="{hx}" y="{cy-15+j*6}" width="{wdt}" height="6" fill="{GREEN}"/>')
    save("vision-flow.svg", svg(W, H, "\n".join(b)))


# ================= FOOTER =================
def footer():
    W, H = 830, 56
    msg = "// END OF PROFILE  -  thanks for stopping by"
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="{PANEL}" stroke="{LINE}"/>',
         noise(W - 300, W - 10, 6, 50, 6, 77, lambda t: 0.03 + 0.55 * t ** 1.4),
         f'<text x="16" y="33" font-family="{MONO}" font-size="14" fill="{GREEN}">{msg}</text>']
    cx = 16 + int(len(msg) * 8.43) + 6
    b.append(f'<rect x="{cx}" y="20" width="9" height="16" fill="{GREEN}"><animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></rect>')
    save("footer.svg", svg(W, H, "\n".join(b)))


# ================= SMALL ICON TILES (48x48, match skillicons dark style) =================
def tiles():
    tile = '<rect width="48" height="48" rx="10" fill="#242938"/>'
    dsa = (tile + f'<g stroke="{MUTE}" stroke-width="2"><path d="M24 12L14 26M24 12L34 26M14 26L9 38M14 26L19 38M34 26L29 38M34 26L39 38"/></g>'
           f'<g fill="{GREEN}"><rect x="20" y="8" width="8" height="8"/><rect x="10" y="22" width="8" height="8"/><rect x="30" y="22" width="8" height="8"/></g>'
           f'<g fill="{TEXT}"><rect x="5" y="36" width="8" height="6"/><rect x="15" y="36" width="8" height="6"/><rect x="25" y="36" width="8" height="6"/><rect x="35" y="36" width="8" height="6"/></g>')
    be = tile + "".join(f'<rect x="9" y="{y}" width="30" height="8" fill="none" stroke="{TEXT}" stroke-width="2"/>'
                        f'<rect x="13" y="{y+3}" width="3" height="3" fill="{GREEN}"/><rect x="31" y="{y+3}" width="5" height="2" fill="{MUTE}"/>'
                        for y in (9, 20, 31))
    slot = (f'<rect x="0.5" y="0.5" width="47" height="47" rx="10" fill="none" stroke="{LINE}" stroke-dasharray="4 4"/>'
            f'<path d="M22 14h4v8h8v4h-8v8h-4v-8h-8v-4h8z" fill="{LINE}"/>')
    for n, c in (("icon-dsa.svg", dsa), ("icon-backend.svg", be), ("slot-empty.svg", slot)):
        save(n, svg(48, 48, c))


# ================= 3D GRAPH PLACEHOLDER (overwritten by the workflow) =================
def placeholder():
    W, H = 1280, 850
    p = os.path.join(ROOT, "profile-3d-contrib", "profile-night-green.svg")
    # never overwrite a real generated file
    if os.path.exists(p) and "WAITING FOR FIRST RUN" not in open(p, encoding="utf-8").read(5000) \
            and os.path.getsize(p) > 20000:
        print("real generated graph found - placeholder not touched")
        return
    t1, t2 = "3D CONTRIBUTION GRAPH", "WAITING FOR FIRST RUN"
    b = [f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<rect width="{W}" height="{H}" fill="url(#grid)"/>',
         noise(0, W, 0, 70, 20, 5, lambda t: 0.35 * abs(2 * t - 1) ** 2),
         pix(t1, (W - text_w(t1, 8)) // 2, 270, 8, TEXT),
         pix(t2, (W - text_w(t2, 8)) // 2, 380, 8, GREEN),
         f'<text x="{W//2}" y="520" text-anchor="middle" font-family="{MONO}" font-size="28" fill="{MUTE}">GitHub -&gt; Actions -&gt; GitHub-Profile-3D-Contrib -&gt; Run workflow</text>',
         f'<text x="{W//2}" y="565" text-anchor="middle" font-family="{MONO}" font-size="28" fill="{MUTE}">This placeholder is replaced by your real contribution data.</text>',
         f'<rect width="{W}" height="{H}" fill="url(#scan)"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{LINE}" stroke-width="2"/>']
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg(W, H, "\n".join(b), GRID_DEFS))


if __name__ == "__main__":
    header()
    for i, (f, l) in enumerate(SECTIONS, 1):
        heading(f, l, i)
    beyond()
    vision()
    footer()
    tiles()
    placeholder()
    print("assets generated in", os.path.abspath(OUT))
