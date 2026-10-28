import React from 'react';
import { AbsoluteFill, Sequence, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { makeTheme, headlineSize, Theme } from './theme';
import { Background } from './Background';
import { Captions } from './Captions';
import { Avatar } from './Avatar';
import { ease, useSpring } from './anim';

export type Props = { cfg: any; timeline: any };

const Words: React.FC<{ text: string; size: number; theme: Theme; align?: 'left' | 'center'; delay?: number; accent?: string }> = ({
  text, size, theme: t, align = 'left', delay = 4, accent,
}) => {
  const words = text.split(/\s+/);
  const accentSet = new Set((accent ?? '').split(/\s+/).filter(Boolean));
  return (
    <div style={{ fontFamily: t.heading, fontWeight: t.headingWeight, fontSize: size, lineHeight: 1.04, letterSpacing: -size * 0.03, color: t.ink, textAlign: align, textWrap: 'balance' as any }}>
      {words.map((w, k) => {
        const s = useSpring(delay + k * 3, 16, 130);
        return (
          <span key={k} style={{ display: 'inline-block', marginRight: size * 0.24, opacity: Math.min(1, s * 1.6), transform: `translateY(${(1 - s) * 36}px)`, color: accentSet.has(w) ? t.primaryText : undefined }}>{w}</span>
        );
      })}
    </div>
  );
};

const Eyebrow: React.FC<{ text: string; theme: Theme }> = ({ text, theme: t }) => {
  const k = ease(useCurrentFrame(), 0, 16);
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 28, opacity: k }}>
      <div style={{ width: 44 * k, height: 4, borderRadius: 2, background: t.primary }} />
      <div style={{ fontFamily: t.body, fontWeight: 700, fontSize: 24, letterSpacing: 5, textTransform: 'uppercase', color: t.primaryText }}>{text}</div>
    </div>
  );
};

/** Optional visual on the right of a title scene: none | avatar | image (a file under public/, copied by make.mjs). */
const Visual: React.FC<{ v: any; cfg: any }> = ({ v, cfg }) => {
  const k = useSpring(8, 18, 100);
  if (!v || v.type === 'none') return null;
  const style = { width: 560, height: 560, opacity: k, transform: `scale(${0.9 + 0.1 * k})` } as const;
  if (v.type === 'avatar') return <div style={style}><Avatar {...(cfg.avatar ?? {})} {...(v.props ?? {})} /></div>;
  if (v.type === 'image' && v.file) {
    return <img src={staticFile(v.file)} style={{ ...style, objectFit: 'contain', borderRadius: 24 }} />;
  }
  return null;
};

const SceneView: React.FC<{ cfg: any; theme: Theme; scene: any; isFirst: boolean; isClosing: boolean; ov: number; dur: number }> = ({ cfg, theme: t, scene, isFirst, isClosing, ov, dur }) => {
  const frame = useCurrentFrame();
  const opIn = isFirst ? ease(frame, 0, 10) : ease(frame, 0, ov);
  const opOut = isClosing ? 1 : ease(frame, dur - ov, dur, 1, 0);
  const op = Math.min(opIn, opOut);
  const ty = isClosing ? 0 : ease(frame, dur - ov, dur, 0, -18);
  const headline: string = scene.headline ?? '';
  const eyebrow: string = scene.eyebrow ?? String(cfg.project ?? '').toUpperCase();
  const hasVisual = scene.visual && scene.visual.type && scene.visual.type !== 'none';

  let body: React.ReactNode;
  if (isClosing) {
    // Closing card: headline, support line, call-to-action pill.
    body = (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', gap: 40, textAlign: 'center' }}>
        <div style={{ maxWidth: 1480 }}><Words text={headline} size={headlineSize(headline, false) * 0.9} theme={t} align="center" delay={8} accent={scene.accentWords} /></div>
        {scene.support && <div style={{ fontFamily: t.body, fontWeight: 500, fontSize: 38, color: t.muted, maxWidth: 1200, opacity: ease(frame, 26, 42) }}>{scene.support}</div>}
        {cfg.closing?.cta && (
          <div style={{ padding: '20px 46px', borderRadius: 99, background: t.primary, color: t.onPrimary, fontFamily: t.heading, fontWeight: 800, fontSize: 34, opacity: ease(frame, 34, 50), transform: `translateY(${(1 - ease(frame, 34, 50)) * 14}px)` }}>{cfg.closing.cta}</div>
        )}
      </div>
    );
  } else if (hasVisual) {
    body = (
      <div style={{ display: 'flex', alignItems: 'center', height: '100%', gap: 70 }}>
        <div style={{ flex: 1 }}>
          <Eyebrow text={eyebrow} theme={t} />
          <Words text={headline} size={headlineSize(headline, true)} theme={t} accent={scene.accentWords} />
          {scene.support && <div style={{ fontFamily: t.body, fontWeight: 500, fontSize: 36, lineHeight: 1.35, color: t.muted, marginTop: 30, maxWidth: 740, opacity: ease(frame, 18, 34) }}>{scene.support}</div>}
        </div>
        <div style={{ flex: '0 0 560px', display: 'flex', justifyContent: 'center' }}><Visual v={scene.visual} cfg={cfg} /></div>
      </div>
    );
  } else {
    body = (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', textAlign: 'center' }}>
        <Eyebrow text={eyebrow} theme={t} />
        <div style={{ maxWidth: 1400 }}><Words text={headline} size={headlineSize(headline, false)} theme={t} align="center" accent={scene.accentWords} /></div>
        {scene.support && <div style={{ fontFamily: t.body, fontWeight: 500, fontSize: 40, color: t.muted, marginTop: 34, maxWidth: 1100, opacity: ease(frame, 18, 34) }}>{scene.support}</div>}
      </div>
    );
  }
  return (
    <AbsoluteFill style={{ opacity: op, transform: `translateY(${ty}px)` }}>
      <div style={{ position: 'absolute', left: 120, right: 120, top: 70, bottom: 190 }}>{body}</div>
    </AbsoluteFill>
  );
};

export const Video: React.FC<Props> = ({ cfg, timeline }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const theme = makeTheme(cfg);
  const scenes: any[] = timeline.scenes;
  const starts = scenes.map((s) => s.startFrame);
  const endFade = ease(frame, durationInFrames - 14, durationInFrames - 1);
  return (
    <AbsoluteFill style={{ background: theme.background }}>
      <Background theme={theme} sceneStarts={starts} />
      {scenes.map((s, i) => (
        <Sequence key={i} from={s.startFrame} durationInFrames={s.durFrames} layout="none">
          <SceneView cfg={cfg} theme={theme} scene={s.scene} isFirst={i === 0} isClosing={i === scenes.length - 1} ov={timeline.overlapFrames} dur={s.durFrames} />
        </Sequence>
      ))}
      <div style={{ position: 'absolute', left: 0, top: 0, height: 5, width: `${(frame / durationInFrames) * 100}%`, background: theme.primary, opacity: 0.9 }} />
      {cfg.subtitles !== false && <Captions caps={timeline.captions} theme={theme} />}
      <AbsoluteFill style={{ background: theme.background, opacity: endFade, pointerEvents: 'none' }} />
    </AbsoluteFill>
  );
};
