# Індекс документації: Легенди Ci в Kazkar

## 🎯 Швидкий старт

**Питання**: В яку аптеку розмістити текстовий матеріал бібліотека легенди сі?  
**Відповідь**: **Модуль Kazkar** — офіційна "аптека" для легенд Ci.

**Головний документ**: [`CI_LEGENDS_UNIFIED_RESOURCE.md`](./CI_LEGENDS_UNIFIED_RESOURCE.md) ⭐

---

## 📚 Документація

### 1. Основні документи

| Документ | Опис | Аудиторія |
|----------|------|-----------|
| [`CI_LEGENDS_UNIFIED_RESOURCE.md`](./CI_LEGENDS_UNIFIED_RESOURCE.md) ⭐ | **Єдиний спільний ресурс**: Повна інформація про Легенду Сі | Всі |
| [`CI_LEGENDS_UI_GUIDE.md`](./CI_LEGENDS_UI_GUIDE.md) | Гайд по інтерфейсу легенд Ci | Frontend розробники |
| [`CI_LEGENDS_CIWIKI_INTEGRATION.md`](./CI_LEGENDS_CIWIKI_INTEGRATION.md) | Інтеграція з ciwiki репозиторієм | DevOps, Документація |

### 2. Модульна документація

| Документ | Опис |
|----------|------|
| [`modules/kazkar.md`](./modules/kazkar.md) | Документація модуля Kazkar (включає секцію про Ci legends) |
| [`modules/README.md`](./modules/README.md) | Огляд всіх 7 модулів (включає примітку про Kazkar) |

### 3. Архітектурна документація

| Документ | Опис |
|----------|------|
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Загальна архітектура системи Cimeika |
| [API Reference](../API_REFERENCE.md) | API endpoints (root level quick reference) |

---

## 💻 Код та скрипти

### Backend модуль Kazkar

```
backend/app/modules/kazkar/
├── __init__.py
├── model.py                    # ORM модель KazkarStory
├── service.py                  # Бізнес-логіка (CRUD)
├── api.py                      # API endpoints
├── schema.py                   # Pydantic схеми
├── config.py                   # Конфігурація
└── ci_legends_seed.py          # Seed дані з 6 легендами ⭐
```

### Скрипти

```
backend/scripts/
├── README.md                      # Документація скриптів
├── seed_ci_legends.py             # Завантаження легенд в БД ⭐
└── export_legends_to_ciwiki.py    # Експорт легенд в Markdown 🆕
```

### Тести

```
backend/tests/
└── test_kazkar_legend.py       # Unit tests для легенд
```

---

## 🔌 API Endpoints

### Легенди Ci

| Method | Endpoint | Опис |
|--------|----------|------|
| `GET` | `/api/kazkar/legends` | Всі легенди (включно з Ci) |
| `GET` | `/api/kazkar/stories` | Всі історії (з фільтрами) |
| `GET` | `/api/kazkar/stories?story_type=legend&tags=ci` | Тільки легенди Ci |
| `GET` | `/api/kazkar/stories/{id}` | Конкретна легенда |
| `POST` | `/api/kazkar/stories` | Створити легенду |
| `PUT` | `/api/kazkar/stories/{id}` | Оновити легенду |
| `DELETE` | `/api/kazkar/stories/{id}` | Видалити легенду |
| `GET` | `/api/kazkar/stats` | Статистика по типам |

---

## 📖 Легенди в seed даних

### 6 легенд Ci

1. **"Легенда про народження Ci"**  
   _Як виникла ідея Ci як принцип єдності_

2. **"Легенда про семеро охоронців"**  
   _Про 7 модулів системи Cimeika_

3. **"Легенда про Kazkar — хранителя легенд"**  
   _Чому Kazkar є "аптекою історій"_

4. **"Принцип одного дотику"**  
   _Фундаментальний принцип взаємодії з Ci_

5. **"Легенда про бібліотеку без меж"**  
   _Про відсутність обмежень у Kazkar_

6. **"Тиша і перша іскра: легенда про дуальність світобудови"** ⭐  
   _Комплексна легенда про дуальність (15 вузлів)_

