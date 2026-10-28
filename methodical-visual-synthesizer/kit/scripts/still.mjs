#!/usr/bin/env node
// Code-drawn avatar (SVG via a Remotion still): free default for images. No generator, no credits, no network.
// usage: node scripts/still.mjs --out=out/avatar [--motif=triangle-arc|ring|lattice|beam|monogram] [--letter=A]
//          [--brand=brand/<slug>/brand.json  take the avatar colours and motif from the brand book]
//          [--glow=#5FD0FF --deep=#1479B5 --highlight=#E3F6FF --bg0=#14161B --bg1=#1E2128] [--progress=0.5] [--props=file.json]
// Writes <out>-1024.png (master) and native renders at 512, 256, 128, 48 and 32 px, plus <out>-check32.png
// (the 32 px render enlarged 8x with hard pixels, so you can look at it) and <out>-sheet.png (all sizes side by side on one row).
import path from 'node:path';
import fs from 'node:fs';
import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition } from '@remotion/renderer';
import { ROOT, args, mkdirp, run, die, applyBrand } from './lib.mjs';

const { flags } = args();
const base = path.resolve(ROOT, flags.out && flags.out !== true ? flags.out : 'out/avatar');
mkdirp(path.dirname(base));
mkdirp(ROOT, 'public');
const props = flags.props ? JSON.parse(fs.readFileSync(flags.props, 'utf8')) : {};
if (flags.brand && flags.brand !== true) Object.assign(props, applyBrand({ brand: flags.brand }).cfg.avatar ?? {}); // the brand book supplies the defaults; flags below still override
for (const k of ['motif', 'letter', 'glow', 'deep', 'highlight', 'bg0', 'bg1']) if (flags[k]) props[k] = flags[k];
if (flags.progress) props.progress = Number(flags.progress);

const t0 = Date.now();
const serveUrl = await bundle({ entryPoint: path.join(ROOT, 'src/index.ts'), publicDir: path.join(ROOT, 'public') });
const sizes = [1024, 512, 256, 128, 48, 32];
const files = [];
for (const size of sizes) {
  const inputProps = { ...props, small: size <= 64 }; // fewer fine details at tiny sizes
  const composition = await selectComposition({ serveUrl, id: 'Avatar', inputProps });
  const out = `${base}-${size}.png`;
  await renderStill({ composition, serveUrl, inputProps, output: out, scale: size / 1024 });
  files.push(out);
}
const [f1024, , , , , f32] = files;
await run('ffmpeg', ['-y', '-loglevel', 'error', '-i', f32, '-vf', 'scale=256:256:flags=neighbor', `${base}-check32.png`]);
// one-row contact sheet: 256, 128, 48 and 32 px shown at their real pixel size, over a mid-grey strip
const ins = [files[2], files[3], files[4], files[5]];
await run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'color=c=0x808080:s=520x280:d=1', ...ins.flatMap((f) => ['-i', f]),
  '-filter_complex', '[0][1]overlay=12:12[a];[a][2]overlay=280:12[b];[b][3]overlay=280:150[c];[c][4]overlay=340:150', '-frames:v', '1', `${base}-sheet.png`]);
if (!fs.existsSync(f1024)) die('avatar render failed');
console.log(`avatar set: ${files.map((f) => path.relative(ROOT, f)).join(', ')}\ncheck at 32 px (8x enlarged): ${path.relative(ROOT, base)}-check32.png\nsheet: ${path.relative(ROOT, base)}-sheet.png\ndone ${((Date.now() - t0) / 1000).toFixed(1)}s`);
