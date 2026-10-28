#!/usr/bin/env node
// One command: node scripts/make.mjs configs/<project>.json
//   narration (per sentence) -> timeline -> music bed -> ducked mix -> Remotion render -> mux  =>  out/<slug>.mp4 (1920x1080, 30 fps)
// Flags: --stills        only narration + one PNG per scene (fast layout check, no video)
//        --no-render     stop after the audio mix and timeline
//        --seconds=N     render only the first N seconds (used by doctor.sh)
//        --voice=Name    Phonon voice (default Harper)     --engine=auto|phonon|none   (none = silent narration, captions still shown)
//        --fresh         ignore the narration cache        --concurrency=N   --out=path.mp4
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { ROOT, args, die, makeLap, run, probeDur, slugify, mkdirp, applyBrand } from './lib.mjs';
import { narrate } from './narrate.mjs';
import { makeBed } from './music.mjs';
import { mix } from './mix.mjs';

process.chdir(ROOT);
const { flags, pos } = args();
const cfgPath = pos[0];
if (!cfgPath) die('usage: node scripts/make.mjs configs/<project>.json [--stills] [--no-render] [--seconds=N] [--engine=none]');
const lap = makeLap();
const FPS = 30;

// ---------- validate ----------
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
applyBrand(cfg); // optional "brand": "brand/<slug>/brand.json" makes the brand book the source of the palette, fonts and avatar colours
if (!cfg.project) die('config.project missing');
if (!Array.isArray(cfg.scenes) || cfg.scenes.length < 1) die('config.scenes needs at least one scene');
if (!cfg.closing?.headline) die('config.closing.headline missing (the closing card)');
cfg.palette ??= {};
for (const k of ['primary', 'accent', 'background', 'ink', 'surface']) {
  if (cfg.palette[k] && !/^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/.test(cfg.palette[k])) die(`palette.${k} must be a #hex colour, got ${cfg.palette[k]}`);
}
cfg.scenes.forEach((s, i) => { if (!s.headline || !s.narration) die(`scene ${i + 1} needs headline + narration`); });
if (cfg.music?.file && !(cfg.music.credit?.title && cfg.music.credit?.license && cfg.music.credit?.url)) {
  die('music.file needs music.credit {title, author, url, license}: record where a non-built-in track came from and under which licence (see README, Music).');
}
const slug = slugify(cfg.slug ?? cfg.project);
const WORK = mkdirp(ROOT, 'work', slug);
mkdirp(ROOT, 'out'); mkdirp(ROOT, 'public');
const OUT = path.resolve(flags.out && flags.out !== true ? flags.out : `out/${slug}.mp4`);

const closing = { headline: cfg.closing.headline, support: cfg.closing.support, accentWords: cfg.closing.accentWords, narration: cfg.closing.narration ?? cfg.closing.headline, visual: { type: 'none' } };
const scenes = [...cfg.scenes.map((s) => ({ ...s })), closing];

// Copy images used by scenes into public/ so Remotion can load them.
for (const s of scenes) {
  if (s.visual?.type === 'image') {
    const src = path.resolve(ROOT, s.visual.src ?? '');
    if (!fs.existsSync(src)) die(`image not found: ${s.visual.src}`);
    const name = `scene-${slug}-${path.basename(src)}`;
    fs.copyFileSync(src, path.join(ROOT, 'public', name));
    s.visual.file = name;
  }
}

// ---------- 1. narration ----------
lap(`Narration for ${scenes.length} scenes`);
const nar = await narrate({ scenes, voice: cfg.voice ?? {}, pronounce: cfg.pronounce ?? {}, workDir: WORK, fresh: !!flags.fresh, engine: flags.engine, voiceOverride: flags.voice });
lap(`Narration done: ${nar.clips} clips, engine ${nar.engine}${nar.engine === 'phonon' ? ', voice ' + nar.voice : ' (silent, captions only)'}`);

