import { compileSymbol } from "./operator_symbol_compiler";
import { decideFromState } from "./operator_decision";
import { createMemoryTrace } from "./operator_memory";
import { recognizePattern } from "./operator_pattern";

export interface CognitionResult {
  source: string;
  pattern: string;
  description: string;
  decision: string;
  reason: string;
  confidence: number;
  signature: string;
}

export function processSymbolicInput(
  input: string
): CognitionResult {
  const compiled = compileSymbol(input);
  const pattern = recognizePattern(compiled.operators);
  const decision = decideFromState(compiled.state);

  const trace = createMemoryTrace(
    input,
    compiled.operators,
    compiled.state.attention,
    compiled.state.tension,
    compiled.state.resonance,
    compiled.state.stability
  );

  return {
    source: input,
    pattern: pattern.name,
    description: pattern.description,
    decision: decision.signal,
    reason: decision.reason,
    confidence: decision.confidence,
    signature: trace.signature
  };
}
