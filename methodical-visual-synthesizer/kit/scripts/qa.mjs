#!/usr/bin/env node
// Measure a finished video and report it, so the handoff has numbers, not guesses.
//   node scripts/qa.mjs out/<slug>.mp4 [--lufs=-14] [--format=16:9|1:1|9:16] [--min-seconds=N]
// Reports size, frame rate, duration, audio, integrated loudness (LUFS), true peak (dBTP). Exit code 1 if a hard limit is broken.
// Loudness is measured on the FINAL file, not on the mix before it was muxed. Short clips (under 10 s) are not judged on loudness.
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import { args, die } from './lib.mjs';

const { flags, pos } = args();
const f = pos[0];
if (!f || !fs.existsSync(f)) die('usage: node scripts/qa.mjs out/<slug>.mp4 [--lufs=-14] [--format=16:9]');
const target = Number(flags.lufs ?? -14);
const probe = (a) => spawnSync('ffprobe', ['-v', 'error', ...a, f]).stdout.toString().trim();
const [w, h, rate] = probe(['-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate', '-of', 'csv=p=0']).split(',');
const [rn, rd] = (rate ?? '0/1').split('/').map(Number);
const fps = rd ? rn / rd : 0;
const dur = parseFloat(probe(['-show_entries', 'format=duration', '-of', 'csv=p=0']));
const acodec = probe(['-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0']);
let bad = 0, warn = 0;
const line = (k, m) => { if (k === 'FAIL') bad++; if (k === 'WARN') warn++; console.log(`  ${k.padEnd(4)}  ${m}`); };

console.log(`== qa ${f} ==`);
line('INFO', `${w}x${h}, ${fps.toFixed(2)} fps, ${dur.toFixed(1)} s, audio ${acodec || 'none'}, ${(fs.statSync(f).size / 1e6).toFixed(1)} MB`);
const want = { '16:9': '1920,1080', '1:1': '1080,1080', '9:16': '1080,1920', '4:5': '1080,1350' }[flags.format ?? '16:9'];
if (want && `${w},${h}` !== want) line('FAIL', `expected ${flags.format ?? '16:9'} (${want.replace(',', 'x')}), got ${w}x${h}`);
if (Math.abs(fps - 30) > 0.1) line('WARN', `frame rate is ${fps.toFixed(2)}, the kit renders at 30`);
if (!acodec) line('FAIL', 'no audio stream');
if (flags['min-seconds'] && dur < Number(flags['min-seconds'])) line('FAIL', `shorter than ${flags['min-seconds']} s`);
if (acodec) {
  const r = spawnSync('ffmpeg', ['-nostats', '-i', f, '-af', 'ebur128=peak=true', '-f', 'null', '-'], { encoding: 'utf8' });
  const sum = (r.stderr ?? '').split('Summary:').pop();
  const I = parseFloat((sum.match(/I:\s+(-?[\d.]+) LUFS/) ?? [])[1]);
  const TP = parseFloat((sum.match(/Peak:\s+(-?[\d.]+) dBFS/) ?? [])[1]);
  if (Number.isNaN(I)) line('WARN', 'could not measure loudness');
  else {
    line('INFO', `loudness ${I.toFixed(1)} LUFS (target ${target}), true peak ${Number.isNaN(TP) ? '?' : TP.toFixed(1)} dBTP (limit -1.5)`);
    if (dur >= 10 && Math.abs(I - target) > 1.5) line('FAIL', `loudness is ${(I - target).toFixed(1)} LU away from ${target}. Re-mix: a sparse voice track can miss the target in one pass, so run the loudness step again on the final mix`);
    else if (dur >= 10 && Math.abs(I - target) > 0.7) line('WARN', `loudness is ${(I - target).toFixed(1)} LU from the target`);
    if (!Number.isNaN(TP) && TP > -1.0) line('FAIL', `true peak ${TP.toFixed(1)} dBTP is above -1.5: it can clip after upload compression`);
  }
}
console.log(bad ? `QA FAIL (${bad})` : `QA PASS (${warn} warning(s))`);
process.exit(bad ? 1 : 0);
