// RenoMetric Global Unit Engine - Weight
export const weightUnits = {
  kg: 1,
  lb: 2.2046226218
};

export function toKg(value, unit='kg') {
  return Number(value || 0) / weightUnits[unit];
}

export function fromKg(value, unit='kg') {
  return Number(value || 0) * weightUnits[unit];
}
