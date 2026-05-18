export interface PredictionResult {
  probableState: string;
  confidence: number;
}

export function predictNextState(input: string): PredictionResult {
  if (input.includes("Y")) {
    return {
      probableState: "BRANCH_EXPANSION",
      confidence: 0.84
    };
  }

  if (input.includes("↺")) {
    return {
      probableState: "CYCLIC_RETURN",
      confidence: 0.91
    };
  }

  if (input.includes("+")) {
    return {
      probableState: "CONFIRMED_ALIGNMENT",
      confidence: 0.88
    };
  }

  return {
    probableState: "UNDEFINED_TRANSITION",
    confidence: 0.4
  };
}
