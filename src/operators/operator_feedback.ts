export interface FeedbackState {
  stable: boolean;
  amplification: number;
  drift: number;
}

export function calculateFeedback(
  resonance: number,
  tension: number
): FeedbackState {
  const amplification = resonance * (1 + tension);
  const drift = tension - resonance;

  return {
    stable: drift <= 0,
    amplification,
    drift
  };
}