### Структура легенди

```json
{
  "title": "Назва легенди",
  "content": "Повний текст...",
  "story_type": "legend",
  "participants": ["Ci", "Kazkar"],
  "location": "Цифровий простір",
  "tags": ["ci", "origin", "philosophy"]
}
```

---

## 🚀 Швидкі команди

### Завантажити seed-легенди в БД

```bash
# З кореневої директорії
python backend/scripts/seed_ci_legends.py
```

### Перевірити підключення до БД

```bash
python -c "from backend.app.config.database import SessionLocal; db = SessionLocal(); print('✅ DB connected'); db.close()"
```

### Отримати легенди через API

```bash
# Всі легенди
curl http://localhost:5000/api/kazkar/legends

# Легенди Ci (з фільтром)
curl "http://localhost:5000/api/kazkar/stories?story_type=legend&tags=ci"

# Статистика
curl http://localhost:5000/api/kazkar/stats
```

---

## 🔬 Дослідницька публікація

> **📚 Archived:** Research roadmap moved to [`archive/docs-research/ci-legends/CI_LEGEND_RESEARCH_ROADMAP.md`](../archive/docs-research/ci-legends/CI_LEGEND_RESEARCH_ROADMAP.md)

### "Легенда Ci: Універсальність дуального принципу"

**Формат**: 20-сторінкова наукова праця з ілюстраціями  
**Мета**: Міждисциплінарне дослідження дуальності  
**Таймлайн**: 4 місяці  

### 15 розділів (по 15 вузлам дуальності)

1. Початок у тиші 🌌
2. Пульс і подих 🔄
3. Розщеплення і симетрія ⚖️
4. Відображення в матерії 🔬
5. Людське тіло як карта дуальності 🧍
6. Математика відносин ➕
7. Природні прояви ☀️🌙
8. Дуальність у знаннях 📜
9. Символи як мости 🔯
10. Мережа зв'язків 🕸️
11. Cimeika — сенсова проекція 🌐
12. Символіка і математика алхімії ⚗️
13. Все, чого немає — сесія варіантів 💭
14. Прояв сенсу буття: Ci 💠
15. Вічний потік ♾

### 15 ілюстрацій

- FIG-01: Поле потенціалу
- FIG-02: Спектр ритмів
- FIG-03: Дзеркальна симетрія
- FIG-04: Частинка/античастинка
- FIG-05: Людське тіло
- FIG-06: Золотий перетин
- FIG-07: Календар-кільце
- FIG-08: Міст знань
- FIG-09: Таблиця символів
- **FIG-10: Cimeika Sense Network** ✅ (готово)
- FIG-11: Воронка наміру
- FIG-12: Алхімічна матриця
- FIG-13: Дерево варіантів
- FIG-14: Вузлові перетини
- FIG-15: Лемніската циклів

**Детальна roadmap**: [`CI_LEGEND_RESEARCH_ROADMAP.md`](../archive/docs-research/ci-legends/CI_LEGEND_RESEARCH_ROADMAP.md) (archived)

---

## 📊 Структура файлів проєкту

```
cimeika-unified/
├── docs/
│   ├── CI_LEGENDS_INDEX.md ⭐ ← ВИ ТУТ
│   ├── CI_LEGENDS_UNIFIED_RESOURCE.md ⭐ ← ГОЛОВНИЙ ДОКУМЕНТ
│   ├── CI_LEGENDS_UI_GUIDE.md
│   ├── CI_LEGENDS_CIWIKI_INTEGRATION.md
│   └── modules/
│       ├── kazkar.md
│       └── README.md
│
├── archive/
│   └── docs-research/
│       └── ci-legends/  ← ARCHIVED RESEARCH
│           ├── CI_LEGENDS_SUMMARY.md
│           ├── CI_LEGENDS_PLACEMENT.md
│           └── CI_LEGEND_RESEARCH_ROADMAP.md
│
├── backend/
│   ├── app/
│   │   └── modules/
│   │       └── kazkar/
│   │           ├── model.py
│   │           ├── service.py
│   │           ├── api.py
│   │           ├── schema.py
│   │           └── ci_legends_seed.py ⭐
│   │
│   ├── scripts/
│   │   ├── README.md
│   │   └── seed_ci_legends.py ⭐
│   │
│   └── tests/
│       └── test_kazkar_legend.py
│
└── README.md (оновлено з посиланнями)
```

