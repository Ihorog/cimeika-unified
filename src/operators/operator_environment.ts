import type { TopologyNode } from "./operator_topology";

export interface EnvironmentInfluence {
  pressure: number;
  noise: number;
  support: number;
  instability: number;
}

export function applyEnvironment(
  node: TopologyNode,
  env: EnvironmentInfluence
): void {
  node.tension +=
    env.pressure * 0.5;

  node.tension +=
    env.instability * 0.25;

  node.resonance +=
    env.support * 0.4;

  node.attention +=
    env.noise * 0.1;
}
