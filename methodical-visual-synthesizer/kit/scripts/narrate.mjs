#!/usr/bin/env node
// Narration: one clip per sentence, so a line can change without re-recording the rest.
// Engines:
//   phonon  Free, local, offline TTS: `uvx ptts` (Phonon 31m, Apache-2.0). Needs `uv` (setup.sh --with-tts) and a one-time ~60 MB model download.
//   none    Silent fallback. Each clip is silence, as long as the sentence would take to read (2.6 words/s). Captions still show.
//   auto    (default) phonon if `uvx` exists and a probe works, else none, with a warning.
// usage as a CLI: node scripts/narrate.mjs "A sentence." [--voice=Harper] [--engine=auto|phonon|none] [--out=work/narration-test.wav]
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { ROOT, run, have, probeDur, args, mkdirp } from './lib.mjs';

export const DEFAULT_VOICE = 'Harper';
const hfHome = () => process.env.HF_HOME ?? path.join(ROOT, '.cache', 'hf');

export const sentences = (t) =>
  (t.replace(/\s+/g, ' ').trim().match(/[^.!?]+[.!?]+["')\]]*|[^.!?]+$/g) ?? []).map((s) => s.trim()).filter(Boolean);

const silence = (file, sec) => run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=mono', '-t', sec.toFixed(2), file]);

const phononClip = async (text, voice, seed, out) => {
  const bin = process.env.UVX ?? 'uvx';
  let lastErr;
  for (let a = 0; a < 3; a++) {
    try {
      await run(bin, ['ptts', '--lang', 'en', '--quant', 'q8', '--voice', voice, '-s', String(seed), '--threads', '2', text, '-o', out], { env: { HF_HOME: hfHome() } });
      if (fs.existsSync(out)) return;
    } catch (e) { lastErr = e; }
  }
  throw lastErr ?? new Error('phonon produced no file');
};

/** Decide the engine. Returns 'phonon' or 'none' (and says why when it falls back). */
export const pickEngine = async (want = 'auto', voice = DEFAULT_VOICE) => {
  if (want === 'none') return 'none';
  if (!have(process.env.UVX ?? 'uvx')) {
    if (want === 'phonon') throw new Error('engine phonon needs `uvx` (install uv: run setup.sh --with-tts)');
    console.warn('WARN: `uvx` not found, so narration is SILENT (captions still shown). Run setup.sh --with-tts to enable the free voice.');
    return 'none';
  }
  const probe = path.join(mkdirp(ROOT, 'work'), 'tts-probe.wav');
  try { await phononClip('Check.', voice, 0, probe); return 'phonon'; }
  catch (e) {
    if (want === 'phonon') throw e;
    console.warn(`WARN: Phonon failed (${e.message.split('\n')[0]}), so narration is SILENT. Run doctor.sh for details.`);
    return 'none';
  }
};

/**
 * scenes: [{narration}], returns the same scenes with ._sent = [{text, i, j, file, dur}]
 * voice: {name, seed, engine}, pronounce: {Word: "Respelling"} (spoken only; captions keep the real spelling)
 */
export async function narrate({ scenes, voice = {}, pronounce = {}, workDir, fresh = false, engine: engineOverride, voiceOverride }) {
  const name = voiceOverride ?? voice.name ?? DEFAULT_VOICE, seed = voice.seed ?? 7;
  const engine = await pickEngine(engineOverride ?? voice.engine ?? 'auto', name);
  mkdirp(workDir, 'tts'); mkdirp(workDir, 'voice');
  const spoken = (t) => Object.entries(pronounce).reduce((s, [k, v]) => s.replace(new RegExp(`\\b${k}\\b`, 'g'), v), t);
  const jobs = [];
  scenes.forEach((s, i) => { s._sent = sentences(s.narration).map((text, j) => ({ text, i, j })); s._sent.forEach((x) => jobs.push(x)); });
  let next = 0;
  const worker = async () => {
    while (next < jobs.length) {
      const job = jobs[next++];
      const out = path.join(workDir, 'voice', `s${job.i}-${job.j}.wav`);
      if (engine === 'none') {
        const words = job.text.split(/\s+/).length;
        job.dur = Math.max(0.9, words / 2.6);
        await silence(out, job.dur);
      } else {
        const sp = spoken(job.text);
        const h = crypto.createHash('md5').update(`${name}|${seed}|${sp}`).digest('hex').slice(0, 12);
        const raw = path.join(workDir, 'tts', `${h}.wav`);
        if (fresh || !fs.existsSync(raw)) await phononClip(sp, name, seed, raw);
        // trim leading/trailing silence, mono 48 kHz
        await run('ffmpeg', ['-y', '-loglevel', 'error', '-i', raw, '-af',
          'silenceremove=start_periods=1:start_threshold=-48dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-48dB:start_silence=0.06,areverse,aresample=48000,aformat=channel_layouts=mono', out]);
        job.dur = probeDur(out);
        if (!(job.dur > 0.2)) throw new Error(`TTS produced empty audio for: "${sp}"`);
      }
      job.file = out;
    }
  };
  // Run the voice jobs one or two at a time: heavy jobs should not pile up on a shared computer.
  await Promise.all(Array.from({ length: Math.min(engine === 'none' ? 4 : 2, jobs.length) }, worker));
  return { engine, voice: name, clips: jobs.length };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const { flags, pos } = args();
  const text = pos.join(' ') || 'This is a narration test.';
  const dir = mkdirp(ROOT, 'work', '_narrate');
  const scenes = [{ narration: text }];
  const r = await narrate({ scenes, workDir: dir, engine: flags.engine, voiceOverride: flags.voice });
  const f = scenes[0]._sent.map((x) => x.file);
  const out = path.resolve(flags.out ?? path.join(ROOT, 'work', 'narration-test.wav'));
  await run('ffmpeg', ['-y', '-loglevel', 'error', ...f.flatMap((x) => ['-i', x]), '-filter_complex', `concat=n=${f.length}:v=0:a=1`, out]);
  console.log(`engine=${r.engine} voice=${r.voice} -> ${out} (${probeDur(out).toFixed(2)}s)`);
}
