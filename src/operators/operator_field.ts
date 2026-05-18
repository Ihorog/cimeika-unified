export interface OperatorField {
  center: boolean;
  balance: number;
  expansion: number;
  tension: number;
}

export function calculateField(input: string): OperatorField {
  return {
    center: input.includes("○"),
    balance: input.includes("=") ? 1 : 0,
    expansion: input.includes("→") ? 1 : 0,
    tension: input.includes("-") ? 1 : 0
  };
}
