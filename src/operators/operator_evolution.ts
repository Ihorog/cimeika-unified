import { mutateOperator } from "./operator_mutation";

export interface EvolutionState {
  stage: number;
  current: string;
  previous: string;
}

export function evolveOperator(
  input: string,
  stage: number
): EvolutionState {
  const mutation = mutateOperator(input);

  return {
    stage,
    previous: input,
    current: mutation.mutated
  };
}
