// Shared helpers for the kit scripts. Node 18+, no dependencies.
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

export const makeLap = () => {
  const t0 = Date.now();
  return (m) => console.log(`[${((Date.now() - t0) / 1000).toFixed(1).padStart(6)}s] ${m}`);
};

export const die = (m) => { console.error('\nERROR: ' + m); process.exit(1); };

/** Run a command, resolve with {out, err}, reject with a short error that includes the tail of stderr. */
export const run = (cmd, args, opt = {}) => new Promise((res, rej) => {
  const p = spawn(cmd, args, { cwd: opt.cwd ?? ROOT, env: { ...process.env, ...(opt.env ?? {}) }, stdio: ['ignore', 'pipe', 'pipe'] });
  let out = '', err = '';
  p.stdout.on('data', (d) => (out += d));
  p.stderr.on('data', (d) => (err += d));
  p.on('error', (e) => rej(new Error(`${cmd}: ${e.message}`)));
  p.on('close', (c) => (c === 0 ? res({ out, err }) : rej(new Error(`${cmd} ${args.slice(0, 5).join(' ')} ... exit ${c}\n${err.slice(-1500)}`))));
});

export const have = (cmd) => spawnSync('sh', ['-c', `command -v ${cmd}`], { stdio: 'ignore' }).status === 0;

export const probeDur = (f) =>
  parseFloat(spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).stdout.toString());

export const args = (argv = process.argv.slice(2)) => {
  const flags = {}, pos = [];
  for (const a of argv) {
    if (a.startsWith('--')) { const [k, ...v] = a.slice(2).split('='); flags[k] = v.length ? v.join('=') : true; }
    else pos.push(a);
  }
  return { flags, pos };
};

export const slugify = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

export const mkdirp = (...p) => { const d = path.join(...p); fs.mkdirSync(d, { recursive: true }); return d; };

/** Apply a brand book (brand/<slug>/brand.json) to a video config: the book wins over the config's own palette, fonts and avatar colours.
 *  Returns {cfg, book} (book is null when the config has no "brand" field). Prints a warning if the book is not approved yet. */
export const applyBrand = (cfg, warn = (m) => console.warn(m)) => {
  if (!cfg.brand) return { cfg, book: null };
  const f = path.resolve(ROOT, cfg.brand);
  if (!fs.existsSync(f)) die(`config.brand points to ${cfg.brand}, which does not exist. Create it from brand/_template/ (skill brand-book).`);
  const book = JSON.parse(fs.readFileSync(f, 'utf8'));
  if (!/^approved /.test(book.status ?? '')) warn(`WARN: brand book ${cfg.brand} is "${book.status}", not approved by the owner yet.`);
  cfg.palette = { ...(cfg.palette ?? {}), ...(book.palette ?? {}) };
  const h = book.type?.heading, b = book.type?.body;
  cfg.fonts = { ...(cfg.fonts ?? {}), ...(h?.family ? { heading: h.family } : {}), ...(h?.weight ? { headingWeight: h.weight } : {}), ...(b?.family ? { body: b.family } : {}) };
  if (book.avatar?.props) cfg.avatar = { ...(cfg.avatar ?? {}), ...book.avatar.props };
  if (book.voice?.pronounce) cfg.pronounce = { ...(book.voice.pronounce), ...(cfg.pronounce ?? {}) };
  return { cfg, book };
};
