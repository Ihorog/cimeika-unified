export interface OperatorWave {
  amplitude: number;
  phase: number;
  resonance: number;
}

export function calculateWave(
  frequency: number,
  tension: number
): OperatorWave {
  const amplitude = frequency * (1 + tension);

  return {
    amplitude,
    phase: frequency % 1,
    resonance: amplitude * 0.5
  };
}
