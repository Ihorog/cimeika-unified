export interface OperatorCoordinate {
  x: number;
  y: number;
  z: number;
}

export function resolveCoordinates(input: string): OperatorCoordinate {
  let x = 0;
  let y = 0;
  let z = 0;

  if (input.includes("→")) x += 1;
  if (input.includes("←")) x -= 1;

  if (input.includes("↑")) y += 1;
  if (input.includes("↓")) y -= 1;

  if (input.includes("∧")) z += 1;
  if (input.includes("∨")) z -= 1;

  return { x, y, z };
}
