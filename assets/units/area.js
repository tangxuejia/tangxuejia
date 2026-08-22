// RenoMetric Global Unit Engine - Area
export const areaUnits = {
  m2: 1,
  ft2: 10.7639104167,
  yd2: 1.1959900463
};

export function toM2(value, unit='m2') {
  return Number(value || 0) / areaUnits[unit];
}

export function fromM2(value, unit='m2') {
  return Number(value || 0) * areaUnits[unit];
}
