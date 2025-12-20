# SEO Matrix Documentation

## Overview

The SEO Matrix is a comprehensive system for managing SEO metadata across different emotional states and user intents in the Cimeika application. It provides canonical URLs, hreflang tags, and optimized meta titles and descriptions for improved search engine visibility and international support.

## Architecture

### Components

1. **YAML Configuration** (`backend/app/config/cimeika_seo_matrix.yaml`)
   - Central configuration file containing all SEO metadata
   - Defines hreflang patterns, validation rules, and meta entries

2. **Python Service** (`backend/app/utils/seo_matrix.py`)
   - `SEOMatrix` class for loading and accessing YAML data
   - Validation utilities
   - URL generation helpers

3. **REST API Endpoints** (`backend/main.py`)
   - `/api/v1/seo/config` - Get SEO configuration
   - `/api/v1/seo/states` - Get all emotional states
   - `/api/v1/seo/intents/<state>` - Get intents for a state
   - `/api/v1/seo/meta/<state>/<intent>` - Get complete SEO data

4. **Frontend Service** (`frontend/src/services/seo.ts`)
   - TypeScript service for consuming SEO API
   - Document meta tag management
   - Open Graph and Twitter Card support

5. **React Hook** (`frontend/src/hooks/useSeo.ts`)
   - `useSeo` hook for easy component integration
   - Automatic meta tag application and cleanup

6. **Demo Page** (`frontend/src/pages/SeoDemo.tsx`)
   - Interactive demonstration of SEO functionality
   - Available at `/seo-demo`

## Configuration Structure

### SEO Settings

```yaml
seo:
  canonical_lang: en              # Default canonical language
  hreflang:                       # URL patterns for each language
    en: "/en/{state}/{intent}"
    uk: "/uk/{state}/{intent}"
  rules:                          # Validation rules
    title_max: 60                 # Maximum title length (chars)
    description_max: 155          # Maximum description length (chars)
```

### Meta Entries

The matrix defines meta entries for 7 emotional states, each with 7 intents:

**States:**
- `fatigue` - Physical/mental exhaustion
- `tension` - Stress and pressure
- `anxiety` - Worry and unease
- `joy` - Happiness and contentment
- `loss` - Grief and bereavement
- `anticipation` - Expectation and hope
- `change` - Transition and transformation

**Intents:**
- `understand` - Learn about the state
- `capture` - Record/document the state
- `calm` - Find relief/peace
- `check` - Assess current condition
- `preserve` - Maintain positive state
- `connect` - Share with others
- `prepare` - Plan for future occurrence

Example:
```yaml
meta_entries:
  fatigue:
    understand: 
      title: "Understand your fatigue"
      description: "Clarify fatigue. One step, clear result."
    capture:
      title: "Capture your fatigue"
      description: "Capture fatigue. One step, clear result."
    # ... more intents
```

## Backend Usage

### Python Service

```python
from app.utils.seo_matrix import get_seo_matrix

# Get the global SEO matrix instance
seo = get_seo_matrix()

# Get all states
states = seo.get_all_states()
# Returns: ['fatigue', 'tension', 'anxiety', 'joy', 'loss', 'anticipation', 'change']

# Get intents for a state
intents = seo.get_all_intents('fatigue')
# Returns: ['understand', 'capture', 'calm', 'check', 'preserve', 'connect', 'prepare']

# Get meta information
meta = seo.get_meta('fatigue', 'understand')
# Returns: {'title': 'Understand your fatigue', 'description': '...'}

# Get complete SEO data
data = seo.get_full_seo_data('fatigue', 'understand')
# Returns: {
#   'meta': {...},
#   'canonical_url': '/en/fatigue/understand',
#   'hreflang': {'en': '...', 'uk': '...'},
#   'validation': {...}
# }

# Generate URLs
canonical = seo.get_canonical_url('fatigue', 'understand')
hreflang_tags = seo.get_hreflang_tags('fatigue', 'understand')

# Validate metadata
validation = seo.validate_meta(
    title="Some title",
    description="Some description"
)
```

### API Endpoints

**Get Configuration:**
```bash
GET /api/v1/seo/config
```

Response:
```json
{
  "status": "success",
  "config": {
    "canonical_lang": "en",
    "hreflang_patterns": {...},
    "rules": {...}
  }
}
```

**Get States:**
```bash
GET /api/v1/seo/states
```

Response:
```json
{
  "status": "success",
  "states": ["fatigue", "tension", ...]
}
```

**Get Intents:**
```bash
GET /api/v1/seo/intents/{state}
```

Response:
```json
{
  "status": "success",
  "state": "fatigue",
  "intents": ["understand", "capture", ...]
}
```

**Get SEO Data:**
```bash
GET /api/v1/seo/meta/{state}/{intent}
```

Response:
```json
{
  "status": "success",
  "state": "fatigue",
  "intent": "understand",
  "data": {
    "meta": {
      "title": "Understand your fatigue",
      "description": "Clarify fatigue. One step, clear result."
    },
    "canonical_url": "/en/fatigue/understand",
    "hreflang": {
      "en": "/en/fatigue/understand",
      "uk": "/uk/fatigue/understand"
    },
    "validation": {
      "title": {
        "value": "Understand your fatigue",
        "length": 23,
        "max": 60,
        "valid": true
      },
      "description": {...}
    }
  }
}
```

