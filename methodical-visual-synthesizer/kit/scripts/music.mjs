#!/usr/bin/env node
// Procedural music bed. 100% synthesized by this script: no samples, no loops, no downloads, no third-party material.
// Soft electric-piano chords (ii7 V7 Imaj7 vi7), sub bass, a gentle kick and hat. Deterministic for a given (mood, bpm, seed, duration).
// usage: node scripts/music.mjs --out=work/bed.wav [--duration=60] [--mood=soft|warm|night|upbeat] [--bpm=76] [--seed=0]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { args, die } from './lib.mjs';

const SR = 48000;
export const MOODS = {
  soft: { root: 48, bpm: 76 },   // C
  warm: { root: 53, bpm: 74 },   // F
  night: { root: 50, bpm: 66 },  // D
  upbeat: { root: 55, bpm: 88 }, // G
};
const midi = (m) => 440 * 2 ** ((m - 69) / 12);
const rng = (seed) => { let s = (seed * 2654435761 + 12345) >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };

export function makeBed({ duration = 60, mood = 'soft', bpm, seed = 0, out }) {
  const m = MOODS[mood] ?? MOODS.soft;
  bpm = Number(bpm ?? m.bpm);
  const rand = rng(seed);
  const n = Math.ceil(duration * SR);
  const L = new Float32Array(n), R = new Float32Array(n);
  const beat = 60 / bpm, bar = beat * 4;
  const prog = [
    { off: 2, iv: [0, 3, 7, 10] },  // ii7
    { off: 7, iv: [0, 4, 7, 10] },  // V7
    { off: 0, iv: [0, 4, 7, 11] },  // Imaj7
    { off: 9, iv: [0, 3, 7, 10] },  // vi7
  ];
  const add = (buf, start, data) => { const s0 = Math.floor(start * SR); for (let i = 0; i < data.length && s0 + i < n; i++) buf[s0 + i] += data[i]; };

  const epiano = (f, dur, vel) => {
    const len = Math.floor((dur + 0.6) * SR), d = new Float32Array(len);
    for (let i = 0; i < len; i++) {
      const t = i / SR;
      const tine = Math.sin(2 * Math.PI * f * 7 * t) * Math.exp(-t * 22) * 0.9;  // short FM "tine" attack
      let v = Math.sin(2 * Math.PI * f * t + tine) + 0.28 * Math.sin(2 * Math.PI * f * 2 * t) * Math.exp(-t * 2.5) + 0.08 * Math.sin(2 * Math.PI * f * 3 * t) * Math.exp(-t * 6);
      const env = Math.min(1, t / 0.008) * Math.exp(-t * 1.1) * (t > dur ? Math.exp(-(t - dur) * 9) : 1);
      d[i] = v * env * vel * (1 + 0.04 * Math.sin(2 * Math.PI * 4.5 * t));
    }
    return d;
  };
  const bass = (f, dur) => {
    const len = Math.floor((dur + 0.2) * SR), d = new Float32Array(len);
    for (let i = 0; i < len; i++) {
      const t = i / SR;
      d[i] = Math.sin(2 * Math.PI * f * t) * Math.min(1, t / 0.02) * (t > dur ? Math.exp(-(t - dur) * 14) : 1) * 0.5;
    }
    return d;
  };
  const kick = () => {
    const len = Math.floor(0.35 * SR), d = new Float32Array(len); let ph = 0;
    for (let i = 0; i < len; i++) { const t = i / SR; ph += 2 * Math.PI * (45 + 90 * Math.exp(-t * 28)) / SR; d[i] = Math.sin(ph) * Math.exp(-t * 11) * 0.5; }
    return d;
  };
  const hat = () => {
    const len = Math.floor(0.05 * SR), d = new Float32Array(len); let prev = 0;
    for (let i = 0; i < len; i++) { const x = rand() * 2 - 1; d[i] = (x - prev) * Math.exp(-(i / SR) * 90) * 0.12; prev = x; } // crude high-pass
    return d;
  };
  const K = kick(), H = hat();

  const bars = Math.ceil(duration / bar) + 1;
  for (let b = 0; b < bars; b++) {
    const c = prog[b % 4], t0 = b * bar, root = m.root + c.off;
    c.iv.forEach((iv, k) => {
      const note = root + 12 + iv;
      const f = midi(note), delay = 0.012 * k + rand() * 0.01; // slight strum
      const d = epiano(f, bar * 0.92, 0.17);
      add(L, t0 + delay, d); add(R, t0 + delay + 0.011, d); // Haas-style stereo width
    });
    const bd = bass(midi(root - 12), beat * 1.8);
    add(L, t0, bd); add(R, t0, bd);
    add(L, t0, K); add(R, t0, K); add(L, t0 + beat * 2, K); add(R, t0 + beat * 2, K);
    for (let e = 0; e < 8; e++) { const sw = e % 2 ? beat * 0.06 : 0; add(L, t0 + e * beat / 2 + sw, H); add(R, t0 + e * beat / 2 + sw, H); }
  }
  // Warmth: one-pole low-pass at ~3 kHz, so little energy sits where consonants live.
  const lp = (x, fc) => { const a = (1 / SR) / (1 / (2 * Math.PI * fc) + 1 / SR); let y = 0; for (let i = 0; i < x.length; i++) { y += a * (x[i] - y); x[i] = y; } };
  lp(L, 3000); lp(R, 3000);
  // Normalise to a -3 dBFS peak, fade the first and last 0.5 s.
  let pk = 0; for (let i = 0; i < n; i++) pk = Math.max(pk, Math.abs(L[i]), Math.abs(R[i]));
  const g = pk > 0 ? 0.7 / pk : 1, fade = Math.floor(0.5 * SR);
  for (let i = 0; i < n; i++) { const f = Math.min(1, i / fade, (n - i) / fade); L[i] *= g * f; R[i] *= g * f; }
  // 16-bit stereo WAV
  const buf = Buffer.alloc(44 + n * 4);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 4, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22); buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
  buf.write('data', 36); buf.writeUInt32LE(n * 4, 40);
  for (let i = 0; i < n; i++) { buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, L[i])) * 32767), 44 + i * 4); buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, R[i])) * 32767), 46 + i * 4); }
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  fs.writeFileSync(out, buf);
  return { out, duration, mood, bpm, seed };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const { flags } = args();
  if (!flags.out) die('usage: node scripts/music.mjs --out=work/bed.wav [--duration=60] [--mood=soft|warm|night|upbeat] [--bpm=76] [--seed=0]');
  const r = makeBed({ duration: Number(flags.duration ?? 60), mood: flags.mood ?? 'soft', bpm: flags.bpm, seed: Number(flags.seed ?? 0), out: flags.out });
  console.log(`bed ${r.out} (${r.duration}s, mood ${r.mood}, ${r.bpm} bpm, seed ${r.seed}). Licence: generated by this script, free to use, no attribution needed (see LICENSES.md).`);
}
