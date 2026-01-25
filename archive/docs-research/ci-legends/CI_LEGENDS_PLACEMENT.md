# Розміщення бібліотеки легенд Ci

## Питання
**В яку аптеку розмістити текстовий матеріал бібліотека легенди сі?**

## Відповідь
Текстовий матеріал бібліотеки легенд Ci розміщується в модулі **Kazkar**.

---

## Обґрунтування

### 1. Призначення модуля Kazkar
**Kazkar** (Казкар) — це модуль пам'яті, історій та легенд. Саме цей модуль призначений для збереження та організації:
- Спогадів
- Історій
- Легенд
- Фактів

### 2. Технічна реалізація

#### Backend структура
```
backend/app/modules/kazkar/
├── model.py      # KazkarStory model з полем story_type="legend"
├── service.py    # KazkarService з методом get_legends()
├── api.py        # API endpoint /api/kazkar/legends
└── schema.py     # Pydantic schemas для валідації
```

#### API для легенд
- **GET** `/api/kazkar/legends` — отримати всі легенди
- **POST** `/api/kazkar/stories` — створити нову легенду (з `story_type: "legend"`)
- **GET** `/api/kazkar/stories/{id}` — отримати конкретну легенду
- **PUT** `/api/kazkar/stories/{id}` — оновити легенду
- **DELETE** `/api/kazkar/stories/{id}` — видалити легенду

### 3. Структура легенди Ci

#### Приклад створення легенди:
```json
{
  "title": "Легенда про створення Ci",
  "content": "Давним-давно, коли світ був наповнений хаосом інформації...",
  "story_type": "legend",
  "tags": ["ci", "origin", "founding"],
  "participants": ["Ci"],
  "location": "Цифровий простір"
}
```

#### Поля легенди:
- `title` (обов'язково) — назва легенди
- `content` (обов'язково) — текст легенди
- `story_type` — тип запису: `"legend"`, `"story"`, `"memory"`, `"fact"`
- `participants` — учасники легенди
- `location` — місце, де відбувалися події
- `tags` — теги для категоризації
- `source_trace` — джерело або посилання

### 4. Типи легенд у Kazkar

Kazkar підтримує різні типи записів:
- **legend** — легенди (в т.ч. легенди Ci)
- **story** — історії
- **memory** — спогади
- **fact** — факти

Для легенд Ci використовується `story_type: "legend"` з тегом `"ci"`.

---

## Практичне використання

### Створення легенди Ci через API
```bash
curl -X POST http://localhost:5000/api/kazkar/stories \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Легенда про Ci",
    "content": "Текст легенди...",
    "story_type": "legend",
    "tags": ["ci", "legend"]
  }'
```

### Отримання всіх легенд
```bash
curl http://localhost:5000/api/kazkar/legends
```

### Фільтрація легенд Ci
```bash
curl http://localhost:5000/api/kazkar/stories?story_type=legend
```

---

## Висновок

✅ **Модуль Kazkar** — це офіційна "аптека" (сховище) для бібліотеки легенд Ci.

✅ Всі текстові матеріали легенд Ci повинні зберігатися як записи типу `story_type: "legend"` з тегом `"ci"`.

✅ Kazkar забезпечує повний функціонал для створення, читання, оновлення та видалення легенд.

---

## Зв'язки з іншими модулями

- **Ci** — центральний модуль може посилатися на легенди через Kazkar API
- **Calendar** — легенди можуть бути прив'язані до конкретних дат
- **Gallery** — медіа-вкладення до легенд
- **PoDija** — події з легенд на таймлайні

---

## Додаткова інформація

Детальну документацію модуля Kazkar див.: [`docs/modules/kazkar.md`](./modules/kazkar.md)
