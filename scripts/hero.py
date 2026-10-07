"""Generates assets/hero-{dark,light}.svg for the GitHub profile README.

A terminal window: a duotone halftone portrait on a dark screen (left) and a
neofetch-style system card (right). Pure SVG + CSS animation, system
monospace fonts only, so it renders through GitHub's image proxy.
"""
import json
import sys
from html import escape

PORTRAIT = open(sys.argv[1]).read().strip()
OUT = sys.argv[2]
STATS = json.load(open(sys.argv[3]))['stats']

W = 1000
TITLE_H = 40
PAD = 24

INFO = [
    ('prompt', 'qadir@lab ~ % neofetch --profile'),
    ('head', 'abdul.qadir.khan'),
    ('rule', ''),
    ('kv', 'Role', 'Full Stack AI Engineer · Lead Engineer'),
    ('kv', 'Mode', 'Forward Deployed Engineer'),
    ('kv', 'Uptime', '10+ years in production · since 2016'),
    ('kv', 'Shipped in', 'India · UAE · Germany'),
    ('kv', 'Led', 'teams of up to 6 · Annalect · Omnicom'),
    ('kv', 'Base', 'Gurgaon, India · IST'),
    ('gap',),
    ('sec', 'STACK'),
    ('kv', 'AI', 'agents · hybrid RAG · evals · voice'),
    ('kv', 'Frontend', 'React · Next.js · TypeScript · SwiftUI'),
    ('kv', 'Backend', 'Python · FastAPI · Node.js · NestJS'),
    ('kv', 'Data', 'PostgreSQL · pgvector · Redis'),
    ('kv', 'Infra', 'Docker · Kubernetes · AWS'),
    ('gap',),
    ('sec', 'LIVE STATS'),
    ('kv', 'Builds', f"{STATS['projects']} shipped · {STATS['ai']} AI-powered"),
    ('kv', 'Deployed', f"{STATS['live']} live · {STATS['openSource']} open source"),
    ('gap',),
    ('sec', 'CONTACT'),
    ('kv', 'Portfolio', 'techhub.cafe/me'),
    ('kv', 'LinkedIn', 'in/aqadirkhan'),
    ('gap',),
    ('palette',),
    ('status', 'open to senior, lead & forward-deployed roles'),
    ('cursor', 'qadir@lab ~ %'),
]

THEMES = {
    'dark': dict(
        bg='#07090f', win='#0b0f18', edge='#1d2433', bar='#0e131e', title='#7d869c',
        text='#d7dcea', dim='#6b7489', key='#5ce6ff', head='#ffffff', rule='#273044',
        sec='#9582ff', grid='rgba(92,230,255,0.035)', glow='0.55',
    ),
    'light': dict(
        bg='#ffffff', win='#fbfcfe', edge='#dde2ec', bar='#f1f3f8', title='#6a7387',
        text='#1e2433', dim='#8a93a8', key='#0a8fb0', head='#0b1020', rule='#e3e7ef',
        sec='#6a4ff0', grid='rgba(10,143,176,0.05)', glow='0.25',
    ),
}

# Left screen (always dark, like a monitor inside the window).
SX, SY, SW = PAD, TITLE_H + 20, 384
LABEL_H = 30
IMG_W, IMG_H = 356, 428
IX, IY = SX + 14, SY + LABEL_H + 10
SH = LABEL_H + 10 + IMG_H + 30

# Right column.
RX = SX + SW + 30
LINE = 19.5
KEY_W = 92  # key + leader dots, stretched to exactly this width
VX = RX + KEY_W + 12


def info_height():
    h = 0
    for item in INFO:
        h += 10 if item[0] == 'gap' else (24 if item[0] == 'palette' else LINE)
    return h


H = int(max(SY + SH, TITLE_H + 40 + info_height()) + PAD)


