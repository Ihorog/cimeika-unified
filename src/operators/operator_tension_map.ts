export interface TensionMap {
  local: number;
  global: number;
  gradient: number;
  state: "low" | "medium" | "high" | "critical";
}

export function mapTension(local: number, global: number): TensionMap {
  const gradient = global - local;
  const total = local + global;

  let state: TensionMap["state"] = "low";

  if (total >= 2) state = "medium";
  if (total >= 5) state = "high";
  if (total >= 8) state = "critical";

  return {
    local,
    global,
    gradient,
    state
  };
}