## Frontend Usage

### Service Usage

```typescript
import { seoService } from './services';

// Get all states
const states = await seoService.getStates();

// Get intents for a state
const intents = await seoService.getIntents('fatigue');

// Get complete SEO data
const seoData = await seoService.getSeoData('fatigue', 'understand');

// Apply SEO metadata to document
seoService.updateDocumentMeta(seoData, 'fatigue', 'understand');

// Clear SEO metadata
seoService.clearDocumentMeta();

// Convenient method to apply SEO
await seoService.applySeoMeta('fatigue', 'understand');
```

### React Hook Usage

```tsx
import { useSeo } from './hooks';

function MyComponent() {
  const { seoData, loading, error, applySeo, clearSeo } = useSeo({
    state: 'fatigue',
    intent: 'understand',
    autoApply: true  // Automatically apply on mount (default)
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>{seoData?.meta.title}</h1>
      <p>{seoData?.meta.description}</p>
      
      <button onClick={applySeo}>Reapply SEO</button>
      <button onClick={clearSeo}>Clear SEO</button>
    </div>
  );
}
```

### What Gets Applied

When SEO metadata is applied to a page, the following elements are updated:

1. **Document Title**
   ```html
   <title>Understand your fatigue</title>
   ```

2. **Meta Description**
   ```html
   <meta name="description" content="Clarify fatigue. One step, clear result.">
   ```

3. **Canonical Link**
   ```html
   <link rel="canonical" href="https://example.com/en/fatigue/understand">
   ```

4. **Hreflang Tags**
   ```html
   <link rel="alternate" hreflang="en" href="https://example.com/en/fatigue/understand">
   <link rel="alternate" hreflang="uk" href="https://example.com/uk/fatigue/understand">
   ```

5. **Open Graph Tags**
   ```html
   <meta property="og:title" content="Understand your fatigue">
   <meta property="og:description" content="Clarify fatigue. One step, clear result.">
   <meta property="og:url" content="https://example.com/en/fatigue/understand">
   <meta property="og:type" content="website">
   ```

6. **Twitter Card Tags**
   ```html
   <meta name="twitter:card" content="summary">
   <meta name="twitter:title" content="Understand your fatigue">
   <meta name="twitter:description" content="Clarify fatigue. One step, clear result.">
   ```

## Demo Page

Visit `/seo-demo` to see an interactive demonstration of the SEO functionality.

Features:
- Browse all states and intents
- Preview meta tags and validation
- View canonical URLs and hreflang tags
- Apply and clear SEO metadata dynamically
- See the configuration and rules

## Validation

The system validates meta tags against configured rules:

- **Title:** Maximum 60 characters (optimal for search results)
- **Description:** Maximum 155 characters (optimal for search snippets)

Validation results are included in API responses and can be checked before applying metadata.

## Adding New Content

To add new states or intents:

1. Edit `backend/app/config/cimeika_seo_matrix.yaml`
2. Add new entries following the existing structure
3. Ensure titles and descriptions meet length requirements
4. Reload the SEO matrix (restart backend or use hot reload)

Example:
```yaml
meta_entries:
  new_state:
    new_intent:
      title: "Title for new state/intent"
      description: "Description for new state/intent. Clear and concise."
```

## Best Practices

1. **Keep titles concise** - Aim for 50-60 characters
2. **Make descriptions compelling** - Use 150-155 characters effectively
3. **Use keywords naturally** - Include relevant terms in titles/descriptions
4. **Maintain consistency** - Follow established patterns for similar content
5. **Test validation** - Ensure all entries pass validation rules
6. **Update systematically** - When adding states, add all intents
7. **Clean up on unmount** - Always clear SEO when component unmounts

## Troubleshooting

**Issue: SEO data not loading**
- Check backend is running and accessible
- Verify API endpoints return data
- Check browser console for errors

**Issue: Meta tags not updating**
- Ensure `autoApply` is true in `useSeo` hook
- Check that `seoData` is not null
- Verify `updateDocumentMeta` is called

**Issue: Validation fails**
- Check title/description lengths
- Review configured rules in `cimeika_seo_matrix.yaml`
- Use demo page to preview before applying

## Future Enhancements

Potential improvements:
- Multi-language meta content (not just URLs)
- Dynamic metadata based on user preferences
- A/B testing support for different meta variations
- Analytics integration to track SEO performance
- JSON-LD structured data support
- Sitemap generation based on SEO matrix

## Related Files

- Configuration: `backend/app/config/cimeika_seo_matrix.yaml`
- Python Service: `backend/app/utils/seo_matrix.py`
- API Endpoints: `backend/main.py`
- Frontend Service: `frontend/src/services/seo.ts`
- React Hook: `frontend/src/hooks/useSeo.ts`
- Demo Page: `frontend/src/pages/SeoDemo.tsx`
- Types: `frontend/src/services/seo.ts` (TypeScript interfaces)

---

**Version:** 1.0.0  
**Last Updated:** December 2024  
**Stage:** 2/4 - SEO META CANON + HREFLANG BINDINGS
