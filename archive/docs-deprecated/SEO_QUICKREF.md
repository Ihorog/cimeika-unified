# SEO Integration — Quick Reference

## Overview
The Cimeika SEO system provides a comprehensive 7×7 emotional-intent matrix with bilingual support (EN + UK), module mapping, and writes policy management.

## Quick Facts
- **States**: 7 (fatigue, tension, anxiety, joy, loss, anticipation, change)
- **Intents**: 7 (understand, capture, calm, check, preserve, connect, prepare)
- **Languages**: 2 (en, uk)
- **Total URLs**: 98 (49 per language)
- **Module Mapping**: Nastrij (4), Kazkar (1), PoDija (2)

## API Endpoints

### Get SEO Entry
```bash
GET /api/v1/ci/seo/v2/entry/{lang}/{state}/{intent}

# Example
curl http://localhost:5000/api/v1/ci/seo/v2/entry/en/fatigue/understand
```

**Response:**
```json
{
  "status": "success",
  "entry": {
    "title": "Understand your fatigue",
    "description": "Explore and understand the nature of your fatigue",
    "url": "/en/fatigue/understand",
    "module": "nastrij",
    "state": "fatigue",
    "intent": "understand",
    "lang": "en",
    "writes_policy": {
      "min": 2,
      "max": 3,
      "mandatory": ["calendar.time_point", "gallery.experience_snapshot"],
      "optional": "nastrij.state_mark"
    }
  }
}
```

### Get All Entries for Language
```bash
GET /api/v1/ci/seo/v2/entries/{lang}

# Example
curl http://localhost:5000/api/v1/ci/seo/v2/entries/uk
```

### Get Module Mapping
```bash
GET /api/v1/ci/seo/v2/module/{state}

# Example
curl http://localhost:5000/api/v1/ci/seo/v2/module/loss
```

**Response:**
```json
{
  "status": "success",
  "state": "loss",
  "module": "kazkar",
  "writes_policy": {
    "min": 2,
    "max": 3,
    "mandatory": ["calendar.time_point", "gallery.experience_snapshot"],
    "optional": "kazkar.memory_node"
  }
}
```

### Generate Sitemap
```bash
GET /api/v1/ci/seo/v2/sitemap?base_url={url}

# Example
curl http://localhost:5000/api/v1/ci/seo/v2/sitemap?base_url=https://cimeika.com
```

## Python Usage

### Import Service
```python
from app.config.seo import seo_service
```

### Get SEO Entry
```python
entry = seo_service.get_entry('en', 'fatigue', 'understand')
print(entry['title'])  # "Understand your fatigue"
print(entry['module'])  # "nastrij"
```

### Validate Routing
```python
is_valid = seo_service.validate_routing('en', 'fatigue', 'understand')  # True
is_valid = seo_service.validate_routing('de', 'fatigue', 'understand')  # False
```

### Get Module for State
```python
module = seo_service.get_module('loss')  # "kazkar"
module = seo_service.get_module('anticipation')  # "podija"
```

### Get Writes Policy
```python
policy = seo_service.get_writes_policy('nastrij')
# {
#   "min": 2,
#   "max": 3,
#   "mandatory": ["calendar.time_point", "gallery.experience_snapshot"],
#   "optional": "nastrij.state_mark"
# }
```

### Generate All Entries
```python
all_entries = seo_service.get_all_entries('en')  # 49 entries
all_entries = seo_service.get_all_entries('uk')  # 49 entries
```

### Generate Sitemap
```python
sitemap = seo_service.generate_sitemap_entries('https://cimeika.com')
# Returns 49 entries with hreflang alternates
```

## Module Mapping

| State | Module | Writes Optional |
|-------|--------|-----------------|
| fatigue | nastrij | nastrij.state_mark |
| tension | nastrij | nastrij.state_mark |
| anxiety | nastrij | nastrij.state_mark |
| joy | nastrij | nastrij.state_mark |
| loss | kazkar | kazkar.memory_node |
| anticipation | podija | podija.future_link |
| change | podija | podija.future_link |

## Writes Policy

### Base Policy (Always)
- **Min**: 2 writes
- **Max**: 3 writes
- **Mandatory**: 
  - `calendar.time_point` (when)
  - `gallery.experience_snapshot` (what)

