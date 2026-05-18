export interface FrequencyField {
  rhythm: number;
  repetition: number;
  strength: number;
}

export function calculateFrequencyField(repetition: number): FrequencyField {
  return {
    rhythm: repetition > 0 ? 1 / repetition : 0,
    repetition,
    strength: Math.min(1, repetition / 12)
  };
}
