# Operator Memory v0.8

Purpose:
Add persistent memory traces and pattern indexing.

Added:
- trace index
- trace serialization
- trace deserialization
- pattern summaries
- symbolic input recording

Runtime expansion:
symbol
→ operator
→ state
→ trace
→ index
→ repeated pattern
→ memory topology

Core idea:
A symbolic event becomes memory only when it leaves a trace.

Repeated traces increase pattern weight.

This prepares the system for:
- long-term operator memory
- recurring pattern detection
- semantic history
- adaptive runtime behavior
