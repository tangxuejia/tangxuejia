export const lengthToM = (value, unit) => {
  const map = { mm: 0.001, cm: 0.01, m: 1, in: 0.0254, ft: 0.3048 };
  return value * (map[unit] ?? 1);
};

export const mToLength = (value, unit) => {
  const map = { mm: 1000, cm: 100, m: 1, in: 39.3700787, ft: 3.2808399 };
  return value * (map[unit] ?? 1);
};
