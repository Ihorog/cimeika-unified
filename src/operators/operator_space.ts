import { buildVisualNode } from "./operator_visual_graph";

export interface SpatialField {
  active: boolean;
  nodeCount: number;
  fieldType: string;
}

export function createSpatialField(
  inputs: string[]
): SpatialField {
  const nodes = inputs.map(buildVisualNode);

  const active = nodes.length > 0;

  return {
    active,
    nodeCount: nodes.length,
    fieldType: active
      ? "RESONANCE_FIELD"
      : "VOID_FIELD"
  };
}
