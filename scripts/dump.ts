// Dumps the techhub.cafe/me portfolio data the README is built from.
// Run from the techhub repo: npx tsx --tsconfig tsconfig.json <this file> <out.json>
import { writeFileSync } from 'fs';

import { domainsOf } from '@/app/(portfolio)/me/_data/domains';
import { PROFILE } from '@/app/(portfolio)/me/_data/profile';
import { PROJECTS, STATS } from '@/app/(portfolio)/me/_data/projects';

const projects = PROJECTS.map((p) => ({
  slug: p.slug,
  name: p.name,
  tagline: p.tagline,
  category: p.category,
  status: p.status,
  statusNote: p.statusNote,
  platforms: p.platforms,
  tech: p.tech.slice(0, 8),
  live: p.links.live,
  repo: p.links.repo,
  featured: p.featured,
  cover: p.media.cover?.srcSm ?? p.media.cover?.src,
  domains: domainsOf(p),
}));
writeFileSync(process.argv[2], JSON.stringify({ profile: PROFILE, stats: STATS, projects }, null, 1));
