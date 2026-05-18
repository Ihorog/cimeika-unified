import { compileSymbol } from "./operator_symbol_compiler";
import { detectReaction } from "./operator_reaction";
import { calculateField } from "./operator_field";
import { predictNextState } from "./operator_prediction";
import { createMemoryTrace } from "./operator_memory";
import { evolveOperator } from "./operator_evolution";
import { calculateEntropy } from "./operator_entropy";
import { calculateFeedback } from "./operator_feedback";
import { createRuntimeCycle } from "./operator_cycle";

export interface RuntimeLoopResult {
  symbols: string[];
  prediction: string;
  entropy: number;
  stable: boolean;
  evolved: string;
  cycle: string;
}

export function runOperatorLoop(
  input: string
): RuntimeLoopResult {
  const compiled = compileSymbol(input);

  const field = calculateField(input);

  const prediction = predictNextState(input);

  const reaction = detectReaction(input);

  const trace = createMemoryTrace(
    input,
    compiled.operators,
    compiled.state.attention,
    compiled.state.tension,
    compiled.state.resonance,
    compiled.state.stability
  );

  const evolution = evolveOperator(
    input,
    trace.count
  );

  const entropy = calculateEntropy(
    compiled.operators
  );

  const feedback = calculateFeedback(
    reaction.intensity,
    field.tension
  );

  const cycle = createRuntimeCycle(
    trace.count
  );

  return {
    symbols: compiled.operators,
    prediction: prediction.probableState,
    entropy: entropy.entropy,
    stable: feedback.stable,
    evolved: evolution.current,
    cycle: cycle.phase
  };
}
