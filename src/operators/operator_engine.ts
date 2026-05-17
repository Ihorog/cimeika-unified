import type { OperatorNode, OperatorRegistry, OperatorTransition } from "./operator_types";

export class OperatorEngine {
  private byId = new Map<string, OperatorNode>();
  private bySymbol = new Map<string, OperatorNode>();

  constructor(private registry: OperatorRegistry) {
    for (const op of registry.operators) {
      this.byId.set(op.id, op);
      this.bySymbol.set(op.symbol, op);
    }
  }

  getById(id: string): OperatorNode | null {
    return this.byId.get(id) ?? null;
  }

  getBySymbol(symbol: string): OperatorNode | null {
    return this.bySymbol.get(symbol) ?? null;
  }

  parseSequence(input: string): OperatorNode[] {
    return [...input]
      .map((symbol) => this.getBySymbol(symbol))
      .filter((op): op is OperatorNode => Boolean(op));
  }

  validate(): string[] {
    const errors: string[] = [];
    const ids = new Set<string>();
    const symbols = new Set<string>();

    for (const op of this.registry.operators) {
      if (ids.has(op.id)) errors.push(`Duplicate id: ${op.id}`);
      if (symbols.has(op.symbol)) errors.push(`Duplicate symbol: ${op.symbol}`);

      ids.add(op.id);
      symbols.add(op.symbol);

      if (!op.function) errors.push(`Missing function: ${op.id}`);
      if (!op.geometry) errors.push(`Missing geometry: ${op.id}`);
      if (!op.role) errors.push(`Missing role: ${op.id}`);
    }

    return errors;
  }
}

export const baseTransitions: OperatorTransition[] = [
  { from: "VOID", to: "POINT", relation: "emerges" },
  { from: "POINT", to: "CENTER", relation: "stabilizes" },
  { from: "CENTER", to: "AXIS", relation: "stabilizes" },
  { from: "AXIS", to: "FLOW", relation: "emerges" },
  { from: "FLOW", to: "SPLIT", relation: "branches" },
  { from: "SPLIT", to: "CROSS", relation: "conflicts" },
  { from: "CROSS", to: "BALANCE", relation: "balances" },
  { from: "BALANCE", to: "CONFIRM", relation: "confirms" },
  { from: "CONFIRM", to: "FACT", relation: "stabilizes" }
];
