# SEO Matrix API Reference

**Version:** 1.0.0  
**Base URL:** `http://localhost:5000/api/v1/seo/matrix`

---

## Quick Reference

### Product & Strategy

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/strategy` | GET | Get product strategy and positioning |
| `/status` | GET | Get implementation status and execution plan |

### Content Structure

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/modules` | GET | Get all 7 modules |
| `/modules/{module_id}` | GET | Get specific module |
| `/categories` | GET | Get all 7 traffic categories |
| `/patterns` | GET | Get all 49 patterns (7×7 matrix) |
| `/patterns/{module_id}/{category_id}` | GET | Get specific pattern |
| `/pages` | GET | Get all 98 pages |

### SEO Technical

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sitemap` | GET | Get sitemap entries (JSON) |
| `/sitemap.xml` | GET | Get sitemap XML |
| `/robots.txt` | GET | Get robots.txt |

---

## Detailed Reference

### GET /api/v1/seo/matrix/strategy

Get product strategy and positioning.

**Response:**
```json
{
  "status": "success",
  "strategy": {
    "wedge_market": "Family Memory & Planning Hub",
    "core_promise": "Фото → Історія → Календар → Друк",
    "primary_cta": "Створити приватний сімейний простір",
    "non_goals": ["..."]
  }
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/strategy
```

---

### GET /api/v1/seo/matrix/modules

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
    {
      "id": "kazkar",
      "name": "Kazkar",
      "role": "історії + сенс + легенда ci"
    },
    ...
  ]
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/modules
```

---

### GET /api/v1/seo/matrix/modules/{module_id}

Get specific module details.

**Parameters:**
- `module_id` (path) - Module identifier (ci, kazkar, podija, nastrij, malya, calendar, gallery)

**Response:**
```json
{
  "status": "success",
  "module": {
    "id": "kazkar",
    "name": "Kazkar",
    "role": "історії + сенс + легенда ci"
  }
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/modules/kazkar
```

---

### GET /api/v1/seo/matrix/categories

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
    {
      "id": "how_to",
      "name": "Як зробити"
    },
    ...
  ]
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/categories
```

---

### GET /api/v1/seo/matrix/patterns

Get all patterns (7×7 matrix).

**Query Parameters:**
- `module` (optional) - Filter by module ID

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
      "how_to": {
        "intent": "onboarding",
        "pages": ["ci/how-to-start", "ci/how-to-private-space"]
      },
      ...
    },
    ...
  }
}
```

**cURL Examples:**
```bash
# Get all patterns
curl http://localhost:5000/api/v1/seo/matrix/patterns

# Get patterns for specific module
curl http://localhost:5000/api/v1/seo/matrix/patterns?module=kazkar
```

---

### GET /api/v1/seo/matrix/patterns/{module_id}/{category_id}

Get specific pattern.

**Parameters:**
- `module_id` (path) - Module identifier
- `category_id` (path) - Category identifier

**Response:**
```json
{
  "status": "success",
  "module": "kazkar",
  "category": "examples",
  "pattern": {
    "intent": "examples",
    "pages": [
      "kazkar/examples/wedding",
      "kazkar/examples/winter"
    ]
  }
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/patterns/kazkar/examples
```

---

### GET /api/v1/seo/matrix/pages

Get all pages.

**Query Parameters:**
- `module` (optional) - Filter by module ID

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

**cURL Examples:**
```bash
# Get all pages
curl http://localhost:5000/api/v1/seo/matrix/pages

# Get pages for specific module
curl http://localhost:5000/api/v1/seo/matrix/pages?module=gallery
```

---

### GET /api/v1/seo/matrix/sitemap

Get sitemap entries in JSON format.

**Query Parameters:**
- `base_url` (optional, default: `https://cimeika.com`) - Base URL for the site

**Response:**
```json
{
  "status": "success",
  "sitemap": [
    {
      "loc": "https://cimeika.com/en/ci/actions",
      "alternates": [
        {
          "hreflang": "en",
          "href": "https://cimeika.com/en/ci/actions"
        },
        {
          "hreflang": "uk",
          "href": "https://cimeika.com/ua/ci/actions"
        }
      ]
    },
    ...
  ],
  "count": 98
}
```

