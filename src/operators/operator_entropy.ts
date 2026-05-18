export interface EntropyState {
  entropy: number;
  order: number;
}

export function calculateEntropy(
  symbols: string[]
): EntropyState {
  const unique = new Set(symbols);

  const entropy =
    unique.size / Math.max(symbols.length, 1);

  return {
    entropy,
    order: 1 - entropy
  };
}
