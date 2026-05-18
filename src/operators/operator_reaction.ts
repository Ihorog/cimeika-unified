export interface OperatorReaction {
  signal: string;
  field: string;
  intensity: number;
}

export function detectReaction(input: string): OperatorReaction {
  if (input.includes("∧")) {
    return {
      signal: "ASCEND",
      field: "FORWARD_EXPANSION",
      intensity: 0.9
    };
  }

  if (input.includes("∨")) {
    return {
      signal: "GROUND",
      field: "ROOT_STABILIZATION",
      intensity: 0.7
    };
  }

  if (input.includes("×")) {
    return {
      signal: "CONFLICT",
      field: "NODE_COLLISION",
      intensity: 0.95
    };
  }

  return {
    signal: "NEUTRAL",
    field: "STABLE_FIELD",
    intensity: 0.5
  };
}
