export interface OperatorTimeState {
  timestamp: number;
  phase: "init" | "rise" | "peak" | "fall" | "return" | "stable";
  age: number;
}

export function createTimeState(timestamp = Date.now()): OperatorTimeState {
  return {
    timestamp,
    phase: "init",
    age: 0
  };
}

export function resolvePhase(age: number): OperatorTimeState["phase"] {
  if (age < 1) return "init";
  if (age < 3) return "rise";
  if (age < 5) return "peak";
  if (age < 7) return "fall";
  if (age < 9) return "return";
  return "stable";
}
