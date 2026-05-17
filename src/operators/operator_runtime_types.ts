export type OperatorId =
  | "VOID"
  | "POINT"
  | "CENTER"
  | "AXIS"
  | "FIELD"
  | "FLOW"
  | "VECTOR"
  | "LOOP"
  | "PEAK"
  | "ROOT"
  | "SPLIT"
  | "CROSS"
  | "BALANCE"
  | "TENSION"
  | "CONFIRM"
  | "FACT";

export interface OperatorRuntimeState {
  active: OperatorId[];
  fact: boolean;
  tension: number;
  attention: number;
  resonance: number;
  stability: number;
  vector: "none" | "forward" | "backward" | "up" | "down";
}

export interface CompiledSymbol {
  source: string;
  operators: OperatorId[];
  state: OperatorRuntimeState;
  warnings: string[];
}
