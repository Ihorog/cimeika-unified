# SEO Matrix Implementation Guide
## Family Memory & Planning Hub

**Version:** 1.0.0  
**Date:** 2025-12-22  
**Status:** ✅ Implemented

---

## Overview

This implementation provides a comprehensive SEO strategy for Cimeika as a **Family Memory & Planning Hub**, based on the 7×7 content matrix pattern (7 modules × 7 traffic categories = 49 content patterns).

### Product Strategy

- **Wedge Market:** Family Memory & Planning Hub
- **Core Promise:** Фото → Історія → Календар → Друк
- **Primary CTA:** Створити приватний сімейний простір

### Network Matrix

#### 7 Modules
1. **Ci** - інтерфейс + оркестрація дій
2. **Kazkar** - історії + сенс + легенда ci
3. **PoDija** - події + майбутнє
4. **Nastrij** - стан + емоційний контекст
5. **Malya** - ідеї + варіанти
6. **Calendar** - ритм + планування
7. **Gallery** - архів + друк + шеринґ

#### 7 Traffic Categories
1. **use_cases** - Сценарії використання
2. **how_to** - Як зробити
3. **templates** - Шаблони
4. **examples** - Приклади/історії
5. **features** - Функції
6. **problems** - Проблеми/виправлення
7. **comparisons** - Порівняння

---

## Architecture

### Files Structure

```
.governance/seo/
  └── cimeika_seo_matrix.yaml       # Source of truth

backend/app/config/
  ├── cimeika_seo_matrix.yaml       # Backend copy
  └── seo/
      ├── __init__.py
      ├── seo_service.py            # Legacy service (states×intents)
      └── seo_matrix_service.py     # New service (modules×categories)

backend/
  ├── main.py                       # API endpoints
  ├── test_seo_matrix_service.py   # Test suite
  └── generate_content_skeleton.py # Content generator
```

### URL Structure

#### Format
```
/{lang}/{module}/{category}[/page]
```

#### Examples
```
/en/ci/use_cases
/ua/kazkar/examples
/en/gallery/how-to/album
/ua/calendar/features/sync
```

---

## API Endpoints

### Product Strategy

#### `GET /api/v1/seo/matrix/strategy`
Get product strategy and positioning.

**Response:**
```json
{
  "status": "success",
  "strategy": {
    "wedge_market": "Family Memory & Planning Hub",
    "core_promise": "Фото → Історія → Календар → Друк",
    "primary_cta": "Створити приватний сімейний простір",
    "non_goals": [...]
  }
}
```

### Modules

#### `GET /api/v1/seo/matrix/modules`
Get all modules.

**Response:**
```json
{
  "status": "success",
  "modules": [
    {
      "id": "ci",
      "name": "Ci",
      "role": "інтерфейс + оркестрація дій"
    },
    ...
  ]
}
```

#### `GET /api/v1/seo/matrix/modules/{module_id}`
Get specific module details.

**Example:** `/api/v1/seo/matrix/modules/kazkar`

### Categories

#### `GET /api/v1/seo/matrix/categories`
Get all traffic categories.

**Response:**
```json
{
  "status": "success",
  "categories": [
    {
      "id": "use_cases",
      "name": "Сценарії"
    },
    ...
  ]
}
```

### Patterns

#### `GET /api/v1/seo/matrix/patterns`
Get all patterns (7×7 matrix).

**Query Parameters:**
- `module` (optional) - Filter by module

**Response:**
```json
{
  "status": "success",
  "patterns": {
    "ci": {
      "use_cases": {
        "intent": "action hub",
        "pages": ["ci/actions", "ci/quick-panel"]
      },
      ...
    }
  }
}
```

#### `GET /api/v1/seo/matrix/patterns/{module_id}/{category_id}`
Get specific pattern.

**Example:** `/api/v1/seo/matrix/patterns/kazkar/examples`

### Pages

#### `GET /api/v1/seo/matrix/pages`
Get all pages.

**Query Parameters:**
- `module` (optional) - Filter by module

**Response:**
```json
{
  "status": "success",
  "pages": [
    {
      "module": "ci",
      "category": "use_cases",
      "intent": "action hub",
      "slug": "ci/actions",
      "url_en": "/en/ci/actions",
      "url_ua": "/ua/ci/actions"
    },
    ...
  ],
  "count": 98
}
```

