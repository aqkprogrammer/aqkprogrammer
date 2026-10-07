"""Renders assets/activity-{dark,light}.svg: the last WEEKS weeks of the real
GitHub contribution calendar, in the README's palette. Run daily by
.github/workflows/activity.yml; needs GITHUB_TOKEN (or GH_TOKEN) in the env.

The window is labelled with its exact dates, so the card never implies more
than it shows.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

USER = 'aqkprogrammer'
WEEKS = 12
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'assets')

QUERY = '''query($login: String!) { user(login: $login) { contributionsCollection {
  contributionCalendar { weeks { contributionDays { date contributionCount } } } } } }'''


def fetch():
    token = os.environ.get('GITHUB_TOKEN') or os.environ['GH_TOKEN']
    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': QUERY, 'variables': {'login': USER}}).encode(),
        headers={'Authorization': f'bearer {token}', 'Content-Type': 'application/json'},
    )
    data = json.load(urllib.request.urlopen(req))
    weeks = data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    return [[(d['date'], d['contributionCount']) for d in w['contributionDays']] for w in weeks[-WEEKS:]]


THEMES = {
    'dark': dict(bg='#0b0f18', edge='#1d2433', text='#d7dcea', dim='#6b7489', head='#ffffff',
                 empty='#151b28', scale=['#123a4a', '#1a6d86', '#2fb3d6', '#5ce6ff', '#a593ff']),
    'light': dict(bg='#fbfcfe', edge='#dde2ec', text='#1e2433', dim='#8a93a8', head='#0b1020',
                  empty='#eceff5', scale=['#c6eef8', '#7fd6ec', '#2fb3d6', '#0a8fb0', '#6a4ff0']),
}


def thresholds(days):
    """Quartiles of the non-zero days, like GitHub's own shading."""
    counts = sorted(n for w in days for _, n in w if n)
    if not counts:
        return [1, 1, 1, 1]
    return [counts[min(len(counts) - 1, int(len(counts) * q))] for q in (0.2, 0.4, 0.6, 0.8)]


def level(n, cuts):
    if n == 0:
        return -1
    return sum(n > c for c in cuts)


def stats(days):
    flat = [d for w in days for d in w]
    total = sum(n for _, n in flat)
    active = sum(1 for _, n in flat if n)
    best = max(flat, key=lambda d: d[1])
    streak = cur = 0
    for _, n in flat:
        cur = cur + 1 if n else 0
        streak = max(streak, cur)
    return total, active, len(flat), best, streak


def fmt(d):
    return dt.date.fromisoformat(d).strftime('%-d %b %Y')


def render(days, theme):
    t = THEMES[theme]
    total, active, span, best, streak = stats(days)
    cuts = thresholds(days)
    W, CELL, GAP, X0, Y0 = 1000, 34, 7, 64, 108
    grid_w = WEEKS * (CELL + GAP)
    H = Y0 + 7 * (CELL + GAP) + 64
    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="GitHub activity, last {WEEKS} weeks: {total} contributions on {active} of {span} days">',
        "<style>text{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace}"
        '.c{animation:pop .5s ease-out both}@keyframes pop{from{opacity:.25}}'
        '@media (prefers-reduced-motion:reduce){.c{animation:none}}</style>',
        '<defs><linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="#5ce6ff"/>'
        '<stop offset=".5" stop-color="#8fb8ff"/><stop offset="1" stop-color="#9582ff"/></linearGradient></defs>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="{t["bg"]}" stroke="{t["edge"]}"/>',
        f'<rect x="1" y="{H - 4}" width="{W - 2}" height="3" fill="url(#accent)" opacity=".8"/>',
        f'<text x="{X0}" y="52" font-size="12" letter-spacing="2.2" fill="#9582ff">◆ ACTIVITY · LAST {WEEKS} WEEKS</text>',
        f'<text x="{X0}" y="78" font-size="13" fill="{t["dim"]}">{fmt(days[0][0][0])} — {fmt(days[-1][-1][0])}</text>',
    ]
    for d, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        o.append(f'<text x="{X0 - 12}" y="{Y0 + d * (CELL + GAP) + 22}" text-anchor="end" font-size="11" fill="{t["dim"]}">{label}</text>')
    for wi, week in enumerate(days):
        for di, (date, n) in enumerate(week):
            lv = level(n, cuts)
            fill = t['empty'] if lv < 0 else t['scale'][lv]
            o.append(
                f'<rect class="c" style="animation-delay:{(wi * 7 + di) * 0.006:.3f}s" x="{X0 + wi * (CELL + GAP)}" '
                f'y="{Y0 + di * (CELL + GAP)}" width="{CELL}" height="{CELL}" rx="6" fill="{fill}">'
                f'<title>{date}: {n} contribution{"s" if n != 1 else ""}</title></rect>'
            )
    # Stats column.
    sx = X0 + grid_w + 56
    rows = [
        (f'{total:,}', 'contributions'),
        (f'{active}/{span}', 'active days'),
        (f'{streak}', 'day longest streak'),
        (f'{best[1]}', f'on {fmt(best[0])}, busiest day'),
    ]
    for i, (big, small) in enumerate(rows):
        y = Y0 + 34 + i * 66
        o.append(f'<text x="{sx}" y="{y}" font-size="26" font-weight="700" fill="{t["head"]}">{big}</text>')
        o.append(f'<text x="{sx}" y="{y + 20}" font-size="12" fill="{t["dim"]}">{small}</text>')
    lx = X0
    ly = H - 30
    o.append(f'<text x="{lx}" y="{ly}" font-size="11" fill="{t["dim"]}">less</text>')
    for k, c in enumerate([t['empty']] + t['scale']):
        o.append(f'<rect x="{lx + 38 + k * 18}" y="{ly - 11}" width="13" height="13" rx="3" fill="{c}"/>')
    o.append(f'<text x="{lx + 38 + 6 * 18 + 4}" y="{ly}" font-size="11" fill="{t["dim"]}">more</text>')
    o.append(f'<text x="{W - 32}" y="{ly}" text-anchor="end" font-size="11" fill="{t["dim"]}">full history → github.com/{USER}</text>')
    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    days = fetch()
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        (OUT / f'activity-{theme}.svg').write_text(render(days, theme))
    print('weeks', len(days), 'stats', stats(days))
