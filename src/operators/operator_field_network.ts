import type { OperatorNode } from "./operator_node";
import type { OperatorLink } from "./operator_link";

export interface OperatorFieldNetwork {
  nodes: OperatorNode[];
  links: OperatorLink[];
  density: number;
}

export function createFieldNetwork(
  nodes: OperatorNode[],
  links: OperatorLink[]
): OperatorFieldNetwork {
  const possible = nodes.length * Math.max(nodes.length - 1, 1);

  return {
    nodes,
    links,
    density:
      possible === 0
        ? 0
        : links.length / possible
  };
}
