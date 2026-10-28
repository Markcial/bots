// Audio mix: voice clips placed on a timeline, a music bed ducked under the voice (sidechain), loudness normalised.
// Exported function used by make.mjs. Targets -14 LUFS / -1.5 dBTP overall (voice alone is normalised to -16 first).
import { run } from './lib.mjs';

export async function mix({ voice, bed, totalSec, bedGainDb = -9, out }) {
  const T = totalSec.toFixed(3);
  const inputs = [], fc = [];
  if (voice.length === 0) {
    // No audible voice (silent fallback): just the bed.
    inputs.push('-i', bed);
    fc.push(`[0:a]atrim=0:${T},asetpts=N/SR/TB,aformat=channel_layouts=stereo,volume=${bedGainDb + 4}dB,afade=t=in:d=1.5,afade=t=out:st=${Math.max(0, totalSec - 3.2).toFixed(2)}:d=3.2,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]`);
  } else {
    voice.forEach((v, k) => { inputs.push('-i', v.file); fc.push(`[${k}:a]adelay=${Math.round(v.start * 1000)}:all=1[v${k}]`); });
    const n = voice.length;
    fc.push(`${voice.map((_, k) => `[v${k}]`).join('')}amix=inputs=${n}:normalize=0:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=${T},atrim=0:${T},asplit=2[vsc][vmix]`);
    inputs.push('-i', bed);
    fc.push(`[${n}:a]atrim=0:${T},asetpts=N/SR/TB,aformat=channel_layouts=stereo,volume=${bedGainDb}dB,afade=t=in:d=1.5,afade=t=out:st=${Math.max(0, totalSec - 3.2).toFixed(2)}:d=3.2[bed]`);
    // Duck: the bed drops when the voice is present, and comes back after about 0.6 s.
    fc.push('[bed][vsc]sidechaincompress=threshold=0.015:ratio=9:attack=40:release=600:makeup=1[ducked]');
    fc.push('[ducked][vmix]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]');
  }
  await run('ffmpeg', ['-y', '-loglevel', 'error', ...inputs, '-filter_complex', fc.join(';'), '-map', '[out]', '-t', T, out]);
  return out;
}
