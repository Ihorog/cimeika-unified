# GitHub Copilot Instructions — Cimeika Unified

Цей репозиторій має фіксовану архітектуру.  
Copilot діє як інженер-асистент і **НЕ змінює структуру або патерни без прямої вказівки**.

---

## 1. Загальні правила

- Дотримуйся існуючої структури репозиторію.
- Генеруй код лише у визначених папках.
- Один файл — одна відповідальність.
- Ніяких прихованих абстракцій або "покращень наперед".
- Якщо не впевнений — **не вигадуй**.

---

## 2. Структура репозиторію (НЕ ЗМІНЮВАТИ)

```
cimeika-unified/
├─ backend/
├─ frontend/
├─ docs/
├─ infra/
├─ scripts/
├─ .github/
```

Заборонено створювати нові кореневі папки.

---

## 3. Backend — базові правила

### Стек
- Python ≥ 3.11
- FastAPI (основний API)
- SQLAlchemy 2.0
- Pydantic v2

### Структура

```
backend/app/
├─ core/
├─ modules/
├─ api/
├─ models/
├─ services/
├─ config/
└─ utils/
```

---

## 4. Backend — Core (Ci)

`backend/app/core/`:
- orchestration / координація
- реєстрація модулів
- глобальний контекст

Правила:
- Core **не містить** доменної логіки модулів
- Core **не імпортує** UI або API
- Взаємодія з модулями — тільки через інтерфейси/реєстр

---

## 5. Backend — модулі (7, фіксовані)

Назви модулів (НЕ змінювати):
- `ci`
- `kazkar`
- `podija`
- `nastrij`
- `malya`
- `gallery`
- `calendar`

Стандарт кожного модуля:

```
module/
├─ api.py
├─ service.py
├─ model.py
├─ schema.py
├─ config.py
└─ __init__.py
```

Правила:
- `api.py` → тільки маршрути
- `service.py` → бізнес-логіка
- `model.py` → ORM
- `schema.py` → Pydantic
- Заборонені циклічні імпорти

---

## 6. API Layer

- Всі маршрути через `backend/app/api/`
- Версія: `/api/v1`
- OpenAPI/Swagger увімкнено
- Всі відповіді типізовані

---

## 7. Frontend — базові правила

### Стек
- React 18
- TypeScript (`strict: true`)
- Zustand
- Vite
- Tailwind

### Структура

```
frontend/
├─ app/
├─ components/
├─ modules/
├─ stores/
├─ services/
├─ styles/
└─ assets/
```

---

## 8. Frontend — модулі (дзеркально backend)

Назви:
- `Ci`
- `Kazkar`
- `Podija`
- `Nastrij`
- `Malya`
- `Gallery`
- `Calendar`

Стандарт модуля:

```
Module/
├─ views/
├─ components/
├─ hooks/
├─ service.ts
├─ store.ts
└─ index.ts
```

Правила:
- `views` — orchestration UI, без бізнес-логіки
- `service.ts` — API / data layer
- `store.ts` — state (без HTTP напряму)

---

## 9. Імпорти та залежності

Заборонено:
- циклічні імпорти
- імпорт з інших модулів напряму (обхід core або API)
- "utils для всього" без чіткої ролі

---

## 10. Стиль коду

- Читабельний
- Мінімалістичний
- Без "магії"
- Коментарі — лише де критично
- Без псевдо-архітектурних рішень

---

## 11. Коміти (якщо Copilot пропонує)

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `refactor: ...`
- `chore: ...`

Одна логічна зміна = один коміт.

---

## 12. Головне правило

**Це частина Cimeika.  
Структура первинна.  
Якщо немає чіткої задачі — не ускладнюй.**

---

Сі
