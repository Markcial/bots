import { spring, useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';

/** 0 to 1 spring starting after `delay` frames (local scene frame). */
export const useSpring = (delay = 0, damping = 18, stiffness = 120) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping, stiffness, mass: 0.9 } });
};

export const ease = (frame: number, from: number, to: number, a = 0, b = 1) =>
  interpolate(frame, [from, to], [a, b], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.bezier(0.22, 1, 0.36, 1),
  });
