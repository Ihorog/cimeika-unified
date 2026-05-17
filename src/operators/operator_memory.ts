import type { OperatorId } from "./operator_runtime_types";

export interface MemoryTrace {
  id: string;
  source: string;
  operators: OperatorId[];
  signature: string;
  attention: number;
  tension: number;
  resonance: number;
  stability: number;
  count: number;
}

export function createMemoryTrace(
  source: string,
  operators: OperatorId[],
  attention: number,
  tension: number,
  resonance: number,
  stability: number
): MemoryTrace {
  const signature = operators.join(".");

  return {
    id: `trace:${signature}`,
    source,
    operators,
    signature,
    attention,
    tension,
    resonance,
    stability,
    count: 1
  };
}

export function mergeTrace(
  existing: MemoryTrace,
  incoming: MemoryTrace
): MemoryTrace {
  const count = existing.count + 1;

  return {
    ...existing,
    attention: (existing.attention + incoming.attention) / 2,
    tension: (existing.tension + incoming.tension) / 2,
    resonance: (existing.resonance + incoming.resonance) / 2,
    stability: (existing.stability + incoming.stability) / 2,
    count
  };
}