def build(theme):
    t = THEMES[theme]
    o = []
    o.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Abdul Qadir Khan, Full Stack AI Engineer, Lead Software Engineer and Forward Deployed Engineer">'
    )
    o.append(
        '<style>'
        "text{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace}"
        '.scan{animation:scan 5.5s linear infinite}'
        f'@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY({IMG_H + 60}px)}}}}'
        '.cur{animation:blink 1.05s steps(1) infinite}'
        '@keyframes blink{50%{opacity:0}}'
        '.dot{animation:pulse 2.4s ease-in-out infinite}'
        '@keyframes pulse{50%{opacity:.35}}'
        '.flk{animation:flk 7s ease-in-out infinite}'
        '@keyframes flk{0%,100%{opacity:1}48%{opacity:1}50%{opacity:.8}52%{opacity:1}}'
        '.hud{animation:hud 3.2s ease-in-out infinite}@keyframes hud{50%{opacity:.45}}'
        '@media (prefers-reduced-motion:reduce){*{animation:none!important}.scan{display:none}}'
        '</style>'
    )
    o.append(
        '<defs>'
        '<linearGradient id="ink" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#7cecff"/><stop offset=".55" stop-color="#8fb8ff"/>'
        '<stop offset="1" stop-color="#a593ff"/></linearGradient>'
        '<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#5ce6ff" stop-opacity="0"/>'
        '<stop offset=".85" stop-color="#5ce6ff" stop-opacity=".16"/>'
        '<stop offset="1" stop-color="#5ce6ff" stop-opacity=".55"/></linearGradient>'
        '<linearGradient id="accent" x1="0" x2="1">'
        '<stop offset="0" stop-color="#5ce6ff"/><stop offset=".5" stop-color="#8fb8ff"/>'
        '<stop offset="1" stop-color="#9582ff"/></linearGradient>'
        f'<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<path d="M22 0H0V22" fill="none" stroke="{t["grid"]}"/></pattern>'
        f'<clipPath id="screen"><rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="12"/></clipPath>'
        '<radialGradient id="halo" cx=".5" cy=".42" r=".6">'
        f'<stop offset="0" stop-color="#5ce6ff" stop-opacity="{float(t["glow"]) * 0.22:.3f}"/>'
        '<stop offset="1" stop-color="#5ce6ff" stop-opacity="0"/></radialGradient>'
        '<filter id="duo" color-interpolation-filters="sRGB">'
        '<feColorMatrix type="matrix" values=".33 .33 .33 0 0 .33 .33 .33 0 0 .33 .33 .33 0 0 0 0 0 1 0"/>'
        '<feComponentTransfer><feFuncR type="table" tableValues=".015 .09 .33 .86"/>'
        '<feFuncG type="table" tableValues=".02 .30 .86 .99"/><feFuncB type="table" tableValues=".04 .52 1 1"/>'
        '</feComponentTransfer></filter>'
        '<pattern id="dots" width="3" height="3" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.3" fill="#fff"/></pattern>'
        f'<mask id="half"><rect x="{IX}" y="{IY}" width="{IMG_W}" height="{IMG_H}" fill="url(#dots)"/></mask>'
        '<pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".45"/></pattern>'
        '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".7" stop-color="#04060b" stop-opacity="0"/><stop offset="1" stop-color="#04060b"/></linearGradient>'
        '</defs>'
    )
    # Window.
    o.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["win"]}" stroke="{t["edge"]}"/>')
    o.append(f'<rect x="1" y="{TITLE_H}" width="{W - 2}" height="{H - TITLE_H - 1}" fill="url(#grid)"/>')
    o.append(f'<path d="M1 {TITLE_H}V17A16 16 0 0 1 17 1H{W - 17}A16 16 0 0 1 {W - 1} 17V{TITLE_H}Z" fill="{t["bar"]}"/>')
    o.append(f'<line x1="1" y1="{TITLE_H}" x2="{W - 1}" y2="{TITLE_H}" stroke="{t["edge"]}"/>')
    o.append(f'<rect x="{W * 0.3}" y="{TITLE_H - 1}" width="{W * 0.4}" height="1.5" fill="url(#accent)" opacity=".8"/>')
    for i, c in enumerate(['#ff5f57', '#febc2e', '#28c840']):
        o.append(f'<circle cx="{22 + i * 19}" cy="{TITLE_H / 2}" r="6" fill="{c}"/>')
    o.append(
        f'<text x="{W / 2}" y="{TITLE_H / 2 + 4}" text-anchor="middle" font-size="12" fill="{t["title"]}">'
        'aqkprogrammer / README.md — qadir@lab: ~</text>'
    )
    o.append(
        f'<g transform="translate({W - 92} {TITLE_H / 2})"><circle class="dot" r="3.5" cx="0" cy="0" fill="#22c55e"/>'
        f'<text x="10" y="4" font-size="11" letter-spacing="1.5" fill="{t["dim"]}">ONLINE</text></g>'
    )

    # Screen.
    o.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="12" fill="#04060b" stroke="#1b2333"/>')
    o.append(f'<g clip-path="url(#screen)">')
    o.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" fill="url(#halo)"/>')
    o.append(f'<line x1="{SX}" y1="{SY + LABEL_H}" x2="{SX + SW}" y2="{SY + LABEL_H}" stroke="#151c2a"/>')
    o.append(
        f'<text x="{SX + 14}" y="{SY + 19}" font-size="10" letter-spacing="1.6" fill="#5ce6ff">◆ AI.MAP</text>'
        f'<text x="{SX + SW - 14}" y="{SY + 19}" text-anchor="end" font-size="10" letter-spacing="1.2" fill="#4b556b">portrait.scan · halftone</text>'
    )
    img = f'href="data:image/jpeg;base64,{PORTRAIT}" x="{IX}" y="{IY}" width="{IMG_W}" height="{IMG_H}"'
    o.append('<g class="flk">')
    o.append(f'<image {img} filter="url(#duo)" opacity=".28"/>')
    o.append(f'<image {img} filter="url(#duo)" mask="url(#half)"/>')
    o.append(f'<rect x="{IX}" y="{IY}" width="{IMG_W}" height="{IMG_H}" fill="url(#lines)"/>')
    o.append(f'<rect x="{IX}" y="{IY}" width="{IMG_W}" height="{IMG_H}" fill="url(#fade)"/>')
    o.append('</g>')
    # Face-tracking HUD.
    fx, fy, fw, fh = IX + 98, IY + 70, 150, 196
    k = 16
    br = ''.join([
        f'M{fx} {fy + k}V{fy}H{fx + k}', f'M{fx + fw - k} {fy}H{fx + fw}V{fy + k}',
        f'M{fx} {fy + fh - k}V{fy + fh}H{fx + k}', f'M{fx + fw - k} {fy + fh}H{fx + fw}V{fy + fh - k}',
    ])
    o.append(
        f'<g class="hud"><path d="{br}" fill="none" stroke="#5ce6ff" stroke-width="1.6"/>'
        f'<text x="{fx}" y="{fy - 8}" font-size="9" letter-spacing="1.4" fill="#5ce6ff">SUBJECT · AQK</text>'
        f'<text x="{fx + fw}" y="{fy + fh + 14}" text-anchor="end" font-size="9" letter-spacing="1.2" fill="#8fb8ff">MATCH ✓</text></g>'
    )
    o.append(f'<rect class="scan" x="{SX}" y="{IY - 60}" width="{SW}" height="60" fill="url(#beam)"/>')
    # Corner ticks on the screen.
    bx, by = SX + 10, SY + SH - 16
    o.append(f'<text x="{bx + 4}" y="{by}" font-size="9" letter-spacing="1.4" fill="#3d4659">QADIR / LAB · GURGAON · IST</text>')
    o.append('</g>')

    # Info column.
    y = TITLE_H + 40
    i = 0
    for item in INFO:
        kind = item[0]
        d = f'style="animation-delay:{0.35 + i * 0.07:.2f}s"'
        if kind == 'gap':
            y += 10
            continue
        if kind == 'prompt':
            o.append(
                f'<text class="l" {d} x="{RX}" y="{y}" font-size="13"><tspan fill="#22c55e">➜</tspan>'
                f'<tspan fill="{t["key"]}"> {escape(item[1].split(" % ")[0])}</tspan>'
                f'<tspan fill="{t["dim"]}"> % </tspan><tspan fill="{t["text"]}">{escape(item[1].split(" % ")[1])}</tspan></text>'
            )
        elif kind == 'head':
            o.append(
                f'<text class="l" {d} x="{RX}" y="{y + 4}" font-size="17" font-weight="700" fill="{t["head"]}">'
                f'Abdul Qadir Khan<tspan fill="{t["dim"]}" font-weight="400" font-size="13">  @aqkprogrammer</tspan></text>'
            )
            y += 4
        elif kind == 'rule':
            o.append(f'<rect class="l" {d} x="{RX}" y="{y - 10}" width="{W - RX - PAD - 4}" height="1.5" fill="url(#accent)" opacity=".7"/>')
            y -= 4
        elif kind == 'sec':
            o.append(
                f'<text class="l" {d} x="{RX}" y="{y}" font-size="10.5" letter-spacing="2" fill="{t["sec"]}">'
                f'── {escape(item[1])} </text>'
            )
        elif kind == 'kv':
            key = item[1]
            dots = ' ' + '·' * max(2, 12 - len(key))
            o.append(
                f'<g class="l" {d}><text x="{RX}" y="{y}" font-size="13" textLength="{KEY_W}" lengthAdjust="spacing">'
                f'<tspan fill="{t["key"]}">{escape(key)}</tspan><tspan fill="{t["rule"]}">{dots}</tspan></text>'
                f'<text x="{VX}" y="{y}" font-size="13" fill="{t["text"]}">{escape(item[2])}</text></g>'
            )
        elif kind == 'palette':
            cols = ['#ff5f57', '#febc2e', '#28c840', '#5ce6ff', '#8fb8ff', '#9582ff', '#f472b6', t['text']]
            o.append(f'<g class="l" {d}>' + ''.join(
                f'<rect x="{RX + k * 26}" y="{y - 8}" width="22" height="12" rx="3" fill="{c}"/>' for k, c in enumerate(cols)
            ) + '</g>')
            y += 24 - LINE
        elif kind == 'status':
            o.append(
                f'<g class="l" {d}><circle class="dot" cx="{RX + 5}" cy="{y - 4}" r="4" fill="#22c55e"/>'
                f'<text x="{RX + 16}" y="{y}" font-size="13" fill="{t["text"]}">{escape(item[1])}</text></g>'
            )
        elif kind == 'cursor':
            o.append(
                f'<text class="l" {d} x="{RX}" y="{y}" font-size="13"><tspan fill="#22c55e">➜</tspan>'
                f'<tspan fill="{t["key"]}"> qadir@lab</tspan><tspan fill="{t["dim"]}"> % </tspan></text>'
                f'<rect class="cur" x="{RX + 128}" y="{y - 11}" width="8" height="14" fill="{t["key"]}"/>'
            )
        y += LINE
        i += 1
    o.append('</svg>')
    return '\n'.join(o)


for theme in THEMES:
    with open(OUT.replace('{theme}', theme), 'w') as f:
        f.write(build(theme))
print('height', H)
