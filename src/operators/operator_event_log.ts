export interface OperatorEvent {
  timestamp: number;
  type: string;
  payload: string;
}

export class OperatorEventLog {
  private events: OperatorEvent[] = [];

  add(type: string, payload: string): void {
    this.events.push({
      timestamp: Date.now(),
      type,
      payload
    });
  }

  list(): OperatorEvent[] {
    return this.events;
  }
}
