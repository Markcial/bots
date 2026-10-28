import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { Theme } from './theme';

export type Cap = { start: number; end: number; text: string };

export const Captions: React.FC<{ caps: Cap[]; theme: Theme }> = ({ caps, theme }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const a = caps.find((c) => t >= c.start && t < c.end);
  if (!a) return null;
  const k = Math.min(1, (t - a.start) / 0.12);
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 64 }}>
      <div
        style={{
          maxWidth: 1500,
          padding: '14px 32px',
          borderRadius: 16,
          background: 'rgba(10,12,16,0.80)',
          color: '#fff',
          fontFamily: theme.body,
          fontWeight: 600,
          fontSize: 40,
          lineHeight: 1.25,
          textAlign: 'center',
          letterSpacing: -0.2,
          opacity: k,
          transform: `translateY(${(1 - k) * 8}px)`,
        }}
      >
        {a.text}
      </div>
    </AbsoluteFill>
  );
};
