import { resolveCoordinates } from "./operator_coordinates";
import { calculateVectorField } from "./operator_vector_field";
import { detectResonance } from "./operator_resonance";

export interface VisualOperatorNode {
  symbol: string;
  coordinates: {
    x: number;
    y: number;
    z: number;
  };
  vector: string;
  resonance: number;
}

export function buildVisualNode(
  input: string
): VisualOperatorNode {
  const coordinates = resolveCoordinates(input);
  const vector = calculateVectorField(input);
  const resonance = detectResonance(input);

  return {
    symbol: input,
    coordinates,
    vector: vector.direction,
    resonance: resonance.resonance
  };
}
