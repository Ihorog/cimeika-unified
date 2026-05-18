import type { OperatorCluster } from "./operator_cluster";

export interface EmergenceState {
  emerged: boolean;
  complexity: number;
}

export function detectEmergence(
  clusters: OperatorCluster[]
): EmergenceState {
  const complexity = clusters.reduce(
    (sum, c) => sum + c.nodes.length,
    0
  );

  return {
    emerged: complexity >= 5,
    complexity
  };
}
