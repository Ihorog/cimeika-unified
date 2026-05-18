import { compileSymbol } from "./operator_symbol_compiler";
import { detectReaction } from "./operator_reaction";
import { calculateField } from "./operator_field";
import { predictNextState } from "./operator_prediction";

export interface OperatorExecutionResult {
  symbols: string[];
  reaction: unknown;
  field: unknown;
  prediction: unknown;
}

export function executeOperatorSequence(
  input: string
): OperatorExecutionResult {
  const compiled = compileSymbol(input);

  return {
    symbols: compiled.operators,
    reaction: detectReaction(input),
    field: calculateField(input),
    prediction: predictNextState(input)
  };
}
