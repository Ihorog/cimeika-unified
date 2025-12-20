# CIMEIKA — SEO & SYSTEM INTEGRATION

**Version 1.0.0**  
**Recommendational Document**  
**EN + UK**

---

## 1. Purpose / Навіщо

### EN
This document unifies Cimeika's SEO matrix, semantic research, seeds, system mapping, and development guidelines into a single reference.  
It is recommendational, not prescriptive: developers may choose the best implementation approach.

### UK
Цей документ об'єднує SEO‑матрицю Cimeika, семантичне дослідження, seeds, системне мапування та рекомендації для розробки в один файл.  
Документ рекомендаційний, а не директивний: розробник сам обирає спосіб реалізації.

---

## 2. Canonical Emotional–Intent Matrix (7×7)

### States / Стани
- **fatigue** / втома  
- **tension** / напруга  
- **anxiety** / тривога  
- **joy** / радість  
- **loss** / втрата  
- **anticipation** / очікування  
- **change** / зміна  

### Intents / Намір
- **understand** / зрозуміти  
- **capture** / зафіксувати  
- **calm** / заспокоїти  
- **check** / перевірити  
- **preserve** / зберегти  
- **connect** / пов'язати  
- **prepare** / підготуватися  

### Implementation
The complete 7×7 matrix with canonical titles (EN) and recommended equivalents (UK) is stored in:
```
backend/app/config/seo/cimeikaseomatrix.yaml
```

Each entry contains:
- `state`: Emotional state
- `intent`: User intent
- `en`: English title and description
- `uk`: Ukrainian title and description

---

## 3. Semantic Research Seeds

### Coverage
The seeds file contains approximately **196 semantic phrases** covering:
- Intent-generic patterns (cross-state)
- State-specific patterns
- Combined patterns
- Both EN and UK languages

### Location
```
backend/app/config/seo/seoresearchseeds.yaml
```

### Structure
- `intent_generic`: Patterns that work across all states (e.g., "why am I", "how to calm")
- `state_specific`: Patterns specific to each emotional state
- `combined_patterns`: Example combinations of state + intent

---

## 4. URL Structure

### Format
```
/{lang}/{state}/{intent}
```

### Examples
- `/en/fatigue/understand`  
- `/uk/anticipation/prepare`  
- `/en/loss/calm`

### Hreflang
Each URL should have alternate language versions:
```html
<link rel="alternate" hreflang="en" href="/en/fatigue/understand" />
<link rel="alternate" hreflang="uk" href="/uk/fatigue/understand" />
```

---

## 5. Module Mapping

### State → Module Mapping

| State | Module |
|-------|--------|
| fatigue | nastrij |
| tension | nastrij |
| anxiety | nastrij |
| joy | nastrij |
| loss | kazkar |
| anticipation | podija |
| change | podija |

### Rationale
- **Nastrij**: Emotional states (mood, feeling states)
- **Kazkar**: Memory and loss (preservation, remembering)
- **PoDija**: Future-oriented (anticipation, change, preparation)

---

## 6. Writes Policy

### Configuration
```yaml
min: 2
max: 3
mandatory:
  - calendar.time_point
  - gallery.experience_snapshot
optional_by_module:
  nastrij: nastrij.state_mark
  kazkar: kazkar.memory_node
  podija: podija.future_link
```

### Explanation
- **Minimum 2 writes**: Always calendar + gallery
- **Maximum 3 writes**: Mandatory + one optional module-specific write
- **Module-specific**: Depends on which module handles the state

---

## 7. API Implementation

### SEO Service
Location: `backend/app/config/seo/seo_service.py`

Core class: `SEOService`

#### Key Methods

```python
# Get canonical lists
get_states() -> List[str]
get_intents() -> List[str]
get_languages() -> List[str]

# Validation and routing
validate_routing(lang, state, intent) -> bool
build_url(lang, state, intent) -> str

# Entry resolution
get_entry(lang, state, intent) -> Dict
get_all_entries(lang) -> List[Dict]

# Module and policy
get_module(state) -> str
get_writes_policy(module) -> Dict

# Utilities
get_seeds(lang) -> Dict
generate_sitemap_entries(base_url) -> List[Dict]
```

### Ci Module Integration
Location: `backend/app/modules/ci/api.py`

#### Available Endpoints

```
GET /api/v1/ci/seo/states
GET /api/v1/ci/seo/intents
GET /api/v1/ci/seo/languages
GET /api/v1/ci/seo/entry/{lang}/{state}/{intent}
GET /api/v1/ci/seo/entries/{lang}
GET /api/v1/ci/seo/sitemap
GET /api/v1/ci/seo/seeds
GET /api/v1/ci/seo/module/{state}
```

---

## 8. Usage Examples

### Get SEO Entry
```bash
curl http://localhost:8000/api/v1/ci/seo/entry/en/fatigue/understand
```