### SEO Technical

#### `GET /api/v1/seo/matrix/sitemap`
Generate sitemap entries.

**Query Parameters:**
- `base_url` (optional, default: `https://cimeika.com`)

**Response:**
```json
{
  "status": "success",
  "sitemap": [
    {
      "loc": "https://cimeika.com/en/ci/actions",
      "alternates": [
        {"hreflang": "en", "href": "https://cimeika.com/en/ci/actions"},
        {"hreflang": "uk", "href": "https://cimeika.com/ua/ci/actions"}
      ]
    },
    ...
  ],
  "count": 98
}
```

#### `GET /api/v1/seo/matrix/sitemap.xml`
Generate sitemap XML.

**Query Parameters:**
- `base_url` (optional)

**Response:** XML content

#### `GET /api/v1/seo/matrix/robots.txt`
Generate robots.txt.

**Query Parameters:**
- `sitemap_url` (optional)

**Response:** Plain text content

### Status

#### `GET /api/v1/seo/matrix/status`
Get implementation status and execution strategy.

**Response:**
```json
{
  "status": "success",
  "implementation_status": {
    "audit_external": "+",
    "positioning_wedge": "+",
    "matrix_7x7": "+",
    "blockers": {...}
  },
  "priority_order": [...],
  "gates": {...}
}
```

---

## Usage Examples

### Python

```python
from app.config.seo import get_seo_matrix_service

# Initialize service
service = get_seo_matrix_service()

# Get product strategy
print(service.wedge_market)  # "Family Memory & Planning Hub"
print(service.core_promise)  # "Фото → Історія → Календар → Друк"

# Get modules
modules = service.get_modules()  # List of 7 modules

# Get pattern
pattern = service.get_pattern('kazkar', 'examples')
print(pattern['intent'])  # "examples"
print(pattern['pages'])   # ["kazkar/examples/wedding", ...]

# Get all pages
pages = service.get_all_pages()  # 98 pages
ci_pages = service.get_all_pages('ci')  # 14 CI module pages

# Generate sitemap
entries = service.generate_sitemap_entries('https://cimeika.com')
xml = service.generate_sitemap_xml('https://cimeika.com')

# Generate robots.txt
robots = service.generate_robots_txt()

# Generate meta tags
tags = service.generate_meta_tags(
    title="Family Stories - Kazkar",
    description="Capture and share your family stories",
    url="https://cimeika.com/en/kazkar/family-stories",
    image="https://cimeika.com/og-image.jpg"
)
```

### cURL

```bash
# Get product strategy
curl http://localhost:5000/api/v1/seo/matrix/strategy

# Get modules
curl http://localhost:5000/api/v1/seo/matrix/modules

# Get patterns for Kazkar module
curl http://localhost:5000/api/v1/seo/matrix/patterns?module=kazkar

# Get specific pattern
curl http://localhost:5000/api/v1/seo/matrix/patterns/ci/use_cases

# Get all pages
curl http://localhost:5000/api/v1/seo/matrix/pages

# Get sitemap
curl http://localhost:5000/api/v1/seo/matrix/sitemap

# Get sitemap XML
curl http://localhost:5000/api/v1/seo/matrix/sitemap.xml

# Get robots.txt
curl http://localhost:5000/api/v1/seo/matrix/robots.txt

# Get implementation status
curl http://localhost:5000/api/v1/seo/matrix/status
```

---

## Content Generation

### Generate All Content Skeletons

```bash
cd backend

# Dry run (see what would be created)
python generate_content_skeleton.py --dry-run

# Generate files
python generate_content_skeleton.py --output ./content

# Generate with index pages
python generate_content_skeleton.py --output ./content --index
```

This will generate:
- 98 markdown files (49 pages × 2 languages)
- 2 index pages (en/index.md, ua/index.md)

### Generated File Structure

```
content/
├── en/
│   ├── index.md
│   ├── ci/
│   │   ├── actions.md
│   │   ├── how-to-start.md
│   │   └── ...
│   ├── kazkar/
│   │   ├── family-stories.md
│   │   └── ...
│   └── ...
└── ua/
    ├── index.md
    ├── ci/
    │   ├── actions.md
    │   └── ...
    └── ...
```

### Page Template

Each generated page includes:
- YAML frontmatter with metadata
- Title and description
- Overview section
- Key features list
- How to use guide
- Related pages links
- CTA

