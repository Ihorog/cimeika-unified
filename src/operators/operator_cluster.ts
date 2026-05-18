import type { OperatorNode } from "./operator_node";

export interface OperatorCluster {
  id: string;
  nodes: OperatorNode[];
  centerWeight: number;
}

export function createCluster(
  id: string,
  nodes: OperatorNode[]
): OperatorCluster {
  const total = nodes.reduce((sum, n) => sum + n.weight, 0);

  return {
    id,
    nodes,
    centerWeight: total / Math.max(nodes.length, 1)
  };
}
