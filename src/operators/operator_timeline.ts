import type { StateSnapshot } from "./operator_state_snapshot";

export interface TimelineState {
  snapshots: StateSnapshot[];
}

export function createTimeline(): TimelineState {
  return {
    snapshots: []
  };
}

export function appendSnapshot(
  timeline: TimelineState,
  snapshot: StateSnapshot
): TimelineState {
  timeline.snapshots.push(snapshot);
  return timeline;
}