### Optional (Module-specific)
- **Nastrij**: `nastrij.state_mark` (emotional state marker)
- **Kazkar**: `kazkar.memory_node` (memory link)
- **PoDija**: `podija.future_link` (future event link)

## URL Structure

### Format
```
/{lang}/{state}/{intent}
```

### Examples
- `/en/fatigue/understand`
- `/uk/втома/зрозуміти` (not implemented, uses English slugs)
- `/en/loss/calm`
- `/uk/anticipation/prepare`

### Hreflang Tags
Each URL has alternates:
```html
<link rel="alternate" hreflang="en" href="/en/fatigue/understand" />
<link rel="alternate" hreflang="uk" href="/uk/fatigue/understand" />
```

## File Locations

### Configuration
- `backend/app/config/seo/cimeikaseomatrix.yaml` - 7×7 matrix data
- `backend/app/config/seo/seoresearchseeds.yaml` - Semantic research seeds

### Implementation
- `backend/app/config/seo/seo_service.py` - Core service
- `backend/app/config/seo/__init__.py` - Package init
- `backend/app/modules/ci/service.py` - Ci integration
- `backend/app/modules/ci/api.py` - FastAPI endpoints
- `backend/main.py` - Flask v2 endpoints

### Testing
- `backend/test_seo_service.py` - Comprehensive test suite

### Documentation
- `docs/SEO_INTEGRATION.md` - Full integration guide
- `docs/SEO_QUICKREF.md` - This quick reference

## Testing

### Run Test Suite
```bash
cd backend
python test_seo_service.py
```

### Expected Output
```
✅ ALL TESTS PASSED
- Basic getters: ✓
- Routing validation: ✓
- URL building: ✓
- Module mapping: ✓
- Writes policy: ✓
- Entry retrieval: ✓
- All entries: ✓ (49 EN, 49 UK)
- Sitemap: ✓ (49 entries)
- Coverage: ✓ (100%)
```

## Frontend Integration Example

### React Component
```typescript
import { useEffect, useState } from 'react';

interface SEOEntry {
  title: string;
  description: string;
  url: string;
  module: string;
  writes_policy: any;
}

function StateIntentPage({ lang, state, intent }) {
  const [seoData, setSeoData] = useState<SEOEntry | null>(null);
  
  useEffect(() => {
    fetch(`/api/v1/ci/seo/v2/entry/${lang}/${state}/${intent}`)
      .then(res => res.json())
      .then(data => setSeoData(data.entry));
  }, [lang, state, intent]);
  
  if (!seoData) return <div>Loading...</div>;
  
  return (
    <>
      <Helmet>
        <title>{seoData.title}</title>
        <meta name="description" content={seoData.description} />
        <link rel="alternate" hreflang="en" href={`/en/${state}/${intent}`} />
        <link rel="alternate" hreflang="uk" href={`/uk/${state}/${intent}`} />
      </Helmet>
      
      <main>
        <h1>{seoData.title}</h1>
        <p>Module: {seoData.module}</p>
        {/* Render content based on module */}
      </main>
    </>
  );
}
```

## Common Patterns

### Pattern 1: Get Entry with Module
```python
entry = seo_service.get_entry('en', 'fatigue', 'understand')
module = entry['module']  # "nastrij"
policy = entry['writes_policy']  # Full policy with optional
```

### Pattern 2: Validate Before Processing
```python
if seo_service.validate_routing(lang, state, intent):
    entry = seo_service.get_entry(lang, state, intent)
    # Process entry
else:
    # Return 404
```

### Pattern 3: Generate Language Selector
```python
states = seo_service.get_states()
intents = seo_service.get_intents()
languages = seo_service.get_languages()

for lang in languages:
    for state in states:
        for intent in intents:
            url = seo_service.build_url(lang, state, intent)
            # Generate link
```

## Troubleshooting

### Entry Not Found
- Check that state is in canonical list
- Check that intent is in canonical list
- Check that language is 'en' or 'uk'
- Use `validate_routing()` first

### Missing Optional Writes Policy
- Only appears when module is specified
- Use `get_writes_policy(module)` not `get_writes_policy()`

### Wrong Module Mapping
- Check `MODULE_MAPPING` in `seo_service.py`
- Use `get_module(state)` to verify

## Support

For full documentation, see:
- `docs/SEO_INTEGRATION.md` - Complete implementation guide
- `backend/test_seo_service.py` - Working examples

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-20