// ---------- 2. timeline ----------
const OV = 12, GAP = 0.28, TAIL = 0.4, CLOSE_TAIL = 1.7, LEAD0 = 0.7, LEAD = OV / FPS + 0.12;
const fr = (s) => Math.round(s * FPS);
const tl = { fps: FPS, overlapFrames: OV, scenes: [], captions: [], voice: [] };
const chunk = (text) => {
  const out = []; let cur = [];
  text.split(/\s+/).forEach((w, k, all) => {
    cur.push(w);
    if (cur.join(' ').length >= 44 || (/[,;:]$/.test(w) && cur.join(' ').length >= 16) || k === all.length - 1) { out.push(cur.join(' ')); cur = []; }
  });
  if (out.length > 1 && out[out.length - 1].length < 10) { const l = out.pop(); out[out.length - 1] += ' ' + l; }
  return out;
};
let cursor = 0;
scenes.forEach((s, i) => {
  const isLast = i === scenes.length - 1;
  const startSec = cursor / FPS;
  let t = startSec + (i === 0 ? LEAD0 : LEAD);
  for (const x of s._sent) {
    x.start = t; x.end = t + x.dur;
    if (nar.engine !== 'none') tl.voice.push({ file: x.file, start: x.start, dur: x.dur });
    const ch = chunk(x.text), wts = ch.map((c) => c.length), tot = wts.reduce((a, b) => a + b, 0);
    let c0 = x.start;
    ch.forEach((c, k) => { const d = (x.dur * wts[k]) / tot; tl.captions.push({ start: +c0.toFixed(3), end: +(k === ch.length - 1 ? x.end + 0.12 : c0 + d).toFixed(3), text: c }); c0 += d; });
    t = x.end + GAP;
  }
  const dur = fr(t - GAP - startSec + (isLast ? CLOSE_TAIL : TAIL));
  const { _sent, narration, ...pub } = s;
  tl.scenes.push({ startFrame: cursor, durFrames: dur, scene: pub });
  cursor += dur - (isLast ? 0 : OV);
});
const lastScene = tl.scenes[tl.scenes.length - 1];
tl.totalFrames = lastScene.startFrame + lastScene.durFrames;
const totalSec = tl.totalFrames / FPS;
fs.writeFileSync(path.join(WORK, 'props.json'), JSON.stringify({ cfg, timeline: tl }, null, 1));
fs.writeFileSync(path.join(WORK, 'timeline.json'), JSON.stringify(tl, null, 1));
lap(`Timeline: ${tl.scenes.length} scenes, ${totalSec.toFixed(1)} s (${tl.totalFrames} frames)`);

const conc = String(flags.concurrency ?? process.env.CONCURRENCY ?? Math.max(1, Math.min(4, os.cpus().length - 1)));

if (flags.stills) {
  await run('node', ['scripts/render.mjs', path.join(WORK, 'props.json'), path.join(WORK, 'stills'), '--stills']);
  console.log(`\nStills in ${path.join(WORK, 'stills')}`);
  process.exit(0);
}

// ---------- 3. music + mix ----------
let bed, credit;
if (cfg.music?.file) { bed = path.resolve(ROOT, cfg.music.file); credit = cfg.music.credit; if (!fs.existsSync(bed)) die(`music file not found: ${bed}`); }
else {
  bed = path.join(WORK, 'bed.wav');
  makeBed({ duration: Math.ceil(totalSec) + 2, mood: cfg.music?.mood ?? 'soft', seed: cfg.music?.seed ?? 0, out: bed });
  credit = { title: `built-in procedural bed (${cfg.music?.mood ?? 'soft'})`, author: 'scripts/music.mjs', url: 'n/a', license: 'generated by this kit, MIT, no attribution needed' };
}
fs.writeFileSync(path.join(WORK, 'music-credits.json'), JSON.stringify(credit, null, 1));
const MIX = path.join(WORK, 'mix.wav');
const clipSec = flags.seconds ? Math.min(totalSec, Number(flags.seconds)) : totalSec;
await mix({ voice: tl.voice, bed, totalSec: clipSec, bedGainDb: cfg.music?.gainDb ?? -9, out: MIX });
lap(`Audio mix done (bed ${path.basename(bed)}, ${tl.voice.length ? 'ducked under the voice' : 'no voice, bed only'})`);
if (flags['no-render']) { console.log('Stopped before render (--no-render). Mix at', MIX); process.exit(0); }

// ---------- 4. render ----------
const SILENT = path.join(WORK, 'silent.mp4');
lap(`Render 1920x1080@30, concurrency ${conc}${flags.seconds ? `, first ${flags.seconds} s only` : ''}`);
const rargs = ['scripts/render.mjs', path.join(WORK, 'props.json'), SILENT, `--concurrency=${conc}`];
if (flags.seconds) rargs.push(`--frames=0-${Math.round(Number(flags.seconds) * FPS) - 1}`);
const rp = spawn('node', rargs, { cwd: ROOT, stdio: ['ignore', 'pipe', 'pipe'] });
let errBuf = '', lastPct = -1;
const onData = (d) => { const m = String(d).match(/Rendered (\d+)%/g); if (m) { const pct = Number(m[m.length - 1].match(/\d+/)[0]); if (pct !== lastPct) { lastPct = pct; lap(`  render ${pct}%`); } } errBuf = (errBuf + d).slice(-3000); };
rp.stdout.on('data', onData); rp.stderr.on('data', onData);
const renderT0 = Date.now();
const code = await new Promise((r) => rp.on('close', r));
if (code !== 0 || !fs.existsSync(SILENT)) die(`Remotion render failed (exit ${code}). Last output:\n${errBuf}\nTip: retry with --concurrency=1, and run bash doctor.sh`);
const renderSec = (Date.now() - renderT0) / 1000;
lap(`Render done in ${renderSec.toFixed(1)} s`);

// ---------- 5. mux ----------
await run('ffmpeg', ['-y', '-loglevel', 'error', '-i', SILENT, '-i', MIX, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT]);
const d = probeDur(OUT);
lap(`DONE ${OUT}  (${d.toFixed(1)} s, ${(fs.statSync(OUT).size / 1e6).toFixed(1)} MB, narration ${nar.engine})`);
fs.writeFileSync(path.join(WORK, 'last-run.json'), JSON.stringify({ out: OUT, videoSeconds: d, renderSeconds: renderSec, narration: nar.engine, concurrency: conc }, null, 1));
