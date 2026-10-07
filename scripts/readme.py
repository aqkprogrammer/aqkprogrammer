"""Builds the aqkprogrammer profile README from the /me portfolio data.

Every project, status and link comes from techhub's src/app/(portfolio)/me/_data
(dumped by scripts/dump.ts; run scripts/build.sh), so the profile never claims more than the portfolio.
"""
import json
import os
import shutil
import sys
from pathlib import Path

DATA = json.load(open(sys.argv[1]))
REPO = Path(sys.argv[2])
PUBLIC = Path(os.environ['TECHHUB']) / 'public'
SITE = 'https://techhub.cafe/me'

P = {p['slug']: p for p in DATA['projects']}
used: set[str] = set()


def case(slug):
    return f'{SITE}/work/{slug}'


def status(p):
    label = {
        'product': 'Product', 'prototype': 'Prototype', 'in-development': 'In development',
        'demo': 'Demo', 'experiment': 'Experiment', 'assessment': 'Assessment', 'client': 'Client',
    }[p['status']]
    return f"{label} · {p['statusNote']}" if p.get('statusNote') else label


def links(p, sep=' · '):
    out = []
    if p.get('live'):
        out.append(f"<a href=\"{p['live']}\">Live&nbsp;↗</a>")
    if p.get('repo'):
        out.append(f"<a href=\"{p['repo']}\">Code</a>")
    out.append(f"<a href=\"{case(p['slug'])}\">Case&nbsp;study</a>")
    return sep.join(out)


def copy_shot(p, size='sm'):
    src = p.get('cover')
    if not src:
        return None
    if size != 'sm':
        src = src.replace('-sm.webp', f'-{size}.webp')
    dest = REPO / 'assets' / 'shots' / f"{p['slug']}.webp"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PUBLIC / src.lstrip('/'), dest)
    return f'assets/shots/{p["slug"]}.webp'


def card(slug):
    p = P[slug]
    used.add(slug)
    img = copy_shot(p)
    stack = ' '.join(f'<code>{t}</code>' for t in p['tech'][:5])
    return (
        f'<td width="50%" valign="top">\n'
        f'<a href="{case(slug)}"><img src="{img}" alt="{p["name"]} screenshot" width="100%"></a>\n'
        f'<h3>{p["name"]}</h3>\n'
        f'<sub><b>{status(p).upper()}</b></sub>\n'
        f'<p>{p["tagline"]}</p>\n'
        f'<p>{stack}</p>\n'
        f'<p>{links(p)}</p>\n'
        f'</td>'
    )


def table(slugs, cols=('Project', 'What it is', 'Status', 'Links')):
    rows = [f"| {' | '.join(cols)} |", '|' + '---|' * len(cols)]
    for s in slugs:
        p = P[s]
        used.add(s)
        rows.append(
            f"| **{p['name']}** | {p['tagline']} | <sub>{status(p)}</sub> | {links(p, '<br>')} |"
        )
    return '\n'.join(rows)


def section(title, sub=None):
    return f'\n## {title}\n' + (f'\n<sub>{sub}</sub>\n' if sub else '')


FEATURED = ['cardcopilot', 'kavrix', 'techhub', 'growzen', 'dowel', 'novaryn', 'salariax', 'docintel']
AI_SYSTEMS = ['llm-gateway', 'llm-eval-platform', 'agent-orchestrator', 'rag-hybrid-search',
              'ai-software-factory', 'latency-spike', 'aiplatform', 'swara', 'indic-voice', 'local-llm-chat']
AI_PRODUCTS = ['paytoroast', 'contract-ai', 'finopsguard', 'revio', 'branexa', 'jarvis', 'truthlens']
NATIVE = ['aether', 'vision', 'hangly', 'deskpal', 'flyby', 'web-hang']
INTERACTIVE = ['demos-platform', 'gesture-arena', 'air-music', 'air-wheel', 'bloom', 'aviary', 'ludoverse',
               'otp-slingshot', 'receipt-printer', 'orbit-cards', 'vault-meter', 'hanging-cards']
STUDIES = ['kagaz', 'vanilla-studio', 'mirror-nine', 'nova-brew', 'lumen-atelier', 'sartor', 'crema-club']
CLIENT = ['searchmyguide', 'faiz-web', 'skillgraph', 'clinical-snapshot']

cp = P['cluepilot']
used.add('cluepilot')
banner = copy_shot(cp, 'md')

badge = lambda label, color, logo, href: (
    f'<a href="{href}"><img alt="{label}" src="https://img.shields.io/badge/{label.replace(" ", "%20").replace("-", "--")}'
    f'-{color}?style=for-the-badge&logo={logo}&logoColor=white&labelColor=0b1020"></a>'
)

md = []
md.append('''<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img alt="Abdul Qadir Khan — Full Stack AI Engineer, Lead Software Engineer and Forward Deployed Engineer" src="assets/hero-dark.svg" width="100%">
</picture>

<br>
''')
md.append(' '.join([
    badge('Portfolio', '0aa5c8', 'googlechrome', SITE),
    badge('Résumé', '7a63f0', 'readdotcv', f'{SITE}/resume'),
    badge('LinkedIn', '0A66C2', 'linkedin', 'https://www.linkedin.com/in/aqadirkhan/'),
    badge('Email', '22c55e', 'gmail', 'mailto:aqadirkhan93@gmail.com'),
]))
md.append('''

**AI engineer, forward deployed — I go where the problem lives and ship the system that solves it.**

<sub>Full Stack AI Engineer · Lead Software Engineer · Forward Deployed Engineer · 10+ years in production</sub>

</div>
''')

