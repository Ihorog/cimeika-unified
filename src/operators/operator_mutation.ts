export interface MutationResult {
  original: string;
  mutated: string;
  mutationLevel: number;
}

export function mutateOperator(input: string): MutationResult {
  let mutated = input;

  if (input.includes("+")) {
    mutated = input.replace("+", "=");
  } else if (input.includes("-")) {
    mutated = input.replace("-", "~");
  } else if (input.includes("○")) {
    mutated = input + "↺";
  }

  return {
    original: input,
    mutated,
    mutationLevel:
      originalDistance(input, mutated)
  };
}

function originalDistance(a: string, b: string): number {
  return Math.abs(a.length - b.length) +
    [...a].filter((x, i) => b[i] !== x).length;
}
