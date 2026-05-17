import type { OperatorId } from "./operator_runtime_types";

export interface OperatorGraphEdge {
  from: OperatorId;
  to: OperatorId;
  relation:
    | "emerges"
    | "centers"
    | "structures"
    | "flows"
    | "branches"
    | "conflicts"
    | "balances"
    | "confirms"
    | "fixes";
  weight: number;
}

export const operatorGraph: OperatorGraphEdge[] = [
  { from: "VOID", to: "POINT", relation: "emerges", weight: 1 },
  { from: "POINT", to: "CENTER", relation: "centers", weight: 2 },
  { from: "CENTER", to: "AXIS", relation: "structures", weight: 2 },
  { from: "AXIS", to: "FLOW", relation: "flows", weight: 1 },
  { from: "FLOW", to: "SPLIT", relation: "branches", weight: 2 },
  { from: "SPLIT", to: "CROSS", relation: "conflicts", weight: 2 },
  { from: "CROSS", to: "BALANCE", relation: "balances", weight: 3 },
  { from: "BALANCE", to: "CONFIRM", relation: "confirms", weight: 2 },
  { from: "CONFIRM", to: "FACT", relation: "fixes", weight: 3 }
];
