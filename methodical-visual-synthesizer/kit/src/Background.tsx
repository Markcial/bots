import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { Theme, alpha, mix } from './theme';

// Persistent brand backdrop: slow glow that migrates scene to scene, fine dot grid, drifting geometry.
const SHAPES = [
  { kind: 'ring', x: 8, y: 14, s: 150, c: 0, sp: 0.05, ph: 0 },
  { kind: 'plus', x: 91, y: 12, s: 70, c: 1, sp: -0.08, ph: 1.2 },
  { kind: 'square', x: 94, y: 62, s: 120, c: 0, sp: 0.04, ph: 2.1 },
  { kind: 'dots', x: 5, y: 66, s: 120, c: 1, sp: 0, ph: 3.3 },
  { kind: 'ring', x: 83, y: 88, s: 90, c: 1, sp: -0.06, ph: 4.2 },
  { kind: 'tri', x: 14, y: 90, s: 80, c: 0, sp: 0.07, ph: 5.0 },
] as const;

const Shape: React.FC<{ kind: string; s: number; color: string }> = ({ kind, s, color }) => {
  const sw = 3;
  switch (kind) {
    case 'ring':
      return <svg width={s} height={s}><circle cx={s / 2} cy={s / 2} r={s / 2 - sw} fill="none" stroke={color} strokeWidth={sw} /></svg>;
    case 'plus':
      return <svg width={s} height={s}><path d={`M${s / 2} 4V${s - 4}M4 ${s / 2}H${s - 4}`} stroke={color} strokeWidth={sw + 1} strokeLinecap="round" /></svg>;
    case 'square':
      return <svg width={s} height={s}><rect x={sw} y={sw} width={s - 2 * sw} height={s - 2 * sw} rx={s * 0.18} fill="none" stroke={color} strokeWidth={sw} /></svg>;
    case 'tri':
      return <svg width={s} height={s}><path d={`M${s / 2} 6L${s - 6} ${s - 8}H6Z`} fill="none" stroke={color} strokeWidth={sw} strokeLinejoin="round" /></svg>;
    default:
      return (
        <svg width={s} height={s}>
          {Array.from({ length: 25 }).map((_, i) => (
            <circle key={i} cx={10 + (i % 5) * ((s - 20) / 4)} cy={10 + Math.floor(i / 5) * ((s - 20) / 4)} r={2.4} fill={color} />
          ))}
        </svg>
      );
  }
};

export const Background: React.FC<{ theme: Theme; sceneStarts: number[] }> = ({ theme, sceneStarts }) => {
  const frame = useCurrentFrame();
  const glowPos = [
    [70, 30], [25, 60], [75, 70], [40, 30], [80, 45], [30, 75], [65, 25], [50, 50],
  ];
  const xs = sceneStarts.map((_, i) => glowPos[i % glowPos.length][0]);
  const ys = sceneStarts.map((_, i) => glowPos[i % glowPos.length][1]);
  const gx = sceneStarts.length > 1 ? interpolate(frame, sceneStarts, xs, { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) : 60;
  const gy = sceneStarts.length > 1 ? interpolate(frame, sceneStarts, ys, { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) : 40;
  const cols = [theme.primary, theme.accent];
  const g2 = mix(theme.primary, theme.accent, 0.5);
  return (
    <AbsoluteFill style={{ background: theme.background }}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(1100px 800px at ${gx}% ${gy}%, ${alpha(theme.primary, theme.dark ? 0.22 : 0.16)}, transparent 70%), radial-gradient(900px 700px at ${100 - gx}% ${100 - gy}%, ${alpha(g2, theme.dark ? 0.12 : 0.10)}, transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(${alpha(theme.ink, theme.dark ? 0.10 : 0.09)} 1.4px, transparent 1.6px)`,
          backgroundSize: '44px 44px',
          backgroundPosition: `${(frame * 0.15) % 44}px 0`,
          WebkitMaskImage: 'radial-gradient(ellipse at 50% 45%, transparent 35%, black 100%)',
          maskImage: 'radial-gradient(ellipse at 50% 45%, transparent 35%, black 100%)',
        }}
      />
      {SHAPES.map((sh, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${sh.x}%`,
            top: `${sh.y}%`,
            opacity: theme.dark ? 0.28 : 0.30,
            transform: `translate(-50%,-50%) translate(${Math.sin(frame / 90 + sh.ph) * 14}px, ${Math.cos(frame / 110 + sh.ph) * 18}px) rotate(${frame * sh.sp}deg)`,
          }}
        >
          <Shape kind={sh.kind} s={sh.s} color={cols[sh.c]} />
        </div>
      ))}
    </AbsoluteFill>
  );
};
