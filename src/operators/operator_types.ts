export type OperatorStatus = "FACT" | "MODEL" | "SIMULATION";

export interface OperatorNode {
  id: string;
  symbol: string;
  function: string;
  geometry: string;
  natural_forms: string[];
  role: string;
}

export interface OperatorRegistry {
  version: string;
  name: string;
  status: OperatorStatus;
  operators: OperatorNode[];
}

export interface OperatorTransition {
  from: string;
  to: string;
  relation: "emerges" | "stabilizes" | "branches" | "conflicts" | "balances" | "confirms";
}
