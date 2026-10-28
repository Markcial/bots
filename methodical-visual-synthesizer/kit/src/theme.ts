// Colour and type helpers. Everything derives from the config palette, so any project "just works".
export const hex = (h: string): [number, number, number] => {
  let s = h.replace('#', '').trim();
  if (s.length === 3) s = s.split('').map((c) => c + c).join('');
  const n = parseInt(s.slice(0, 6), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};
export const toHex = (r: number, g: number, b: number) =>
  '#' + [r, g, b].map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');
export const mix = (a: string, b: string, t: number) => {
  const A = hex(a), B = hex(b);
  return toHex(A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t, A[2] + (B[2] - A[2]) * t);
};
export const alpha = (h: string, a: number) => {
  const [r, g, b] = hex(h);
  return `rgba(${r},${g},${b},${a})`;
};
export const lum = (h: string) => {
  const f = (v: number) => {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  };
  const [r, g, b] = hex(h);
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};
export const contrastOn = (bg: string) => (lum(bg) > 0.42 ? '#0E1116' : '#FFFFFF');

export type Theme = ReturnType<typeof makeTheme>;

export const makeTheme = (cfg: any) => {
  const p = cfg.palette ?? {};
  const primary: string = p.primary ?? '#4F8CFF';
  const accent: string = p.accent ?? mix(primary, '#FFFFFF', 0.35);
  const background: string = p.background ?? '#0B0D12';
  const dark = lum(background) < 0.3;
  const ink: string = p.ink ?? (dark ? '#F5F7FA' : '#10131A');
  const surface: string = p.surface ?? (dark ? mix(background, '#FFFFFF', 0.07) : mix(background, '#FFFFFF', 0.7));
  const muted = mix(ink, background, 0.38);
  // Fonts: use a family installed on this computer, else the stack falls back to a generic sans-serif.
  const stack = (f: string) => `'${f}', 'Inter', 'Helvetica Neue', Arial, sans-serif`;
  return {
    dark,
    primary,
    accent,
    background,
    ink,
    surface,
    muted,
    onPrimary: p.onPrimary ?? contrastOn(primary),
    // text-safe version of primary when it sits on the background
    primaryText: p.primaryText ?? (lum(primary) > 0.45 && !dark ? mix(primary, '#000000', 0.35) : primary),
    heading: stack(cfg.fonts?.heading ?? 'Inter'),
    body: stack(cfg.fonts?.body ?? cfg.fonts?.heading ?? 'Inter'),
    headingWeight: cfg.fonts?.headingWeight ?? 800,
  };
};

export const headlineSize = (text: string, split: boolean) => {
  const n = text.length;
  if (split) return n <= 18 ? 108 : n <= 30 ? 92 : n <= 46 ? 78 : n <= 64 ? 66 : 58;
  return n <= 24 ? 132 : n <= 44 ? 108 : n <= 64 ? 90 : 76;
};
