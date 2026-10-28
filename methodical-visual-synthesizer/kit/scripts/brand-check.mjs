#!/usr/bin/env node
// Brand check: contrast of the palette pairs, licences on fonts, a change log, and whether video configs use the brand tokens.
//   node scripts/brand-check.mjs                      checks brand/_template and every brand/<slug>/brand.json, then configs/*.json
//   node scripts/brand-check.mjs brand/<slug>/brand.json [configs/<project>.json ...]
//   add --quiet to print only problems.   Exit code 1 if anything FAILs. WARN never fails.
// A deliverable that deviates from the brand book is reported here, it is not fixed silently.
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, args } from './lib.mjs';

const { flags, pos } = args();
const rel = (p) => path.relative(ROOT, p) || '.';
let fails = 0, warns = 0;
const out = (kind, msg) => { if (kind === 'FAIL') fails++; if (kind === 'WARN') warns++; if (kind !== 'PASS' || !flags.quiet) console.log(`  ${kind.padEnd(4)}  ${msg}`); };

const HEX = /^#([0-9a-f]{3}|[0-9a-f]{6})$/i;
const rgb = (h) => { let s = h.slice(1); if (s.length === 3) s = [...s].map((c) => c + c).join(''); const n = parseInt(s, 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
const lum = (h) => { const [r, g, b] = rgb(h); return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b); };
export const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
const readJson = (f) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) { out('FAIL', `${rel(f)}: not valid JSON (${e.message})`); return null; } };

function checkBook(file) {
  const b = readJson(file);
  if (!b) return null;
  console.log(`-- brand book ${rel(file)}`);
  const P = b.palette ?? {};
  for (const k of ['primary', 'background', 'ink']) if (!P[k]) out('FAIL', `palette.${k} is missing`);
  for (const [k, v] of Object.entries(P)) if (!HEX.test(v)) out('FAIL', `palette.${k} is not a #hex colour: ${v}`);
  let n = 0;
  for (const p of b.pairs ?? []) {
    const fg = P[p.fg], bg = P[p.bg];
    if (!fg || !bg) { out('FAIL', `pair ${p.fg} on ${p.bg}: unknown palette token`); continue; }
    const r = contrast(fg, bg), min = p.min ?? 4.5; n++;
    if (r >= min) out('PASS', `${p.fg} on ${p.bg} = ${r.toFixed(2)}:1 (needs ${min}) ${p.use ?? ''}`);
    else out('FAIL', `${p.fg} (${fg}) on ${p.bg} (${bg}) = ${r.toFixed(2)}:1, needs ${min} for ${p.use ?? 'this pair'}`);
  }
  if (n === 0) out('WARN', 'no contrast pairs listed');
  for (const [use, t] of Object.entries(b.type ?? {})) {
    if (typeof t !== 'object') continue;
    if (!t.family) out('FAIL', `type.${use}: family missing`);
    else if (!t.license) out('FAIL', `type.${use} (${t.family}): licence missing. Record it, and use only SIL OFL or Apache-2.0 fonts unless the owner said yes to a paid one`);
    else if (!/ofl|open font|apache|mit|public domain|owner-approved/i.test(t.license)) out('WARN', `type.${use} (${t.family}): licence "${t.license}" is not a known free licence. Ask the owner first`);
    else out('PASS', `type.${use}: ${t.family}, ${t.license}`);
  }
  if (!b.avatar?.minSizePx) out('WARN', 'avatar.minSizePx is not set (the smallest size the avatar must still read at)');
  if (!Array.isArray(b.changelog) || b.changelog.length === 0) out('FAIL', 'changelog is empty: every change needs a dated line');
  else if (b.changelog.some((c) => !c.date || !c.change || !c.approvedBy)) out('FAIL', 'changelog lines need date, change and approvedBy');
  if (!/^(draft|approved \d{4}-\d{2}-\d{2})$/.test(b.status ?? '')) out('FAIL', `status must be "draft" or "approved YYYY-MM-DD", got "${b.status}"`);
  else if (b.status === 'draft' && !/_template/.test(file)) out('WARN', 'brand book is still a draft: it is not approved by the owner yet');
  return b;
}

// Resolve a video config the way make.mjs does: the brand book wins over the config's own palette.
export function resolvePalette(cfg) {
  let P = { ...(cfg.palette ?? {}) }, b = null;
  if (cfg.brand) { const f = path.resolve(ROOT, cfg.brand); if (fs.existsSync(f)) { b = JSON.parse(fs.readFileSync(f, 'utf8')); P = { ...P, ...(b.palette ?? {}) }; } }
  return { P, b };
}