---

## Testing

### Run Test Suite

```bash
cd backend
python test_seo_matrix_service.py
```

### Test Coverage

The test suite validates:
- ✅ Service initialization
- ✅ Product strategy (wedge, promise, CTA)
- ✅ 7 modules
- ✅ 7 traffic categories
- ✅ 49 patterns (7×7 matrix)
- ✅ 98 pages (49 × 2 languages)
- ✅ URL generation
- ✅ Sitemap generation
- ✅ Robots.txt generation
- ✅ Meta tags generation
- ✅ Status & execution strategy

**Result:** 11/11 tests passing ✅

---

## Execution Strategy

### Priority Order

1. ✅ Define single landing promise + CTA + first wedge pages
2. ⏳ Build IA: /en and /ua, canonical slugs латиницею
3. ⏳ Technical SEO: sitemap/robots/canonicals/og/schema
4. ⏳ Content factory: 49 pages skeleton (thin → expand)

### Go-to-Stage-2 Gates

- Landing bounce improves
- Organic impressions start growing
- First 20 pages indexed cleanly

---

## Implementation Status

### Completed ✅

- Product strategy defined
- Network matrix (7 modules + 7 categories)
- 49 content patterns
- SEO Matrix Service implementation
- 13 API endpoints
- Sitemap generation
- Robots.txt generation
- Meta tags generation
- Test suite (11/11 passing)
- Content skeleton generator

### Current Blockers ⚠️

- `brand_keyword_conflict_semeyka` - Brand keyword conflicts
- `landing_value_prop_clarity` - Landing page value proposition clarity
- `international_ia_en` - International information architecture (EN)
- `indexation_technical_seo` - Technical SEO for indexation

---

## Next Steps

### Phase 1: Infrastructure (Complete)
- ✅ SEO matrix configuration
- ✅ Backend service
- ✅ API endpoints
- ✅ Content generator

### Phase 2: Content Creation (In Progress)
- ⏳ Generate content skeletons
- ⏳ Define landing page structure
- ⏳ Create first wedge pages (priority: Kazkar, Gallery)
- ⏳ Write initial content (thin → expand approach)

### Phase 3: Technical SEO
- ⏳ Implement canonical tags
- ⏳ Add Open Graph meta tags
- ⏳ Add structured data (Schema.org)
- ⏳ Configure robots.txt
- ⏳ Deploy sitemap

### Phase 4: Optimization
- ⏳ Monitor indexation
- ⏳ Track organic impressions
- ⏳ Measure landing bounce
- ⏳ Expand thin content
- ⏳ Iterate based on data

---

## Best Practices

### Content Development

1. **Start Thin**: Create basic skeletons for all pages first
2. **Expand Strategically**: Prioritize based on search intent and business goals
3. **Bilingual Consistency**: Maintain parallel structure across EN/UA
4. **Intent Alignment**: Match content to user intent for each category

### SEO Technical

1. **Canonical Tags**: Always specify canonical URL
2. **Hreflang Tags**: Include alternates for all languages
3. **Meta Tags**: Keep titles ≤60 chars, descriptions ≤155 chars
4. **Sitemap**: Regenerate after content changes
5. **Robots.txt**: Keep simple and permissive

### URL Structure

1. **Clean Slugs**: Use Latin characters, lowercase, hyphens
2. **Consistent Pattern**: /{lang}/{module}/{category}/[page]
3. **No Duplication**: One canonical URL per page
4. **Bilingual Parity**: EN and UA versions for all pages

---

## Support

### Documentation
- 📖 This guide
- 📖 `SEO_README.md` - Overview
- 📖 `SEO_QUICKREF.md` - Quick reference
- 📖 API documentation in code

### Code
- 💻 `backend/app/config/seo/seo_matrix_service.py` - Service implementation
- 💻 `backend/main.py` - API endpoints
- 🧪 `backend/test_seo_matrix_service.py` - Tests
- 🛠️ `backend/generate_content_skeleton.py` - Content generator

### Configuration
- ⚙️ `.governance/seo/cimeika_seo_matrix.yaml` - Source of truth
- ⚙️ `backend/app/config/cimeika_seo_matrix.yaml` - Backend config

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-22  
**Status:** ✅ Implementation Complete - Ready for Content Creation
