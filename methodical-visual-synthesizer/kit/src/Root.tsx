import React from 'react';
import { Composition, Still } from 'remotion';
import { Video, Props } from './Video';
import { Avatar, avatarDefaults } from './Avatar';

const demo: Props = {
  cfg: { project: 'Demo', palette: { primary: '#4F8CFF' } },
  timeline: { overlapFrames: 12, captions: [], scenes: [{ startFrame: 0, durFrames: 90, scene: { headline: 'Demo' } }], totalFrames: 90 },
};

export const Root: React.FC = () => (
  <>
    {/* 16:9 video. Scenes, captions and length come from the config via scripts/make.mjs. */}
    <Composition
      id="Video"
      component={Video as any}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={90}
      defaultProps={demo as any}
      calculateMetadata={({ props }: any) => ({ durationInFrames: props.timeline.totalFrames })}
    />
    {/* 1024 px square avatar. scripts/still.mjs also renders it natively at 512 / 256 / 128 / 48 / 32 px. */}
    <Still id="Avatar" component={Avatar as any} width={1024} height={1024} defaultProps={avatarDefaults as any} />
  </>
);
