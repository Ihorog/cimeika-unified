export interface OperatorMetrics {
  entropy: number;
  resonance: number;
  tension: number;
  stability: number;
  activity: number;
}

export function calculateMetrics(
  entropy: number,
  resonance: number,
  tension: number,
  stability: number
): OperatorMetrics {
  return {
    entropy,
    resonance,
    tension,
    stability,
    activity:
      resonance + stability - tension
  };
}
