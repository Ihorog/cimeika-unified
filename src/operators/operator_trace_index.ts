import type { MemoryTrace } from "./operator_memory";

export interface TraceIndex {
  traces: Record<string, MemoryTrace>;
}

export function createTraceIndex(): TraceIndex {
  return {
    traces: {}
  };
}

export function addTrace(
  index: TraceIndex,
  trace: MemoryTrace
): TraceIndex {
  const existing = index.traces[trace.signature];

  if (!existing) {
    index.traces[trace.signature] = trace;
    return index;
  }

  index.traces[trace.signature] = {
    ...existing,
    count: existing.count + 1,
    attention: (existing.attention + trace.attention) / 2,
    tension: (existing.tension + trace.tension) / 2,
    resonance: (existing.resonance + trace.resonance) / 2,
    stability: (existing.stability + trace.stability) / 2
  };

  return index;
}

export function findTrace(
  index: TraceIndex,
  signature: string
): MemoryTrace | null {
  return index.traces[signature] ?? null;
}

export function listTraces(index: TraceIndex): MemoryTrace[] {
  return Object.values(index.traces);
}
