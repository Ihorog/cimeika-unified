# SEO Matrix Implementation - Stage 2/4

## Overview

This PR implements **Stage 2/4: SEO META CANON + HREFLANG BINDINGS** for the Cimeika Unified project. It provides a complete SEO metadata management system for different emotional states and user intents.

## What's Included

### 1. Configuration (YAML)
- **File:** `backend/app/config/cimeika_seo_matrix.yaml`
- 7 emotional states × 7 intents = 49 meta entries
- Canonical language configuration
- Hreflang URL patterns for EN/UK
- Validation rules (title max: 60, description max: 155)

### 2. Backend Implementation
- **Service:** `backend/app/utils/seo_matrix.py`
  - SEOMatrix class for loading/parsing YAML
  - URL generation utilities
  - Meta validation functions
  - Singleton pattern for global access

- **API Endpoints:** Added to `backend/main.py`
  - `GET /api/v1/seo/config` - Get SEO configuration
  - `GET /api/v1/seo/states` - Get all emotional states
  - `GET /api/v1/seo/intents/<state>` - Get intents for a state
  - `GET /api/v1/seo/meta/<state>/<intent>` - Get complete SEO data

- **Tests:** `backend/tests/test_seo_matrix.py`
  - 15 comprehensive tests
  - All tests passing ✅
  - Coverage: loading, validation, URL generation, API

### 3. Frontend Implementation
- **Service:** `frontend/src/services/seo.ts`
  - TypeScript service for consuming SEO API
  - Document meta tag management
  - Open Graph and Twitter Card support
  - Automatic cleanup

- **React Hook:** `frontend/src/hooks/useSeo.ts`
  - Easy component integration
  - Automatic meta tag application
  - Lifecycle management

- **Demo Page:** `frontend/src/pages/SeoDemo.tsx`
  - Interactive demonstration
  - Available at `/seo-demo`
  - Browse states/intents
  - Preview and apply metadata

### 4. Documentation
- **Guide:** `docs/SEO_MATRIX.md`
  - Complete usage documentation
  - API reference
  - Code examples
  - Best practices
  - Troubleshooting

## States & Intents

### Emotional States (7)
1. `fatigue` - Physical/mental exhaustion
2. `tension` - Stress and pressure
3. `anxiety` - Worry and unease
4. `joy` - Happiness and contentment
5. `loss` - Grief and bereavement
6. `anticipation` - Expectation and hope
7. `change` - Transition and transformation

### User Intents (7)
1. `understand` - Learn about the state
2. `capture` - Record/document the state
3. `calm` - Find relief/peace
4. `check` - Assess current condition
5. `preserve` - Maintain positive state
6. `connect` - Share with others
7. `prepare` - Plan for future occurrence

## Technical Details

### SEO Tags Applied

When SEO metadata is applied to a page:

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
   <meta property="og:description" content="...">
   <meta property="og:url" content="...">
   ```

6. **Twitter Card Tags**
   ```html
   <meta name="twitter:card" content="summary">
   <meta name="twitter:title" content="...">
   ```

## Usage Examples

### Backend (Python)
```python
from app.utils.seo_matrix import get_seo_matrix

seo = get_seo_matrix()
data = seo.get_full_seo_data('fatigue', 'understand')
print(data['meta']['title'])  # "Understand your fatigue"
```

### Frontend (TypeScript/React)
```tsx
import { useSeo } from './hooks';

function MyComponent() {
  const { seoData, loading } = useSeo({
    state: 'fatigue',
    intent: 'understand'
  });
  
  if (loading) return <div>Loading...</div>;
  return <h1>{seoData?.meta.title}</h1>;
}
```

### API (cURL)
```bash
curl http://localhost:5000/api/v1/seo/meta/fatigue/understand
```

## Testing

### Run Backend Tests
```bash
cd backend
pytest tests/test_seo_matrix.py -v
```

**Result:** ✅ 15/15 tests passing

### Manual Testing
1. Start backend: `cd backend && python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Visit: `http://localhost:3000/seo-demo`

## Files Changed

```
14 files changed, 1837 insertions(+)

Backend:
  backend/app/config/cimeika_seo_matrix.yaml    (new)
  backend/app/utils/seo_matrix.py              (new)
  backend/main.py                              (modified)
  backend/requirements.txt                     (modified)
  backend/tests/test_seo_matrix.py             (new)
  backend/tests/__init__.py                    (new)

Frontend:
  frontend/src/services/seo.ts                 (new)
  frontend/src/services/index.ts               (modified)
  frontend/src/hooks/useSeo.ts                 (new)
  frontend/src/hooks/index.ts                  (new)
  frontend/src/pages/SeoDemo.tsx               (new)
  frontend/src/pages/SeoDemo.css               (new)
  frontend/src/App.jsx                         (modified)

Docs:
  docs/SEO_MATRIX.md                           (new)
```

## Validation

All meta entries have been validated:
- ✅ Titles: All under 60 characters
- ✅ Descriptions: All under 155 characters
- ✅ URL patterns: Properly formatted
- ✅ API endpoints: All functional
- ✅ Frontend build: Successful
- ✅ Tests: 15/15 passing

## Next Steps (Stage 3/4)

The implementation is complete and ready for:
1. Integration with actual page routes
2. Language-specific content (beyond URL patterns)
3. Dynamic metadata based on user context
4. Analytics integration
5. Sitemap generation

## Dependencies Added

- **Backend:** `PyYAML==6.0.1` (for YAML parsing)
- **Frontend:** None (uses existing dependencies)

## Demo

To see the SEO matrix in action:
1. Start the backend server
2. Start the frontend development server
3. Navigate to `http://localhost:3000/seo-demo`
4. Select different states and intents
5. Click "Apply SEO Meta" to see changes in browser DevTools

## Architecture Compliance

✅ Follows Cimeika fixed architecture:
- Backend utilities in `app/utils/`
- Configuration in `app/config/`
- API endpoints in `main.py`
- Frontend services in `src/services/`
- Shared hooks in `src/hooks/`
- No structural changes to core architecture

## Notes

- All SEO metadata is currently in English (Stage 2 focus)
- Future stages will add Ukrainian and other language content
- The system is designed to be easily extensible
- Validation ensures all entries meet SEO best practices

---

**Stage:** 2/4 - SEO META CANON + HREFLANG BINDINGS ✅  
**Status:** Complete and tested  
**Ready for:** Review and merge
