import type { OperatorId } from "./operator_runtime_types";

export interface TopologyNode {
  id: OperatorId;

  weight: number;
  tension: number;
  resonance: number;
  attention: number;
  stability: number;
  frequency: number;

  active: boolean;

  connections: OperatorId[];
}

export interface FieldState {
  nodes: TopologyNode[];

  globalTension: number;
  globalResonance: number;
  globalAttention: number;
  globalStability: number;
}

export function createNode(id: OperatorId): TopologyNode {
  return {
    id,

    weight: 0,
    tension: 0,
    resonance: 0,
    attention: 0,
    stability: 0,
    frequency: 0,

    active: false,

    connections: []
  };
}

export function activateNode(
  node: TopologyNode,
  weight = 1
): TopologyNode {
  node.active = true;

  node.weight += weight;
  node.attention += weight * 0.5;
  node.frequency += 1;

  return node;
}

export function propagateResonance(
  source: TopologyNode,
  targets: TopologyNode[]
): void {
  for (const target of targets) {
    target.resonance += source.resonance * 0.25;
    target.attention += source.attention * 0.1;
  }
}

export function applyTension(
  node: TopologyNode,
  value: number
): void {
  node.tension += value;

  if (node.tension > node.stability) {
    node.resonance += value * 0.5;
  }
}

export function stabilizeNode(
  node: TopologyNode,
  value: number
): void {
  node.stability += value;

  if (node.tension > 0) {
    node.tension = Math.max(
      0,
      node.tension - value
    );
  }
}

export function computeFieldState(
  nodes: TopologyNode[]
): FieldState {
  const state: FieldState = {
    nodes,

    globalTension: 0,
    globalResonance: 0,
    globalAttention: 0,
    globalStability: 0
  };

  for (const node of nodes) {
    state.globalTension += node.tension;
    state.globalResonance += node.resonance;
    state.globalAttention += node.attention;
    state.globalStability += node.stability;
  }

  return state;
}