Response:
```json
{
  "title": "Understand your fatigue",
  "description": "Explore and understand the nature of your fatigue",
  "url": "/en/fatigue/understand",
  "module": "nastrij",
  "writes_policy": {
    "min": 2,
    "max": 3,
    "mandatory": ["calendar.time_point", "gallery.experience_snapshot"],
    "optional": "nastrij.state_mark"
  },
  "state": "fatigue",
  "intent": "understand",
  "lang": "en"
}
```

### Get All Entries for Language
```bash
curl http://localhost:8000/api/v1/ci/seo/entries/uk
```

### Generate Sitemap
```bash
curl http://localhost:8000/api/v1/ci/seo/sitemap?base_url=https://cimeika.com
```

### Get Module Mapping
```bash
curl http://localhost:8000/api/v1/ci/seo/module/loss
```

Response:
```json
{
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

---

## 9. Frontend Integration (Recommended)

### React Router
```typescript
// routes.tsx
const routes = [
  {
    path: '/:lang/:state/:intent',
    element: <StateIntentPage />,
    loader: async ({ params }) => {
      const { lang, state, intent } = params;
      const response = await fetch(
        `/api/v1/ci/seo/entry/${lang}/${state}/${intent}`
      );
      return response.json();
    }
  }
];
```

### SEO Component
```typescript
// SEOHead.tsx
interface SEOHeadProps {
  entry: SEOEntry;
}

export const SEOHead: React.FC<SEOHeadProps> = ({ entry }) => {
  return (
    <Helmet>
      <title>{entry.title}</title>
      <meta name="description" content={entry.description} />
      <link rel="alternate" hreflang="en" href={`/en/${entry.state}/${entry.intent}`} />
      <link rel="alternate" hreflang="uk" href={`/uk/${entry.state}/${entry.intent}`} />
    </Helmet>
  );
};
```

---

## 10. Testing

### Manual Testing
```bash
# Start backend
cd backend
python main.py

# Test endpoints
curl http://localhost:8000/api/v1/ci/seo/states
curl http://localhost:8000/api/v1/ci/seo/entry/en/fatigue/understand
curl http://localhost:8000/api/v1/ci/seo/sitemap
```

### Expected Results
- All 7 states returned
- All 7 intents returned
- 49 entries per language (7×7)
- Valid routing for all combinations
- Correct module mapping
- Proper writes policy per module

---

## 11. Validation Rules

### Routing Validation
```python
# Valid
lang ∈ {en, uk}
state ∈ canonical_states
intent ∈ canonical_intents

# Invalid → 404
any other combination
```

### URL Validation
- Must start with `/{lang}/`
- Must contain valid state
- Must contain valid intent
- Format: `/{lang}/{state}/{intent}`

---

## 12. Sitemap Generation

### Structure
Each state/intent combination generates entries with:
- Primary URL (canonical, English)
- Alternate language URLs (hreflang)

### Example Entry
```json
{
  "loc": "https://cimeika.com/en/fatigue/understand",
  "alternates": [
    {
      "hreflang": "en",
      "href": "https://cimeika.com/en/fatigue/understand"
    },
    {
      "hreflang": "uk",
      "href": "https://cimeika.com/uk/fatigue/understand"
    }
  ]
}
```

### Total URLs
- 49 unique state/intent combinations
- 2 languages each
- 98 total URLs
- 49 sitemap entries (with alternates)

---

## 13. Cross-lingual Considerations

### Semantic Differences
- **anticipation** ↔ **передчуття** (more emotional in UK)
- **loss** ↔ **втрата** (deeper emotional context in UK)
- **prepare** ↔ **підготуватися** (more active tone in UK)

### Implementation
Both languages are treated equally, with EN as canonical for URL structure but UK having full content equivalence.

---

## 14. Success Criteria

✅ **SEO structure centralized**  
✅ **Modules receive correct data**  
✅ **Sitemap can be generated automatically**  
✅ **Bilingual support implemented**  
✅ **Routing validation in place**  
✅ **Module mapping functional**  
✅ **Writes policy resolver working**  

---

## 15. Future Enhancements (Optional)

### Potential additions:
- Additional languages (PL, RU, etc.)
- More granular states or intents
- Dynamic SEO content generation
- A/B testing support
- Analytics integration
- Rich snippets / structured data

---

## 16. Final Notes

### EN
This implementation is **recommendational**. Developers may adapt the SEO module to fit the specific architecture needs of Cimeika Unified. The core principles (7×7 matrix, module mapping, writes policy) should be preserved, but implementation details are flexible.

### UK
Ця реалізація має **рекомендаційний характер**. Розробники можуть адаптувати SEO‑модуль відповідно до конкретних архітектурних потреб Cimeika Unified. Основні принципи (матриця 7×7, мапування модулів, політика записів) мають зберігатися, але деталі реалізації гнучкі.

---

**Document Version**: 1.0.0  
**Implementation Location**: `backend/app/config/seo/`  
**API Endpoints**: `backend/app/modules/ci/api.py`  
**Last Updated**: 2025-12-20
