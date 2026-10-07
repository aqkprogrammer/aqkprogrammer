// Renders 1280×640 social-preview cards (assets/social/<repo>.png) for every
// portfolio project with a public repo. GitHub has no API for these, so upload
// each one by hand: repo → Settings → General → Social preview.
// Run from the techhub repo (for sharp):  node <this file> <data.json> <out dir>
const fs = require('fs');
const path = require('path');
// sharp comes from the techhub checkout this runs in.
const sharp = require(require.resolve('sharp', { paths: [process.cwd()] }));

const [dataPath, outDir] = process.argv.slice(2);
const { projects } = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
const W = 1280;
const H = 640;
const SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif";
const MONO = "Menlo, 'SF Mono', Consolas, monospace";
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function wrap(text, max) {
  const lines = [];
  let line = '';
  for (const word of text.split(' ')) {
    if ((line + ' ' + word).trim().length > max) {
      lines.push(line.trim());
      line = word;
    } else line += ' ' + word;
  }
  if (line.trim()) lines.push(line.trim());
  return lines;
}

async function card(p) {
  const repo = p.repo.split('/').pop();
  const shot = p.cover && path.join('public', p.cover.replace('-sm.webp', '-md.webp'));
  const hasShot = shot && fs.existsSync(shot);
  const textW = hasShot ? 560 : 1100;
  const tagline = wrap(p.tagline, hasShot ? 34 : 62).slice(0, 4);
  // Fit long names to the text column (Helvetica Bold averages ~0.6em per char).
  const nameSize = Math.min(68, Math.floor(textW / (p.name.length * 0.6)));

  let img = '';
  if (hasShot) {
    const buf = await sharp(shot).resize(620, 388, { fit: 'cover', position: 'top' }).jpeg({ quality: 86 }).toBuffer();
    const x = 620;
    const y = 126;
    img = `
      <rect x="${x - 2}" y="${y - 30}" width="624" height="420" rx="16" fill="#0b0f18" stroke="#273044"/>
      ${['#ff5f57', '#febc2e', '#28c840'].map((c, i) => `<circle cx="${x + 18 + i * 17}" cy="${y - 15}" r="5" fill="${c}"/>`).join('')}
      <clipPath id="shot"><rect x="${x}" y="${y}" width="620" height="388" rx="0"/></clipPath>
      <image href="data:image/jpeg;base64,${buf.toString('base64')}" x="${x}" y="${y}" width="620" height="388" clip-path="url(#shot)"/>`;
  }

  const chips = [];
  let cx = 64;
  for (const t of p.tech.slice(0, hasShot ? 4 : 6)) {
    const w = t.length * 10.2 + 28;
    if (cx + w > 64 + textW) break;
    chips.push(
      `<rect x="${cx}" y="440" width="${w}" height="34" rx="8" fill="rgba(92,230,255,0.08)" stroke="rgba(92,230,255,0.28)"/>` +
        `<text x="${cx + 14}" y="462" font-family="${MONO}" font-size="16" fill="#9fefff">${esc(t)}</text>`,
    );
    cx += w + 10;
  }

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <defs>
      <radialGradient id="g1" cx="1" cy="0" r="1"><stop offset="0" stop-color="#9582ff" stop-opacity=".35"/><stop offset="1" stop-color="#9582ff" stop-opacity="0"/></radialGradient>
      <radialGradient id="g2" cx="0" cy="1" r="1"><stop offset="0" stop-color="#5ce6ff" stop-opacity=".22"/><stop offset="1" stop-color="#5ce6ff" stop-opacity="0"/></radialGradient>
      <linearGradient id="accent" x1="0" x2="1"><stop offset="0" stop-color="#5ce6ff"/><stop offset=".5" stop-color="#8fb8ff"/><stop offset="1" stop-color="#9582ff"/></linearGradient>
      <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="rgba(92,230,255,0.05)"/></pattern>
    </defs>
    <rect width="${W}" height="${H}" fill="#05060a"/>
    <rect width="${W}" height="${H}" fill="url(#grid)"/>
    <rect width="${W}" height="${H}" fill="url(#g1)"/>
    <rect width="${W}" height="${H}" fill="url(#g2)"/>
    <rect y="${H - 6}" width="${W}" height="6" fill="url(#accent)"/>
    <rect x="64" y="58" width="26" height="26" rx="8" fill="none" stroke="#5ce6ff" stroke-opacity=".6"/>
    <circle cx="77" cy="71" r="4" fill="#5ce6ff"/>
    <text x="104" y="77" font-family="${MONO}" font-size="17" font-weight="700" letter-spacing="3" fill="#fff">QADIR<tspan fill="#5ce6ff"> / </tspan><tspan fill="#9aa3b8" font-weight="400">LAB</tspan></text>
    <text x="64" y="150" font-family="${MONO}" font-size="16" letter-spacing="2" fill="#8a93a8">◆ ${esc(p.status === 'demo' || p.status === 'experiment' ? 'OPEN SOURCE' : p.status.toUpperCase())}</text>
    <text x="64" y="${150 + nameSize + 14}" font-family="${SANS}" font-size="${nameSize}" font-weight="700" letter-spacing="-1.5" fill="#fff">${esc(p.name)}</text>
    ${tagline.map((l, i) => `<text x="64" y="${284 + i * 38}" font-family="${SANS}" font-size="27" fill="#b4bccd">${esc(l)}</text>`).join('')}
    ${chips.join('')}
    <text x="64" y="560" font-family="${MONO}" font-size="18" fill="#8a93a8">github.com/aqkprogrammer/<tspan fill="#fff">${esc(repo)}</tspan></text>
    <text x="64" y="590" font-family="${MONO}" font-size="15" fill="#5c6478">case study → techhub.cafe/me/work/${esc(p.slug)}</text>
    ${img}
  </svg>`;

  const out = path.join(outDir, `${repo}.png`);
  await sharp(Buffer.from(svg)).png({ compressionLevel: 9, palette: false }).toFile(out);
  return [repo, fs.statSync(out).size];
}

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  for (const p of projects.filter((p) => p.repo)) console.log(...(await card(p)));
})();
