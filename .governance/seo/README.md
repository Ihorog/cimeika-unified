# SEO Governance & Strategy

**Version:** 1.0.0  
**Status:** ✅ Implementation Complete  
**Date:** December 2025

---

## Overview

This directory contains the source of truth for Cimeika's SEO strategy and governance.

### Product Positioning

**Cimeika** is a **Family Memory & Planning Hub** that helps families:
- Capture and preserve memories (photos, stories)
- Plan events and milestones
- Share experiences in a private space
- Create printed keepsakes

**Core Promise:** Фото → Історія → Календар → Друк

---

## Files

### `cimeika_seo_matrix.yaml`

The canonical SEO configuration file containing:

1. **Product Strategy** - Wedge market, core promise, primary CTA
2. **Network Matrix** - 7 modules × 7 traffic categories
3. **Patterns (7×7)** - 49 content patterns with intent and pages
4. **Execution Strategy** - Priority order and gates
5. **SEO Automation Layer** - Monitoring and alerts
6. **Governance Loop** - Cadences and decision authority

### `README.md`

This file - governance documentation.

---

## SEO Strategy Matrix

### 7 Modules

1. **Ci** - Interface & orchestration
2. **Kazkar** - Stories & memories
3. **PoDija** - Events & future
4. **Nastrij** - Emotional state tracking
5. **Malya** - Ideas & brainstorming
6. **Calendar** - Rhythm & planning
7. **Gallery** - Photo archive & printing

### 7 Traffic Categories

1. **use_cases** - Usage scenarios
2. **how_to** - How-to guides
3. **templates** - Templates & starters
4. **examples** - Examples & stories
5. **features** - Feature descriptions
6. **problems** - Troubleshooting
7. **comparisons** - Product comparisons

### 49 Content Patterns = 7 modules × 7 categories

---

## Implementation

### Backend

- **Service:** `backend/app/config/seo/seo_matrix_service.py`
- **Config:** `backend/app/config/cimeika_seo_matrix.yaml`
- **API:** 13 endpoints at `/api/v1/seo/matrix/*`
- **Tests:** 11/11 passing ✅

### Documentation

- 📖 [SEO Matrix Guide](../../docs/SEO_MATRIX_GUIDE.md) - Complete guide
- 📖 [API Reference](../../docs/SEO_API_REFERENCE.md) - API docs
- 📖 [SEO README](../../docs/SEO_README.md) - Overview

---

## Automation & Monitoring

### SEO Health Checks

Automated weekly checks for:
- **Anomaly detection** (dynamic threshold)
- **Ranking volatility** (medium sensitivity)
- **Indexation drift** (3% tolerance)

### Workflow

GitHub Actions: `.github/workflows/seo-health.yml`

Schedule:
- Weekly: Monday 06:00 UTC
- On changes to `.governance/seo/**`
- Manual: workflow_dispatch

---

## Governance Cadences

| Cadence | Frequency | Output |
|---------|-----------|--------|
| Weekly Health Checks | Weekly | health_report |
| Monthly Strategy Review | Monthly | strategy_adjustments |
| Quarterly Matrix Refactor | Quarterly | seo_matrix_v_next |

---

## Structure Files (Legacy)

```
.governance/seo/
  ├─ cimeika_seo_matrix.yaml    # Конфігурація (source of truth)
  └─ README.md                   # Ця документація

scripts/seo/
  ├─ seo_health_report.mjs       # Генератор звітів
  ├─ seo_rules.mjs               # Правила оцінювання
  └─ seo_sources_stub.mjs        # Stub джерела даних

.github/workflows/
  └─ seo-health.yml              # GitHub Actions workflow
```

## Як запустити workflow вручну

1. Перейдіть на GitHub: `Actions` → `seo-health`
2. Натисніть `Run workflow`
3. Виберіть гілку (зазвичай `main`)
4. Натисніть зелену кнопку `Run workflow`

## Як переглянути звіти

Після виконання workflow:
1. Перейдіть у запуск workflow
2. Знайдіть секцію `Artifacts` внизу сторінки
3. Завантажте `health_report.json` або `health_report.md`

## Симуляція дрейфу (локальний запуск)

Для тестування з різними значеннями дрейфу:

```bash
# Нормальний дрейф (< 3%)
export SEO_STUB_DRIFT_PERCENT=2.0
node scripts/seo/seo_health_report.mjs

# Критичний дрейф (> 3%) — створить auto-ticket
export SEO_STUB_DRIFT_PERCENT=5.5
node scripts/seo/seo_health_report.mjs

# Висока волатильність
export SEO_STUB_VOLATILITY_SCORE=0.75
node scripts/seo/seo_health_report.mjs

# Аномалія
export SEO_STUB_ANOMALY_SCORE=0.85
node scripts/seo/seo_health_report.mjs
```

## Зміна tolerance_percent

Відредагуйте файл `.governance/seo/cimeika_seo_matrix.yaml`:

```yaml
seo_automation_layer:
  automations:
    - name: indexation_drift_monitoring
      tolerance_percent: 3  # ← змініть це значення
      action: auto_ticket
```

Після зміни workflow автоматично використає нове значення при наступному запуску.

## Auto-ticket логіка

Якщо `drift_percent > tolerance_percent`:
- ✅ Створюється GitHub Issue
- 🏷️ Лейбли: `seo:auto_ticket`, `governance`
- 📝 У тілі Issue: timestamp, drift_percent, tolerance_percent, next steps

## Розклад

- **Щотижня**: понеділок 09:00 Europe/Kyiv (06:00 UTC)
- **При змінах**: push у `.governance/seo/**` або `scripts/seo/**`
- **Вручну**: workflow_dispatch

## Governance cadences

Згідно з `cimeika_seo_matrix.yaml`:

| Cadence | Частота | Output |
|---------|---------|--------|
| weekly_health_checks | щотижня | health_report |
| monthly_strategy_review | щомісяця | strategy_adjustments |
| quarterly_matrix_refactor | щокварталу | seo_matrix_v_next |

## Примітки

- На даному етапі використовуються **stub-джерела** (без реальних API)
- Для production інтеграції потрібно замінити `seo_sources_stub.mjs` на реальні джерела
- Секрети (Google Search Console токени) додаватимуться у наступних етапах
