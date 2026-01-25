# Self-Improvement Mechanism

**Автоматичне виявлення відсутніх інструментів та генерація GitHub Issues**

---

## Огляд

Механізм самовдосконалення Cimeika автоматично:
1. Виявляє відсутні або неактивні інструменти в `manifest.json`
2. Генерує детальні описи GitHub Issues
3. Пропонує кроки для реалізації
4. Підтримує консистентність реєстру інструментів

---

## Структура

```
backend/app/core/
├── manifest.json            # Реєстр інструментів (джерело правди)
├── self_improvement.py      # Механізм самовдосконалення
└── tests/
    └── test_self_improvement.py  # Тести
```

---

## Використання

### Валідація всіх інструментів

```bash
cd backend
python -m app.core.self_improvement validate
```

**Вивід:**
```
=== Tool Manifest Validation ===

✅ All required tools are present and active
```

Або якщо є проблеми:
```
❌ Missing tools: tool1, tool2
⚠️  Inactive tools: tool3
```

### Генерація Issue для конкретного інструменту

```bash
python -m app.core.self_improvement generate-issue <tool_id> <reason>
```

**Приклад:**
```bash
python -m app.core.self_improvement generate-issue analytics_service missing
```

**Вивід:** Повний текст GitHub Issue з:
- Назвою issue
- Детальним описом проблеми
- Критеріями прийняття
- Кроками для реалізації
- Ресурсами та посиланнями

### Повний звіт

```bash
python -m app.core.self_improvement report
```

**Вивід:**
```
=== Self-Improvement Report ===

Found 2 issue(s) to report:

1. [Tool Missing] Add Analytics Service to Manifest
   Tool: analytics_service
   Reason: missing

2. [Tool Inactive] Reactivate Legacy Module
   Tool: legacy_module
   Reason: inactive

Generate individual issues with:
  python -m app.core.self_improvement generate-issue analytics_service missing
  python -m app.core.self_improvement generate-issue legacy_module inactive
```

---

## Manifest.json Schema

Реєстр інструментів визначає всі доступні модулі, сервіси та інтеграції.

### Структура інструменту

```json
{
  "id": "unique_tool_id",
  "name": "Human Readable Name",
  "description": "What this tool does",
  "status": "active|inactive|deprecated",
  "category": "core|module|service|integration",
  "endpoints": ["/api/v1/tool/endpoint"],
  "dependencies": ["ci_core"],
  "external_dependencies": ["ENV_VAR_NAME"]
}
```

### Категорії інструментів

- **core** — Основні системні компоненти (ci_core, orchestrator)
- **module** — Один з 7 основних модулів (kazkar, podija, тощо)
- **service** — Допоміжні сервіси (SEO, analytics, тощо)
- **integration** — Зовнішні API інтеграції (OpenAI, тощо)

### Статуси інструментів

- **active** — Інструмент працює і готовий до використання
- **inactive** — Інструмент існує але тимчасово вимкнений
- **deprecated** — Інструмент застарів і буде видалений

---

## Додавання нового інструменту

### Крок 1: Оновіть manifest.json

```json
{
  "id": "new_tool",
  "name": "New Tool Name",
  "description": "Tool description",
  "status": "active",
  "category": "module",
  "endpoints": ["/api/v1/new-tool/action"],
  "dependencies": ["ci_core"]
}
```

Додайте ID до `required_tools` або `optional_tools`:

```json
{
  "required_tools": ["ci_core", "kazkar", ..., "new_tool"],
  "optional_tools": ["ai_chat", "seo_service"]
}
```

### Крок 2: Валідуйте

```bash
python -m app.core.self_improvement validate
```

### Крок 3: Реалізуйте функціонал

Створіть модуль в `backend/app/modules/new_tool/`:
- `__init__.py`
- `routes.py` — API endpoints
- `service.py` — Бізнес-логіка
- `models.py` — Моделі даних

### Крок 4: Зареєструйте в головному додатку

Оновіть `backend/main.py` або відповідний роутер.

### Крок 5: Додайте тести

Створіть `backend/tests/test_new_tool.py`

### Крок 6: Оновіть документацію

- README.md — Додайте інструмент до списку модулів
- docs/ARCHITECTURE.md — Поясніть роль інструменту
- SYSTEM_WILL.md — Додайте вказівки для AI агентів

---

## API інтеграція

Механізм самовдосконалення можна інтегрувати в FastAPI:

