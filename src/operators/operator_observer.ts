import { runOperatorLoop } from "./operator_runtime_loop";
import { createSnapshot } from "./operator_state_snapshot";
import { calculateMetrics } from "./operator_metrics";
import { inspectRuntime } from "./operator_inspector";

export interface ObservationResult {
  snapshot: unknown;
  metrics: unknown;
  inspection: unknown;
}

export function observeOperator(
  input: string
): ObservationResult {
  const runtime = runOperatorLoop(input);

  const snapshot = createSnapshot(
    runtime.prediction,
    runtime.entropy,
    runtime.stable ? 1 : 0
  );

  const metrics = calculateMetrics(
    runtime.entropy,
    runtime.stable ? 1 : 0.5,
    runtime.stable ? 0 : 1,
    runtime.stable ? 1 : 0
  );

  const inspection = inspectRuntime(runtime);

  return {
    snapshot,
    metrics,
    inspection
  };
}