function checkConfig(file, books) {
  const cfg = readJson(file);
  if (!cfg) return;
  console.log(`-- config ${rel(file)}`);
  const { P, b } = resolvePalette(cfg);
  if (cfg.brand && !b) { out('FAIL', `config.brand points to ${cfg.brand}, which does not exist`); return; }
  if (b) out('PASS', `uses the brand book ${cfg.brand} (palette and fonts come from it)`);
  else if (books.length && !/doctor/.test(file)) out('WARN', 'config has no "brand" field, so it can drift from the brand book. Add "brand": "brand/<slug>/brand.json"');
  if (b) {
    for (const [k, v] of Object.entries(cfg.palette ?? {})) if (b.palette?.[k] && b.palette[k].toLowerCase() !== String(v).toLowerCase()) out('WARN', `config.palette.${k} ${v} differs from the brand book ${b.palette[k]}; the book wins`);
    const hf = cfg.fonts?.heading, bf = b.type?.heading?.family;
    if (hf && bf && hf !== bf) out('WARN', `config.fonts.heading "${hf}" differs from the brand book "${bf}"; the book wins`);
  }
  const bg = P.background ?? '#0B0D12';
  const dark = lum(bg) < 0.3;
  const ink = P.ink ?? (dark ? '#F5F7FA' : '#10131A');
  const c1 = contrast(ink, bg);
  out(c1 >= 4.5 ? 'PASS' : 'FAIL', `text ink ${ink} on background ${bg} = ${c1.toFixed(2)}:1 (needs 4.5)`);
  if (P.primary) {
    // src/theme.ts darkens a light primary by 35% when it is used as text on a light background; do the same here.
    const dk = (h) => '#' + rgb(h).map((v) => Math.round(v * 0.65).toString(16).padStart(2, '0')).join('');
    const tx = P.primaryText ?? (lum(P.primary) > 0.45 && !dark ? dk(P.primary) : P.primary);
    const c2 = contrast(tx, bg);
    out(c2 >= 3 ? 'PASS' : 'WARN', `accent words ${tx}${P.primaryText ? '' : ' (primary as text)'} on background = ${c2.toFixed(2)}:1 (needs 3; set palette.primaryText to a darker or lighter variant)`);
  }
  if (cfg.music?.file) out(cfg.music.credit?.license ? 'PASS' : 'FAIL', `music file ${cfg.music.file}: ${cfg.music.credit?.license ? 'credit recorded' : 'credit missing'}`);
  const long = (cfg.scenes ?? []).map((s, i) => [i + 1, s.headline ?? '']).filter(([, h]) => h.length > 45);
  for (const [i, h] of long) out('WARN', `scene ${i}: headline is ${h.length} characters (45 or fewer reads at 1080p)`);
}

// Does the Remotion project take its colours from the theme, not from hard-coded values?
function checkSource() {
  console.log('-- Remotion source uses theme tokens');
  const dir = path.join(ROOT, 'src');
  if (!fs.existsSync(dir)) return;
  const skip = new Set(['theme.ts', 'Avatar.tsx', 'Root.tsx']); // theme.ts holds the defaults; the avatar takes its own colour props; Root.tsx only has a Studio placeholder
  const hits = [];
  for (const f of fs.readdirSync(dir)) {
    if (!/\.(tsx?|jsx?)$/.test(f) || skip.has(f)) continue;
    const t = fs.readFileSync(path.join(dir, f), 'utf8').split('\n');
    t.forEach((line, i) => { if (/#[0-9a-fA-F]{6}\b/.test(line) && !/^\s*\/\//.test(line)) hits.push(`${f}:${i + 1}`); });
  }
  if (hits.length === 0) out('PASS', 'no hard-coded hex colours outside theme.ts, Avatar.tsx and Root.tsx');
  else out('WARN', `hard-coded hex colours (use a theme token so the brand book applies): ${hits.slice(0, 6).join(', ')}${hits.length > 6 ? ' ...' : ''}`);
}

const files = pos.map((p) => path.resolve(p));
let books = [], cfgs = [];
if (files.length) { books = files.filter((f) => /brand\.json$/.test(f)); cfgs = files.filter((f) => !/brand\.json$/.test(f)); }
else {
  const bd = path.join(ROOT, 'brand');
  if (fs.existsSync(bd)) for (const d of fs.readdirSync(bd)) { const f = path.join(bd, d, 'brand.json'); if (fs.existsSync(f)) books.push(f); }
  const cd = path.join(ROOT, 'configs');
  if (fs.existsSync(cd)) cfgs = fs.readdirSync(cd).filter((f) => f.endsWith('.json')).map((f) => path.join(cd, f));
}
console.log('== brand check ==');
const loaded = books.map(checkBook).filter(Boolean);
cfgs.forEach((f) => checkConfig(f, loaded.filter((b) => b.slug !== 'example-brand')));
if (!files.length) checkSource();
console.log(fails ? `\nBRAND CHECK FAIL: ${fails} problem(s), ${warns} warning(s). Report each one to the owner, and do not change the brand book to make a check pass.` : `\nBRAND CHECK PASS (${warns} warning(s))`);
process.exit(fails ? 1 : 0);
