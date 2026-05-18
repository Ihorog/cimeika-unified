import type { MemoryTrace } from "./operator_memory";

export interface PatternSummary {
  signature: string;
  count: number;
  averageAttention: number;
  averageTension: number;
  averageResonance: number;
  averageStability: number;
}

export function summarizePatterns(
  traces: MemoryTrace[]
): PatternSummary[] {
  return traces
    .map((trace) => ({
      signature: trace.signature,
      count: trace.count,
      averageAttention: trace.attention,
      averageTension: trace.tension,
      averageResonance: trace.resonance,
      averageStability: trace.stability
    }))
    .sort((a, b) => b.count - a.count);
}
