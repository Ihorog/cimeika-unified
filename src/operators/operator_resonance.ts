export interface ResonanceState {
  resonance: number;
  stability: number;
  tension: number;
}

export function detectResonance(input: string): ResonanceState {
  const resonance =
    (input.includes("○") ? 0.4 : 0) +
    (input.includes("+") ? 0.3 : 0) +
    (input.includes("∧") ? 0.3 : 0);

  const tension =
    (input.includes("-") ? 0.5 : 0) +
    (input.includes("×") ? 0.5 : 0);

  return {
    resonance,
    tension,
    stability: Math.max(0, resonance - tension)
  };
}
