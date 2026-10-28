// Remotion Node-API renderer (used by make.mjs). node scripts/render.mjs <props.json> <out.mp4|dir> [--concurrency=N] [--frames=0-59] [--stills]
import path from 'node:path';
import fs from 'node:fs';
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import { ROOT, args, mkdirp } from './lib.mjs';

const { flags, pos } = args();
const [propsFile, out] = pos;
const inputProps = JSON.parse(fs.readFileSync(propsFile, 'utf8'));
const t0 = Date.now();
mkdirp(ROOT, 'public');
const serveUrl = await bundle({ entryPoint: path.join(ROOT, 'src/index.ts'), publicDir: path.join(ROOT, 'public') });
console.log(`bundled ${((Date.now() - t0) / 1000).toFixed(1)}s`);
const composition = await selectComposition({ serveUrl, id: 'Video', inputProps });
console.log(`composition ${composition.durationInFrames} frames`);

if (flags.stills) {
  // One PNG per scene, about 80 frames in, for a quick layout check before the full render.
  fs.mkdirSync(out, { recursive: true });
  const tl = inputProps.timeline;
  for (let i = 0; i < tl.scenes.length; i++) {
    const s = tl.scenes[i];
    const frame = Math.min(composition.durationInFrames - 1, s.startFrame + Math.min(Math.max(0, s.durFrames - 8), 80));
    await renderStill({ composition, serveUrl, inputProps, frame, output: path.join(out, `scene-${String(i + 1).padStart(2, '0')}.png`) });
  }
} else {
  let last = -1;
  const frameRange = flags.frames ? flags.frames.split('-').map(Number) : null;
  await renderMedia({
    composition, serveUrl, inputProps, outputLocation: out, codec: 'h264', crf: 20, pixelFormat: 'yuv420p',
    concurrency: Number(flags.concurrency ?? 4), muted: true, imageFormat: 'jpeg', jpegQuality: 88,
    ...(frameRange ? { frameRange: [frameRange[0], Math.min(frameRange[1], composition.durationInFrames - 1)] } : {}),
    onProgress: ({ progress }) => { const p = Math.floor(progress * 10) * 10; if (p !== last) { last = p; console.log(`Rendered ${p}%`); } },
  });
}
console.log(`render done ${((Date.now() - t0) / 1000).toFixed(1)}s`);
