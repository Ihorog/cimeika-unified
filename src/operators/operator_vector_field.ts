export interface OperatorVector {
  direction: string;
  magnitude: number;
}

export function calculateVectorField(input: string): OperatorVector {
  if (input.includes("→")) {
    return {
      direction: "FORWARD",
      magnitude: 1
    };
  }

  if (input.includes("←")) {
    return {
      direction: "BACKWARD",
      magnitude: 1
    };
  }

  if (input.includes("↑")) {
    return {
      direction: "ASCEND",
      magnitude: 1
    };
  }

  if (input.includes("↓")) {
    return {
      direction: "DESCEND",
      magnitude: 1
    };
  }

  return {
    direction: "STATIC",
    magnitude: 0
  };
}
