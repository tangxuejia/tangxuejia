export const volumeToM3 = (value, unit) => {
  const map = { liter: 0.001, m3: 1, ft3: 0.0283168466, yd3: 0.764554858 };
  return value * (map[unit] ?? 1);
};

export const m3ToVolume = (value, unit) => {
  const map = { liter: 1000, m3: 1, ft3: 35.3146667, yd3: 1.30795062 };
  return value * (map[unit] ?? 1);
};
