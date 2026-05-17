import type { OperatorId } from "./operator_runtime_types";

export interface RecognizedPattern {
  name: string;
  description: string;
  operators: OperatorId[];
}

export function recognizePattern(
  operators: OperatorId[]
): RecognizedPattern {
  const key = operators.join(">");

  if (key === "CENTER>CONFIRM>PEAK>VECTOR") {
    return {
      name: "centered_forward_manifestation",
      description: "center confirmed, active force directed forward",
      operators
    };
  }

  if (operators.includes("TENSION") && operators.includes("BALANCE")) {
    return {
      name: "tension_balancing",
      description: "open contour moving toward stabilization",
      operators
    };
  }

  if (operators.includes("LOOP") && operators.includes("CONFIRM")) {
    return {
      name: "closed_cycle",
      description: "cycle confirmed as stable contour",
      operators
    };
  }

  if (operators.includes("SPLIT") && operators.includes("VECTOR")) {
    return {
      name: "branching_direction",
      description: "development branch receives direction",
      operators
    };
  }

  return {
    name: "unclassified_pattern",
    description: "operator sequence has no named pattern yet",
    operators
  };
}
