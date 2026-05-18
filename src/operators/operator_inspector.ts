import type { RuntimeLoopResult } from "./operator_runtime_loop";

export interface InspectionResult {
  stable: boolean;
  entropyLevel: string;
  evolutionState: string;
}

export function inspectRuntime(
  runtime: RuntimeLoopResult
): InspectionResult {
  let entropyLevel = "LOW";

  if (runtime.entropy > 0.3) {
    entropyLevel = "MEDIUM";
  }

  if (runtime.entropy > 0.6) {
    entropyLevel = "HIGH";
  }

  return {
    stable: runtime.stable,
    entropyLevel,
    evolutionState: runtime.evolved
  };
}
