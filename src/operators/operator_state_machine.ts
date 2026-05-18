export type RuntimeState =
  | "VOID"
  | "POINT"
  | "CENTER"
  | "AXIS"
  | "FLOW"
  | "SPLIT"
  | "CROSS"
  | "BALANCE"
  | "CONFIRM"
  | "FACT";

export interface StateTransition {
  from: RuntimeState;
  to: RuntimeState;
  trigger: string;
}

export const runtimeTransitions: StateTransition[] = [
  { from: "VOID", to: "POINT", trigger: "•" },
  { from: "POINT", to: "CENTER", trigger: "○" },
  { from: "CENTER", to: "AXIS", trigger: "|" },
  { from: "AXIS", to: "FLOW", trigger: "~" },
  { from: "FLOW", to: "SPLIT", trigger: "Y" },
  { from: "SPLIT", to: "CROSS", trigger: "×" },
  { from: "CROSS", to: "BALANCE", trigger: "=" },
  { from: "BALANCE", to: "CONFIRM", trigger: "+" },
  { from: "CONFIRM", to: "FACT", trigger: "1" }
];
