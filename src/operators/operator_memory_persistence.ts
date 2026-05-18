import type { TraceIndex } from "./operator_trace_index";

export function serializeTraceIndex(
  index: TraceIndex
): string {
  return JSON.stringify(index, null, 2);
}

export function deserializeTraceIndex(
  raw: string
): TraceIndex {
  const parsed = JSON.parse(raw) as TraceIndex;

  if (!parsed.traces) {
    return { traces: {} };
  }

  return parsed;
}
