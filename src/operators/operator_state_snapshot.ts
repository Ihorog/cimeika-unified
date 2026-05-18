export interface StateSnapshot {
  timestamp: number;
  state: string;
  entropy: number;
  resonance: number;
}

export function createSnapshot(
  state: string,
  entropy: number,
  resonance: number
): StateSnapshot {
  return {
    timestamp: Date.now(),
    state,
    entropy,
    resonance
  };
}
