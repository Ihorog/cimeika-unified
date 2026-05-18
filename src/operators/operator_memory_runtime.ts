import { compileSymbol } from "./operator_symbol_compiler";
import { createMemoryTrace } from "./operator_memory";
import {
  addTrace,
  createTraceIndex,
  type TraceIndex
} from "./operator_trace_index";

export function recordSymbolicInput(
  input: string,
  index: TraceIndex = createTraceIndex()
): TraceIndex {
  const compiled = compileSymbol(input);

  const trace = createMemoryTrace(
    input,
    compiled.operators,
    compiled.state.attention,
    compiled.state.tension,
    compiled.state.resonance,
    compiled.state.stability
  );

  return addTrace(index, trace);
}
