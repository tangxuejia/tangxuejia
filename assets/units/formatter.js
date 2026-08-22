// RenoMetric Global Unit Engine - Formatter
export function formatUnit(value, digits=2) {
  return Number(value || 0).toLocaleString('en-US', {
    maximumFractionDigits: digits
  });
}

export function formatPair(metric, imperial, metricUnit, imperialUnit) {
  return `${formatUnit(metric)} ${metricUnit} (${formatUnit(imperial)} ${imperialUnit})`;
}
