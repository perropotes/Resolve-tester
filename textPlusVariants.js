/**
 * 20 variantes de entrada para "Text Plus".
 * Todas mantienen un estilo ejecutivo/profesional con transiciones suaves.
 * Cada variante usa una duración de entrada entre 6 y 12 frames.
 */

const textPlusVariants = [
  {
    id: 'executive-fade-up',
    entryFrames: 8,
    easing: 'easeOutCubic',
    from: { opacity: 0, y: 16, x: 0, scale: 1, rotate: 0, blur: 4 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'executive-fade-down',
    entryFrames: 8,
    easing: 'easeOutCubic',
    from: { opacity: 0, y: -14, x: 0, scale: 1, rotate: 0, blur: 3 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'executive-fade-right',
    entryFrames: 7,
    easing: 'easeOutQuad',
    from: { opacity: 0, y: 0, x: -18, scale: 1, rotate: 0, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'executive-fade-left',
    entryFrames: 7,
    easing: 'easeOutQuad',
    from: { opacity: 0, y: 0, x: 18, scale: 1, rotate: 0, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'soft-zoom-in',
    entryFrames: 9,
    easing: 'easeOutCubic',
    from: { opacity: 0, y: 6, x: 0, scale: 0.96, rotate: 0, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'micro-pop',
    entryFrames: 6,
    easing: 'easeOutBackSoft',
    from: { opacity: 0, y: 4, x: 0, scale: 0.94, rotate: 0, blur: 1 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'precision-rise',
    entryFrames: 10,
    easing: 'easeOutExpoSoft',
    from: { opacity: 0, y: 20, x: 0, scale: 1, rotate: 0, blur: 5 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'gentle-drop',
    entryFrames: 10,
    easing: 'easeOutExpoSoft',
    from: { opacity: 0, y: -20, x: 0, scale: 1, rotate: 0, blur: 5 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'clarity-focus',
    entryFrames: 11,
    easing: 'easeOutSine',
    from: { opacity: 0, y: 8, x: 0, scale: 1, rotate: 0, blur: 6 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'boardroom-slide-up',
    entryFrames: 12,
    easing: 'easeOutQuart',
    from: { opacity: 0, y: 24, x: 0, scale: 1, rotate: 0, blur: 3 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'boardroom-slide-right',
    entryFrames: 12,
    easing: 'easeOutQuart',
    from: { opacity: 0, y: 0, x: -24, scale: 1, rotate: 0, blur: 3 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'balanced-lift',
    entryFrames: 9,
    easing: 'easeOutCubic',
    from: { opacity: 0, y: 12, x: 0, scale: 0.985, rotate: 0, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'balanced-settle',
    entryFrames: 9,
    easing: 'easeOutCubic',
    from: { opacity: 0, y: -12, x: 0, scale: 0.985, rotate: 0, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'silk-pan-left',
    entryFrames: 8,
    easing: 'easeOutSine',
    from: { opacity: 0, y: 0, x: 14, scale: 1, rotate: 0, blur: 1 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'silk-pan-right',
    entryFrames: 8,
    easing: 'easeOutSine',
    from: { opacity: 0, y: 0, x: -14, scale: 1, rotate: 0, blur: 1 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'minimal-tilt-rise',
    entryFrames: 10,
    easing: 'easeOutQuad',
    from: { opacity: 0, y: 16, x: 0, scale: 1, rotate: -1.2, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'minimal-tilt-drop',
    entryFrames: 10,
    easing: 'easeOutQuad',
    from: { opacity: 0, y: -16, x: 0, scale: 1, rotate: 1.2, blur: 2 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'steady-reveal',
    entryFrames: 6,
    easing: 'easeOutLinearSoft',
    from: { opacity: 0, y: 6, x: 0, scale: 1, rotate: 0, blur: 0 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'premium-focus-rise',
    entryFrames: 11,
    easing: 'easeOutQuint',
    from: { opacity: 0, y: 18, x: 0, scale: 0.98, rotate: 0, blur: 4 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
  {
    id: 'premium-focus-slide',
    entryFrames: 11,
    easing: 'easeOutQuint',
    from: { opacity: 0, y: 0, x: -20, scale: 0.98, rotate: 0, blur: 4 },
    to: { opacity: 1, y: 0, x: 0, scale: 1, rotate: 0, blur: 0 },
  },
];

function getTextPlusVariants() {
  return textPlusVariants;
}

module.exports = {
  textPlusVariants,
  getTextPlusVariants,
};
