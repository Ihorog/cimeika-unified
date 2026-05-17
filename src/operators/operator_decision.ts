import type { OperatorRuntimeState } from "./operator_runtime_types";

export type DecisionSignal =
  | "void"
  | "observe"
  | "stabilize"
  | "release_tension"
  | "confirm"
  | "materialize";

export interface OperatorDecision {
  signal: DecisionSignal;
  reason: string;
  confidence: number;
}

export function decideFromState(
  state: OperatorRuntimeState
): OperatorDecision {
  if (!state.active.length) {
    return {
      signal: "void",
      reason: "no_active_operators",
      confidence: 1
    };
  }

  if (state.tension > state.stability + 2) {
    return {
      signal: "release_tension",
      reason: "tension_exceeds_stability",
      confidence: 0.85
    };
  }

  if (state.stability >= 3 && state.fact) {
    return {
      signal: "materialize",
      reason: "stable_verified_fact",
      confidence: 0.9
    };
  }

  if (state.stability >= 2 && state.resonance >= 1) {
    return {
      signal: "confirm",
      reason: "stable_resonant_contour",
      confidence: 0.8
    };
  }

  if (state.attention >= 2 && state.tension > 0) {
    return {
      signal: "stabilize",
      reason: "attention_on_tension",
      confidence: 0.75
    };
  }

  return {
    signal: "observe",
    reason: "insufficient_resolution",
    confidence: 0.6
  };
}
