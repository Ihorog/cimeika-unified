# API Reference

## Stabilizer API

### POST /stabilizer/stabilize
Enforce ci_axis.yaml rules over AI draft text.

**Auth:** Admin key required (`X-CI-Key` header)

**Request:**
```json
{
  "intent": "User context/goal",
  "draft": "AI-generated text to stabilize",
  "mode": "normal|smart|critical"
}
```

**Response:**
```json
{
  "final": "Stabilized text",
  "report": {
    "cut_flags": ["char_limit", "variants_removed"],
    "trimmed_chars": 1000,
    "removed_new_topics": 2,
    "policy_allowed": true,
    "trace_id": "a1b2c3d4",
    "deterministic_score": 0.742
  }
}
```

### POST /stabilizer/axis/activate
Switch active axis profile (default, strict, code, docs, chat).

**Auth:** Admin key required

**Request:**
```json
{
  "profile": "code"
}
```

### GET /stabilizer/axis/active
Retrieve current axis configuration (no auth required).

## CLI Usage

```bash
# Stabilize a draft file
cit stabilize --draft input.txt --intent "Fix bug in auth" --mode normal --output final.txt

# Use with environment variables
export CI_ADMIN_KEY=your-key
export CI_API_URL=https://your-api.vercel.app
cit stabilize --draft draft.md --mode critical
```

### Vercel Environment Variables

Set the following in Vercel project settings:
- `CI_ADMIN_KEY`: Admin authentication key for stabilizer API
