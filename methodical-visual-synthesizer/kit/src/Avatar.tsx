import React from 'react';
import { AbsoluteFill } from 'remotion';

// Code-drawn avatar: one glass object with an inner glow on a dark rounded plate. Pure SVG, no assets, no network.
// Motifs: triangle-arc | ring | lattice | beam | monogram. Add a motif by adding a case in <Motif/>.
export type AvatarProps = {
  motif?: 'triangle-arc' | 'ring' | 'lattice' | 'beam' | 'monogram';
  letter?: string; // for motif "monogram" (one character)
  glow?: string;
  deep?: string;
  highlight?: string;
  bg0?: string;
  bg1?: string;
  /** 0 to 1: how much of the arc, ring or lattice is lit. */
  progress?: number;
  /** Simplify (fewer fine details) for sizes at or below 64 px. Set by scripts/still.mjs. */
  small?: boolean;
};

export const avatarDefaults: Required<Omit<AvatarProps, 'letter'>> & { letter: string } = {
  motif: 'triangle-arc',
  letter: 'A',
  glow: '#5FD0FF',
  deep: '#1479B5',
  highlight: '#E3F6FF',
  bg0: '#14161B',
  bg1: '#1E2128',
  progress: 0.5,
  small: false,
};

const Motif: React.FC<Required<AvatarProps>> = (p) => {
  const cx = 512, cy = 512;
  switch (p.motif) {
    case 'ring': {
      const r = 250, sw = p.small ? 90 : 64, circ = 2 * Math.PI * r;
      return (
        <g transform={`rotate(-90 ${cx} ${cy})`}>
          <circle cx={cx} cy={cy} r={r} fill="none" stroke="url(#glass)" strokeWidth={sw} opacity={0.5} />
          <circle cx={cx} cy={cy} r={r} fill="none" stroke={p.glow} strokeWidth={sw * 0.55} strokeLinecap="round"
            strokeDasharray={`${circ * p.progress} ${circ}`} filter="url(#bloom)" />
        </g>
      );
    }
    case 'lattice': {
      const pts: [number, number][] = [];
      for (let j = 0; j < 3; j++) for (let i = 0; i < 3; i++) pts.push([cx + (i - 1) * 210, cy + (j - 1) * 210]);
      const lit = Math.min(8, Math.floor(p.progress * 9));
      const edges: [number, number][] = [[0, 1], [1, 2], [3, 4], [4, 5], [6, 7], [7, 8], [0, 3], [3, 6], [1, 4], [4, 7], [2, 5], [5, 8]];
      return (
        <g>
          {edges.map(([a, b], k) => (
            <line key={k} x1={pts[a][0]} y1={pts[a][1]} x2={pts[b][0]} y2={pts[b][1]} stroke={p.highlight} strokeOpacity={0.35} strokeWidth={p.small ? 22 : 10} />
          ))}
          {pts.map(([x, y], k) => (
            <circle key={k} cx={x} cy={y} r={k === lit ? 62 : 44} fill={k === lit ? p.glow : 'url(#glass)'} filter={k === lit ? 'url(#bloom)' : undefined} stroke={p.highlight} strokeOpacity={0.5} strokeWidth={4} />
          ))}
        </g>
      );
    }
    case 'beam': {
      return (
        <g>
          <polygon points="300,640 520,430 640,480 430,720" fill="url(#glass)" stroke={p.highlight} strokeOpacity={0.6} strokeWidth={6} />
          <path d="M520 430 L760 250" stroke={p.glow} strokeWidth={p.small ? 70 : 44} strokeLinecap="round" filter="url(#bloom)" />
          <path d="M640 480 L800 400" stroke={p.glow} strokeWidth={p.small ? 40 : 22} strokeLinecap="round" opacity={0.6} filter="url(#bloom)" />
        </g>
      );
    }
    case 'monogram': {
      return (
        <text x={cx} y={cy + 150} textAnchor="middle" fontFamily="'Inter','Helvetica Neue',Arial,sans-serif" fontWeight={800} fontSize={440} fill={p.glow} filter="url(#bloom)">
          {p.letter.slice(0, 1).toUpperCase()}
        </text>
      );
    }
    case 'triangle-arc':
    default: {
      // Glass set square with its right angle bottom-left, and one arc of light drawn part-way and stopped at a crosshair.
      const ox = 280, oy = 744, leg = 460;
      const R = 330, a1 = -Math.PI * 0.5 * Math.max(0.05, Math.min(1, p.progress)) * 0.9;
      const ex = ox + R * Math.cos(a1), ey = oy + R * Math.sin(a1);
      const ticks: React.ReactNode[] = [];
      if (!p.small) {
        for (let k = 1; k < 9; k++) {
          const t = (k / 9) * leg, len = k % 2 ? 22 : 38;
          ticks.push(<line key={'h' + k} x1={ox + t} y1={oy} x2={ox + t} y2={oy - len} stroke={p.highlight} strokeOpacity={0.55} strokeWidth={4} />);
          ticks.push(<line key={'v' + k} x1={ox} y1={oy - t} x2={ox + len} y2={oy - t} stroke={p.highlight} strokeOpacity={0.55} strokeWidth={4} />);
        }
      }
      const arcStart = ox + R, arcLarge = Math.abs(a1) > Math.PI ? 1 : 0;
      return (
        <g>
          <polygon points={`${ox},${oy} ${ox + leg},${oy} ${ox},${oy - leg}`} fill="url(#glass)" stroke={p.highlight} strokeOpacity={0.7} strokeWidth={p.small ? 14 : 6} strokeLinejoin="round" />
          {ticks}
          <path d={`M ${arcStart} ${oy} A ${R} ${R} 0 ${arcLarge} 0 ${ex} ${ey}`} fill="none" stroke={p.glow} strokeWidth={p.small ? 48 : 24} strokeLinecap="round" filter="url(#bloom)" />
          <g stroke={p.highlight} strokeWidth={p.small ? 14 : 6} strokeLinecap="round">
            <line x1={ex - 34} y1={ey} x2={ex + 34} y2={ey} />
            <line x1={ex} y1={ey - 34} x2={ex} y2={ey + 34} />
          </g>
        </g>
      );
    }
  }
};

export const Avatar: React.FC<AvatarProps> = (props) => {
  const p = { ...avatarDefaults, ...props } as Required<AvatarProps>;
  return (
    <AbsoluteFill style={{ background: 'transparent' }}>
      <svg width="100%" height="100%" viewBox="0 0 1024 1024">
        <defs>
          <linearGradient id="plate" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor={p.bg0} />
            <stop offset="1" stopColor={p.bg1} />
          </linearGradient>
          <radialGradient id="aura" cx="50%" cy="46%" r="55%">
            <stop offset="0" stopColor={p.glow} stopOpacity={0.30} />
            <stop offset="1" stopColor={p.glow} stopOpacity={0} />
          </radialGradient>
          <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor={p.highlight} stopOpacity={0.55} />
            <stop offset="0.5" stopColor={p.glow} stopOpacity={0.22} />
            <stop offset="1" stopColor={p.deep} stopOpacity={0.45} />
          </linearGradient>
          <filter id="bloom" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation={p.small ? 10 : 16} result="b" />
            <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        <rect width="1024" height="1024" rx="224" fill="url(#plate)" />
        <rect width="1024" height="1024" rx="224" fill="url(#aura)" />
        <Motif {...p} />
      </svg>
    </AbsoluteFill>
  );
};
