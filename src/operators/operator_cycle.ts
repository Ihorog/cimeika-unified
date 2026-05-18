export interface RuntimeCycle {
  iteration: number;
  active: boolean;
  phase: string;
}

export function createRuntimeCycle(
  iteration: number
): RuntimeCycle {
  return {
    iteration,
    active: true,
    phase:
      iteration % 2 === 0
        ? "EXPANSION"
        : "STABILIZATION"
  };
}