```python
from app.core.self_improvement import validate_and_report

@app.get("/api/system/validate")
async def validate_system():
    """Validate all system tools"""
    result = validate_and_report()
    return result
```

---

## CI/CD інтеграція

Додайте валідацію в GitHub Actions:

```yaml
- name: Validate tool manifest
  run: |
    cd backend
    python -m app.core.self_improvement validate
```

---

## Приклади згенерованих Issues

### Issue для відсутнього інструменту

**Заголовок:** `[Tool Missing] Add Analytics Service to Manifest`

**Тіло:**
- Опис проблеми
- Необхідні дії
- Критерії прийняття
- Покрокова реалізація
- Ресурси та посилання
- Мітки (labels)

### Issue для неактивного інструменту

**Заголовок:** `[Tool Inactive] Reactivate Legacy Module`

**Тіло:**
- Опис проблеми
- Причини деактивації
- Кроки для реактивації
- Перевірка функціональності

---

## Тестування

Запуск всіх тестів:

```bash
cd backend
pytest tests/test_self_improvement.py -v
```

Тести покривають:
- Завантаження manifest.json
- Отримання інструментів
- Валідацію наявності
- Генерацію заголовків issues
- Генерацію тіла issues
- Валідацію схеми manifest

---

## Інтеграція з SYSTEM_WILL.md

Механізм самовдосконалення інтегрований з `SYSTEM_WILL.md` — документом для AI агентів.

**AI агенти повинні:**
1. Запускати валідацію перед початком роботи
2. Оновлювати manifest.json при додаванні інструментів
3. Запускати валідацію перед створенням PR
4. Слідувати згенерованим інструкціям в issues

**Детальніше:** Див. `SYSTEM_WILL.md` розділ "Self-Improvement Mechanism"

---

## Архітектура

```
┌─────────────────────┐
│   manifest.json     │  ← Джерело правди
│  (Tool Registry)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ self_improvement.py │
│                     │
│ ├─ ToolManifest     │  ← Завантаження та валідація
│ ├─ GitHubIssue...   │  ← Генерація issues
│ └─ validate_and...  │  ← Основна функція
└──────────┬──────────┘
           │
           ├───► CLI Interface
           ├───► API Endpoints
           ├───► CI/CD Pipelines
           └───► Tests
```

---

## Філософія

### ANTI-REPEAT PRINCIPLE

Механізм самовдосконалення втілює принцип анти-повторення:

❌ **Погано:** Вручну відстежувати відсутні інструменти
✅ **Добре:** Автоматична валідація з кожним PR

❌ **Погано:** Копіювати issue template для кожного інструменту
✅ **Добре:** Згенерувати issue автоматично з контекстом

❌ **Погано:** Забути оновити документацію
✅ **Добре:** Issue містить покрокові інструкції

---

## Майбутні покращення

- [ ] Інтеграція з GitHub API для автоматичного створення issues
- [ ] Сповіщення в Slack/Discord при виявленні проблем
- [ ] Моніторинг стану інструментів в production
- [ ] Автоматичне оновлення статусів інструментів
- [ ] Графічна візуалізація залежностей інструментів
- [ ] Історія змін manifest.json

---

## Troubleshooting

### Помилка: "manifest.json not found"

**Рішення:** Переконайтесь, що файл існує в `backend/app/core/manifest.json`

### Помилка: "Invalid JSON syntax"

**Рішення:** Перевірте синтаксис JSON:
```bash
python -m json.tool backend/app/core/manifest.json
```

### Валідація не виявляє проблеми

**Рішення:** Переконайтесь, що інструмент додано до `required_tools` в manifest.json

---

## Ресурси

- **Код:** `backend/app/core/self_improvement.py`
- **Тести:** `backend/tests/test_self_improvement.py`
- **Manifest:** `backend/app/core/manifest.json`
- **Документація для AI:** `SYSTEM_WILL.md`
- **Архітектура:** `docs/ARCHITECTURE.md`

---

## Контрибуція

При додаванні нових інструментів:

1. Оновіть `manifest.json`
2. Запустіть валідацію
3. Реалізуйте функціонал
4. Додайте тести
5. Оновіть документацію
6. Створіть PR

**Слідуйте ANTI-REPEAT PRINCIPLE — якщо щось повторюється, автоматизуйте це!**

---

**Версія:** 1.0.0  
**Створено:** 2026-01-25  
**Автор:** Cimeika Core Team

---

*"Система, що вдосконалює себе — майбутнє розробки"*