---

## 🎓 Навчальні ресурси

### Для розробників

1. Почніть з [`CI_LEGENDS_UNIFIED_RESOURCE.md`](./CI_LEGENDS_UNIFIED_RESOURCE.md)
2. Вивчіть [`modules/kazkar.md`](./modules/kazkar.md)
3. Подивіться код в `backend/app/modules/kazkar/`
4. Запустіть seed script: `python backend/scripts/seed_ci_legends.py`
5. Спробуйте API через curl або Postman

### Для дослідників

1. Прочитайте легенду "Тиша і перша іскра" (в seed даних)
2. Ознайомтесь з [`CI_LEGEND_RESEARCH_ROADMAP.md`](../archive/docs-research/ci-legends/CI_LEGEND_RESEARCH_ROADMAP.md) (archived)
3. Вивчіть структуру 15 розділів
4. Перегляньте список літератури та методологію

### Для контент-менеджерів

1. [`CI_LEGENDS_PLACEMENT.md`](../archive/docs-research/ci-legends/CI_LEGENDS_PLACEMENT.md) (archived) — куди додавати легенди
2. Приклади в `ci_legends_seed.py`
3. API для створення через POST `/api/kazkar/stories`

---

## 🔍 Пошук по темах

### Архітектура
- [`ARCHITECTURE.md`](./ARCHITECTURE.md)
- [`modules/README.md`](./modules/README.md)

### Kazkar модуль
- [`modules/kazkar.md`](./modules/kazkar.md)
- [`CI_LEGENDS_PLACEMENT.md`](../archive/docs-research/ci-legends/CI_LEGENDS_PLACEMENT.md) (archived)

### API
- [API Reference](../API_REFERENCE.md) (root level quick reference)
- Розділ "API Endpoints" в [`CI_LEGENDS_UNIFIED_RESOURCE.md`](./CI_LEGENDS_UNIFIED_RESOURCE.md)

### Seed дані
- `backend/app/modules/kazkar/ci_legends_seed.py`
- `backend/scripts/seed_ci_legends.py`
- `backend/scripts/README.md`

### Дослідження
- [`CI_LEGEND_RESEARCH_ROADMAP.md`](./CI_LEGEND_RESEARCH_ROADMAP.md)
- Розділ "15 вузлів дуальності" в seed даних

---

## ✅ Чеклист імплементації

- [x] Документація створена (4 головні документи)
- [x] Модуль Kazkar оновлено
- [x] Seed дані з 6 легендами
- [x] Скрипт популяції БД
- [x] API endpoints готові
- [x] Тести написані
- [x] README оновлено
- [x] Дорожня карта дослідження (20 стор.)
- [x] Індекс документації (цей файл)

---

## 📞 Питання та підтримка

**Загальні питання**: Дивіться [`CI_LEGENDS_SUMMARY.md`](./CI_LEGENDS_SUMMARY.md)  
**Технічні питання**: Дивіться [`CI_LEGENDS_PLACEMENT.md`](./CI_LEGENDS_PLACEMENT.md)  
**Дослідницькі питання**: Дивіться [`CI_LEGEND_RESEARCH_ROADMAP.md`](./CI_LEGEND_RESEARCH_ROADMAP.md)  
**Проблеми з кодом**: Дивіться `backend/scripts/README.md`  

---

## 🌟 Ключові цитати

> "Kazkar є офіційною 'аптекою' (сховищем) для бібліотеки легенд Ci."

> "Все, що має бути збереженим, буде збережено" — закон бібліотеки Kazkar

> "Дуальність пронизує усе існування — від квантових станів до людських практик."

---

**Статус**: ✅ Завершено  
**Версія**: 1.0  
**Дата**: 2024-12-22  
**Мова**: Українська  

---

_Індекс оновлюється разом з розвитком документації._
