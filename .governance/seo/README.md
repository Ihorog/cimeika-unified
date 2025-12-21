# SEO Governance — Automation & Health Monitoring

## Огляд контуру

Цей контур реалізує автоматизований моніторинг SEO-здоров'я з можливістю:
- **Моніторинг**: перевірка аномалій, волатильності рейтингів, дрейфу індексації
- **Алерти**: автоматичні повідомлення при виявленні проблем
- **Auto-ticket**: автоматичне створення GitHub Issues при перевищенні порогів
- **Governance cadence**: щотижневі перевірки, щомісячні огляди стратегії

## Структура файлів

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
