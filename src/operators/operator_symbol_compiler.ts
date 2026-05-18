import type {
  CompiledSymbol,
  OperatorId,
  OperatorRuntimeState
} from "./operator_runtime_types";

const SYMBOL_TO_OPERATOR: Record<string, OperatorId> = {
  "0": "VOID",
  "•": "POINT",
  "○": "CENTER",
  "|": "AXIS",
  "—": "FIELD",
  "~": "FLOW",
  "→": "VECTOR",
  "↺": "LOOP",
  "∧": "PEAK",
  "∨": "ROOT",
  "Y": "SPLIT",
  "×": "CROSS",
  "=": "BALANCE",
  "-": "TENSION",
  "+": "CONFIRM",
  "1": "FACT"
};

const DEFAULT_STATE: OperatorRuntimeState = {
  active: [],
  fact: false,
  tension: 0,
  attention: 0,
  resonance: 0,
  stability: 0,
  vector: "none"
};

export function compileSymbol(input: string): CompiledSymbol {
  const state: OperatorRuntimeState = {
    ...DEFAULT_STATE,
    active: []
  };

  const warnings: string[] = [];
  const operators: OperatorId[] = [];

  for (const char of Array.from(input)) {
    const op = SYMBOL_TO_OPERATOR[char];

    if (!op) {
      if (char.trim()) {
        warnings.push(`Unknown symbol: ${char}`);
      }
      continue;
    }

    operators.push(op);
    state.active.push(op);

    switch (op) {
      case "FACT":
        state.fact = true;
        state.stability += 2;
        break;

      case "CONFIRM":
        state.stability += 1;
        state.resonance += 1;
        break;

      case "TENSION":
        state.tension += 2;
        state.attention += 1;
        break;

      case "CENTER":
        state.attention += 2;
        state.stability += 1;
        break;

      case "VECTOR":
        state.vector = "forward";
        state.resonance += 1;
        break;

      case "PEAK":
        state.tension += 1;
        state.resonance += 2;
        break;

      case "ROOT":
        state.stability += 1;
        break;

      case "FLOW":
        state.resonance += 1;
        break;

      case "LOOP":
        state.resonance += 1;
        state.attention += 1;
        break;

      case "CROSS":
        state.tension += 2;
        break;

      case "BALANCE":
        state.tension = Math.max(0, state.tension - 1);
        state.stability += 2;
        break;

      case "VOID":
        state.fact = false;
        break;
    }
  }

  return {
    source: input,
    operators,
    state,
    warnings
  };
}
