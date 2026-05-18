import type { OperatorNode } from "./operator_node";

export interface GravityResult {
  center: string | null;
  gravity: number;
}

export function detectGravityCenter(
  nodes: OperatorNode[]
): GravityResult {
  if (nodes.length === 0) {
    return {
      center: null,
      gravity: 0
    };
  }

  const sorted = [...nodes].sort(
    (a, b) => b.weight - a.weight
  );

  return {
    center: sorted[0].id,
    gravity: sorted[0].weight
  };
}