md.append(section('◆ whoami'))
md.append('''
```yaml
role:     Full Stack AI Engineer · Lead Engineer · Forward Deployed
latest:   Senior Software Engineer @ Tractable AI (2025 — 2026)
          computer-vision model integration for AI vehicle inspection
led:      front-end for L’Oréal’s oneMediaTech @ Annalect · Omnicom
          Express monolith → FastAPI microservices on Kubernetes
on_site:  Volkswagen (Munich) · Emirates (Dubai)
builds:   tool-calling agents with human approval gates
          hybrid RAG with reranking + citation checks · LLM evals
          Indic voice pipelines · on-device models on Apple silicon
ships:    product → architecture → code → deploy → ops
open_to:  senior, lead & forward-deployed roles · freelance AI work
```
''')

md.append(section('◆ Flagship — CluePilot.ai', status(cp)))
md.append(f'''
<a href="{case('cluepilot')}"><img src="{banner}" alt="CluePilot answering an interview question on macOS" width="100%"></a>

**{cp['tagline']}**
A Swift 6 / SwiftUI menu-bar app summoned with ⇧⌘Space that streams answers from eight providers — including on-device Apple Intelligence and Ollama. Context Spaces add on-device retrieval over your résumé and notes; licensing is verified offline with Ed25519.

{' '.join(f'`{t}`' for t in cp['tech'][:6])}

{links(cp)}
''')

md.append(section('◆ Featured builds', 'Click a screenshot for the full case study — problem, architecture, trade-offs and evidence.'))
rows = ['<table>']
for i in range(0, len(FEATURED), 2):
    rows.append('<tr>\n' + '\n'.join(card(s) for s in FEATURED[i:i + 2]) + '\n</tr>')
rows.append('</table>')
md.append('\n' + '\n'.join(rows) + '\n')

md.append(section('◆ AI systems & open source', 'Agents, gateways, evals, RAG and voice — the infrastructure under the products.'))
md.append('\n' + table(AI_SYSTEMS) + '\n')

md.append(section('◆ More AI products'))
md.append('\n' + table(AI_PRODUCTS) + '\n')

for title, slugs in [
    ('◆ Native macOS', NATIVE),
    ('◆ Interactive & gesture lab', INTERACTIVE),
    ('◆ Product & design studies', STUDIES),
    ('◆ Client work & engineering assessments', CLIENT),
]:
    md.append(f'\n<details>\n<summary><b>{title[2:]}</b> — {len(slugs)} builds</summary>\n\n{table(slugs)}\n\n</details>\n')

md.append(section('◆ Experience'))
md.append('''
| When | Role | Where |
|---|---|---|
| 2025 — 2026 | **Senior Software Engineer** · Tractable AI | Noida, India |
| 2021 — 2025 | **Lead Software Engineer** · Annalect · Omnicom | Gurgaon, India |
| 2022 — 2023 | **On-site Engineer** · Volkswagen · EOL | Munich, Germany |
| 2020 — 2021 | **Software Developer** · Dyninno Group | Gurgaon, India |
| 2019 — 2020 | **Software Engineer** · Emirates · Dew Solutions | Dubai, UAE |
| 2016 — 2019 | **Software Engineer** · CoderSoft · Halwits | Gurgaon · Lucknow |
''')

md.append(section('◆ Toolkit'))
md.append('''
<p align="center">
  <img src="https://skillicons.dev/icons?i=python,fastapi,ts,react,nextjs,nodejs,nestjs,swift,tailwind,graphql&theme=dark" alt="Languages and frameworks"><br>
  <img src="https://skillicons.dev/icons?i=postgres,redis,mongodb,supabase,docker,kubernetes,aws,githubactions,rust,tauri&theme=dark" alt="Data and infrastructure">
</p>

<p align="center"><sub><b>AI</b> — LLM agents (LangGraph, tool calling) · hybrid RAG (pgvector, Qdrant, ChromaDB) · evals & observability · speech (Deepgram, ElevenLabs, LiveKit) · on-device (MLX, Core ML) · computer vision (MediaPipe)</sub></p>
''')

md.append(section('◆ Activity'))
md.append('''
<p align="center">
  <img src="./profile-3d-contrib/profile-night-rainbow.svg" alt="3D contribution calendar" width="100%">
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/aqkprogrammer/aqkprogrammer/output/github-snake-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/aqkprogrammer/aqkprogrammer/output/github-snake.svg">
  <img alt="Contribution snake" src="https://raw.githubusercontent.com/aqkprogrammer/aqkprogrammer/output/github-snake.svg" width="100%">
</picture>
''')

md.append(f'''
---

<div align="center">

### Have a hard problem worth solving?

I typically reply within 48 hours, IST-friendly.

{badge('Start a conversation', '0aa5c8', 'maildotru', f'{SITE}#contact')} {badge('Medium', '000000', 'medium', 'https://medium.com/@aqkprogrammer')} {badge('Instagram', 'E4405F', 'instagram', 'https://www.instagram.com/aqkprogrammer/')}

<sub>Every project above has a case study at <a href="{SITE}">techhub.cafe/me</a> — {len(DATA['projects'])} builds, each labelled for exactly what it is.</sub>

</div>
''')

missing = set(P) - used
if missing:
    sys.exit(f'projects missing from README: {sorted(missing)}')
(REPO / 'README.md').write_text('\n'.join(md))
print('ok', len(used), 'projects')
