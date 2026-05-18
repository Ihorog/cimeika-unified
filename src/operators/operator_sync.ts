import type { OperatorTimeState } from "./operator_time";

export interface SyncState {
  synced: boolean;
  delta: number;
  quality: "none" | "weak" | "medium" | "strong";
}

export function syncStates(
  a: OperatorTimeState,
  b: OperatorTimeState
): SyncState {
  const delta = Math.abs(a.timestamp - b.timestamp);

  let quality: SyncState["quality"] = "none";

  if (delta < 10000) quality = "strong";
  else if (delta < 60000) quality = "medium";
  else if (delta < 300000) quality = "weak";

  return {
    synced: quality !== "none",
    delta,
    quality
  };
}
