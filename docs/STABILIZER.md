# Cimeika Stabilitron

Deterministic AI draft stabilizer enforcing ci_axis.yaml as Single Source of Truth.

## Architecture

```
User Intent + Draft → Policy Gate → Axis Manager → Engine → Final + Report
```

## Profiles

- **default**: Balanced (2000 chars, 5 paragraphs)
- **strict**: Minimal (1000 chars, 3 paragraphs)
- **code**: Extended (4000 chars, 10 paragraphs)
- **docs**: Documentation-focused (3000 chars, 8 paragraphs)
- **chat**: Conversational (1500 chars, 4 paragraphs)

## Modes

- **normal**: Standard limits
- **smart**: Relaxed limits
- **critical**: Strict limits, returns single clarifying question if intent missing

## Determinism

Same input ALWAYS produces same output. No randomness. Stability hash included in report.

## Security

- Admin-only endpoints (stabilize, axis/activate)
- Policy integration via existing control framework
- No full-text logging (only hashes + metrics)