**cURL Examples:**
```bash
# Default base URL
curl http://localhost:5000/api/v1/seo/matrix/sitemap

# Custom base URL
curl "http://localhost:5000/api/v1/seo/matrix/sitemap?base_url=https://example.com"
```

---

### GET /api/v1/seo/matrix/sitemap.xml

Get sitemap in XML format (for search engines).

**Query Parameters:**
- `base_url` (optional, default: `https://cimeika.com`) - Base URL for the site

**Response:** XML content
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://cimeika.com/en/ci/actions</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://cimeika.com/en/ci/actions" />
    <xhtml:link rel="alternate" hreflang="uk" href="https://cimeika.com/ua/ci/actions" />
  </url>
  ...
</urlset>
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/sitemap.xml
```

---

### GET /api/v1/seo/matrix/robots.txt

Get robots.txt content.

**Query Parameters:**
- `sitemap_url` (optional, default: `https://cimeika.com/sitemap.xml`) - URL to sitemap

**Response:** Plain text
```
User-agent: *
Allow: /

Sitemap: https://cimeika.com/sitemap.xml
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/robots.txt
```

---

### GET /api/v1/seo/matrix/status

Get implementation status and execution strategy.

**Response:**
```json
{
  "status": "success",
  "implementation_status": {
    "audit_external": "+",
    "positioning_wedge": "+",
    "matrix_7x7": "+",
    "blockers": {
      "brand_keyword_conflict_semeyka": "-",
      "landing_value_prop_clarity": "-",
      "international_ia_en": "-",
      "indexation_technical_seo": "-"
    }
  },
  "priority_order": [
    "+ define single landing promise + CTA + first wedge pages",
    "+ build IA: /en and /ua, canonical slugs латиницею",
    "+ technical SEO: sitemap/robots/canonicals/og/schema",
    "+ content factory: 49 pages skeleton (thin → expand)"
  ],
  "gates": {
    "go_to_stage_2_when": [
      "landing bounce improves",
      "organic impressions start growing",
      "first 20 pages indexed cleanly"
    ]
  }
}
```

**cURL Example:**
```bash
curl http://localhost:5000/api/v1/seo/matrix/status
```

---

## Error Responses

All endpoints return errors in a consistent format:

```json
{
  "status": "error",
  "message": "Error description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Not found
- `500` - Internal server error

---

## Usage Examples

### Python with requests

```python
import requests

base_url = "http://localhost:5000/api/v1/seo/matrix"

# Get all modules
response = requests.get(f"{base_url}/modules")
modules = response.json()['modules']

# Get specific pattern
response = requests.get(f"{base_url}/patterns/kazkar/examples")
pattern = response.json()['pattern']

# Get sitemap
response = requests.get(f"{base_url}/sitemap?base_url=https://example.com")
sitemap = response.json()['sitemap']
```

### JavaScript with fetch

```javascript
const baseUrl = 'http://localhost:5000/api/v1/seo/matrix';

// Get all modules
const response = await fetch(`${baseUrl}/modules`);
const data = await response.json();
const modules = data.modules;

// Get pages for module
const pagesResponse = await fetch(`${baseUrl}/pages?module=ci`);
const pagesData = await pagesResponse.json();
const pages = pagesData.pages;
```

---

## Testing

### Quick Test Script

```bash
#!/bin/bash
BASE_URL="http://localhost:5000/api/v1/seo/matrix"

echo "Testing SEO Matrix API..."

# Test strategy
echo "1. Strategy:"
curl -s "$BASE_URL/strategy" | jq '.strategy.wedge_market'

# Test modules
echo "2. Modules count:"
curl -s "$BASE_URL/modules" | jq '.modules | length'

# Test patterns
echo "3. Total patterns:"
curl -s "$BASE_URL/patterns" | jq '[.patterns[] | length] | add'

# Test pages
echo "4. Total pages:"
curl -s "$BASE_URL/pages" | jq '.count'

echo "✓ Tests complete"
```

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-22  
**Documentation:** See [SEO_MATRIX_GUIDE.md](./SEO_MATRIX_GUIDE.md) for complete guide
