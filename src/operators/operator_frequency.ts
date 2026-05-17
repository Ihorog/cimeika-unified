import type { TopologyNode } from "./operator_topology";

export interface FrequencyPattern {
  node: string;

  repetitions: number;

  frequencyScore: number;

  classification:
    | "rare"
    | "emerging"
    | "stable"
    | "dominant";
}

export function analyzeFrequency(
  node: TopologyNode
): FrequencyPattern {
  const repetitions = node.frequency;

  let classification:
    | "rare"
    | "emerging"
    | "stable"
    | "dominant" = "rare";

  if (repetitions >= 3) {
    classification = "emerging";
  }

  if (repetitions >= 7) {
    classification = "stable";
  }

  if (repetitions >= 12) {
    classification = "dominant";
  }

  return {
    node: node.id,

    repetitions,

    frequencyScore:
      repetitions *
      (1 + node.resonance * 0.1),

    classification
  };
}
