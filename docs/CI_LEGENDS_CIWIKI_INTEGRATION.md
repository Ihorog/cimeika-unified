# Інтеграція Легенди Сі з ciwiki

## 🎯 Мета

Цей документ описує процес інтеграції "Легенда Сі" з репозиторієм ciwiki (документація Cimeika).

---

## 📋 Архітектура інтеграції

### Роль репозиторіїв

```
┌─────────────────────────────────────────────────────────────┐
│                     cimeika-unified                         │
│                   (PRIMARY SOURCE)                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ PostgreSQL Database                                  │  │
│  │ ├── 6 Ci Legends                                     │  │
│  │ └── Metadata (tags, participants, etc.)             │  │
│  └─────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           │ API                             │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ FastAPI Backend                                      │  │
│  │ └── /api/v1/kazkar/legends                          │  │
│  └─────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           │ React                           │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Interactive Web UI                                   │  │
│  │ └── /kazkar/legends (CiLegendsView)                 │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Export Script
                           │ (Markdown)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                        ciwiki                               │
│                 (DOCUMENTATION MIRROR)                      │
│                                                             │
│  Легенда-Сі/                                               │
│  ├── README.md                                             │
│  ├── 01-Легенда-про-народження-Ci.md                      │
│  ├── 02-Легенда-про-семеро-охоронців.md                   │
│  ├── 03-Легенда-про-Kazkar-хранителя-легенд.md           │
│  ├── 04-Принцип-одного-дотику.md                          │
│  ├── 05-Легенда-про-бібліотеку-без-меж.md                │
│  └── 06-Тиша-і-перша-іскра.md                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Workflow синхронізації

### Варіант A: Ручна синхронізація (поточна рекомендація)

**Крок 1: Експорт з cimeika-unified**

```bash
# Перейти в cimeika-unified
cd /path/to/cimeika-unified

# Запустити експорт скрипт
python backend/scripts/export_legends_to_ciwiki.py

# Результат: файли в tmp/ciwiki_export/
```

**Крок 2: Копіювання в ciwiki**

```bash
# Перейти в ciwiki репозиторій
cd /path/to/ciwiki

# Створити директорію (якщо не існує)
mkdir -p Легенда-Сі

# Скопіювати експортовані файли
cp /path/to/cimeika-unified/tmp/ciwiki_export/* ./Легенда-Сі/

# Перевірити файли
ls -la Легенда-Сі/
```

**Крок 3: Commit і push**

```bash
# Додати файли в git
git add Легенда-Сі/

# Commit з описовим повідомленням
git commit -m "docs: sync Легенда Сі from cimeika-unified [$(date +%Y-%m-%d)]"

# Push в ciwiki
git push origin main
```

**Частота**: За потребою (після змін легенд)

---

### Варіант B: Автоматична синхронізація (майбутнє)

**GitHub Action в cimeika-unified**

```yaml
# .github/workflows/sync-legends-to-ciwiki.yml

name: Sync Ci Legends to ciwiki

on:
  push:
    branches: [main]
    paths:
      - 'backend/app/modules/kazkar/ci_legends_seed.py'
      - 'backend/scripts/export_legends_to_ciwiki.py'
  workflow_dispatch:  # Ручний запуск

jobs:
  export-and-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout cimeika-unified
        uses: actions/checkout@v3
        
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
          cache-dependency-path: './backend/requirements.txt'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install sqlalchemy pydantic
      
      - name: Run export script
        run: |
          cd backend
          python scripts/export_legends_to_ciwiki.py
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
      
      - name: Checkout ciwiki
        uses: actions/checkout@v3
        with:
          repository: Ihorog/ciwiki
          path: ciwiki
          token: ${{ secrets.CIWIKI_PAT }}
      
      - name: Copy exported files
        run: |
          mkdir -p ciwiki/Легенда-Сі
          cp tmp/ciwiki_export/* ciwiki/Легенда-Сі/
      
      - name: Create Pull Request in ciwiki
        uses: peter-evans/create-pull-request@v5
        with:
          path: ciwiki
          token: ${{ secrets.CIWIKI_PAT }}
          commit-message: "docs: sync Легенда Сі [automated]"
          title: "📚 Sync Легенда Сі from cimeika-unified"
          body: |
            Автоматична синхронізація легенд Ci з cimeika-unified.
            
            Дата експорту: ${{ github.event.head_commit.timestamp }}
            Commit: ${{ github.sha }}
          branch: sync-ci-legends
```

**Переваги**:
- ✅ Автоматизація
- ✅ Консистентність
- ✅ Audit trail через PR
- ✅ Review можливість

**Недоліки**:
- ⚠️ Потрібен Personal Access Token
- ⚠️ Налаштування GitHub Actions
- ⚠️ Додаткова складність

---

### Варіант C: Read-only embed (альтернатива)

**У ciwiki замість статичних файлів**:

```markdown
# Легенда Сі

> Ці легенди доступні в інтерактивному форматі

🔗 **[Переглянути легенди в Cimeika](https://cimeika.app/kazkar/legends)**

## Чому інтерактивний інтерфейс?

- 🔍 **Пошук** — швидке знаходження легенд
- 🏷️ **Фільтри** — сортування за тегами
- 📱 **Responsive** — працює на всіх пристроях
- 🔄 **Актуальність** — завжди найсвіжіший контент
- ✨ **UX** — красивий дизайн з анімаціями

## Альтернатива: Markdown версії

Якщо вам потрібні статичні версії для офлайн читання:

1. Відкрийте [cimeika-unified repository](https://github.com/Ihorog/cimeika-unified)
2. Запустіть експорт: `python backend/scripts/export_legends_to_ciwiki.py`
3. Отримайте Markdown файли в `tmp/ciwiki_export/`
```

**Переваги**:
- ✅ Завжди актуально
- ✅ Немає синхронізації
- ✅ Одне джерело істини

**Недоліки**:
- ⚠️ Потрібен доступ до cimeika.app
- ⚠️ Не працює офлайн
- ⚠️ Менш зручно для швидкого read

---

## 📝 Структура файлів в ciwiki

### Рекомендована структура

```
ciwiki/
├── README.md                                    # Головна ciwiki
├── Легенда-Сі/                                 # Розділ легенд
│   ├── README.md                               # Індекс легенд
│   ├── 01-Легенда-про-народження-Ci.md
│   ├── 02-Легенда-про-семеро-охоронців.md
│   ├── 03-Легенда-про-Kazkar-хранителя-легенд.md
│   ├── 04-Принцип-одного-дотику.md
│   ├── 05-Легенда-про-бібліотеку-без-меж.md
│   └── 06-Тиша-і-перша-іскра.md
├── Модулі/                                     # Документація модулів
│   ├── README.md
│   ├── Ci.md
│   ├── Kazkar.md                               # Посилання на Легенду Сі
│   └── ...
└── Архітектура/
    └── ...
```

### Приклад вмісту README.md в Легенда-Сі/

```markdown
# Легенда Сі

> Бібліотека легенд системи Cimeika

---

## 🎯 Про Легенду Сі

**Легенда Сі** — це збірка текстових матеріалів про:
- Походження та філософію Cimeika
- Історію створення модулів
- Міфологію та символізм
- Ключові принципи

---

## 📚 Легенди

**Всього легенд**: 6

### 1. [Легенда про народження Ci](./01-Легенда-про-народження-Ci.md)
Як виникла ідея Ci як принцип єдності...
**Теги**: `ci`, `origin`, `founding`, `philosophy`

### 2. [Легенда про семеро охоронців](./02-Легенда-про-семеро-охоронців.md)
Про 7 модулів системи Cimeika...
**Теги**: `ci`, `modules`, `seven`, `unity`

[... інші легенди ...]

---

## 🔗 Інтерактивний інтерфейс

**Для повноцінної роботи використовуйте**:

🌐 [Легенди Ci в Cimeika](https://cimeika.app/kazkar/legends)

**Можливості**:
- 🔍 Пошук
- 🏷️ Фільтри
- 📖 Зручний UI
- ✏️ Створення нових

---

_Експортовано: 24.12.2025_
```

---

## 🔧 Налаштування експорт скрипта

### Перевірка роботи скрипта

```bash
# 1. Переконайтесь що БД запущена
docker-compose up -d postgres

# 2. Переконайтесь що легенди в БД
python backend/scripts/seed_ci_legends.py

# 3. Запустіть експорт
python backend/scripts/export_legends_to_ciwiki.py

# 4. Перевірте результат
ls -la tmp/ciwiki_export/
cat tmp/ciwiki_export/README.md
```

### Налаштування шляху експорту

Відредагуйте `backend/scripts/export_legends_to_ciwiki.py`:

```python
# Змініть шлях експорту (за замовчуванням: tmp/ciwiki_export)
export_dir = Path("/custom/path/to/export")
```

---

## 📊 Процес review змін

### Коли легенда змінюється в cimeika-unified

**1. Виявлення змін**
```bash
# В cimeika-unified
git log --oneline backend/app/modules/kazkar/ci_legends_seed.py
```

**2. Експорт оновленої версії**
```bash
python backend/scripts/export_legends_to_ciwiki.py
```

**3. Порівняння з ciwiki**
```bash
# В ciwiki
diff ./Легенда-Сі/01-*.md /path/to/cimeika-unified/tmp/ciwiki_export/01-*.md
```

**4. Update в ciwiki**
```bash
# Копіюємо тільки змінені файли
cp /path/to/export/01-*.md ./Легенда-Сі/
git add Легенда-Сі/01-*.md
git commit -m "docs: update Легенда про народження Ci"
```

---

## ✅ Checklist інтеграції

### Початкове налаштування

- [ ] Створити папку `Легенда-Сі` в ciwiki
- [ ] Запустити експорт скрипт
- [ ] Скопіювати всі файли в ciwiki
- [ ] Commit і push
- [ ] Додати посилання в головну README ciwiki
- [ ] Додати посилання в Модулі/Kazkar.md

### При кожній синхронізації

- [ ] Запустити експорт
- [ ] Перевірити diff
- [ ] Скопіювати оновлені файли
- [ ] Перевірити метадані (дата експорту)
- [ ] Commit з описовим повідомленням
- [ ] Push і перевірка в GitHub

### Для автоматизації (опціонально)

- [ ] Створити GitHub Action
- [ ] Налаштувати Personal Access Token
- [ ] Протестувати workflow
- [ ] Документувати процес
- [ ] Встановити schedule (якщо потрібно)

---

## 🎯 Best Practices

### 1. Єдине джерело істини

✅ **DO**: Редагувати легенди тільки в cimeika-unified  
❌ **DON'T**: Редагувати Markdown файли в ciwiki напряму

### 2. Часті синхронізації

✅ **DO**: Синхронізувати після кожної значної зміни  
❌ **DON'T**: Накопичувати багато змін перед синхронізацією

### 3. Описові commit messages

✅ **DO**: `docs: sync Легенда Сі - updated Тиша і перша іскра`  
❌ **DON'T**: `update`

### 4. Посилання на живий інтерфейс

✅ **DO**: Завжди вказувати лінк на /kazkar/legends  
❌ **DON'T**: Приховувати існування інтерактивного UI

### 5. Дата експорту

✅ **DO**: Вказувати дату в футері кожного файлу  
❌ **DON'T**: Забувати про версіонування

---

## 📞 Troubleshooting

### Помилка: "Легенди не знайдені в БД"

**Рішення**:
```bash
python backend/scripts/seed_ci_legends.py
```

### Помилка: "Database connection failed"

**Рішення**:
```bash
# Перевірте .env файл
cat .env | grep DATABASE_URL

# Запустіть PostgreSQL
docker-compose up -d postgres
```

### Помилка: "Permission denied" при експорті

**Рішення**:
```bash
chmod +x backend/scripts/export_legends_to_ciwiki.py
```

### Файли не копіюються в ciwiki

**Рішення**:
```bash
# Переконайтесь що шлях правильний
ls -la tmp/ciwiki_export/

# Створіть папку в ciwiki якщо не існує
mkdir -p /path/to/ciwiki/Легенда-Сі
```

---

## 🔗 Пов'язані документи

- [CI_LEGENDS_UNIFIED_RESOURCE.md](./CI_LEGENDS_UNIFIED_RESOURCE.md) — Єдиний ресурс
- [CI_LEGENDS_REPOSITORY_COMPARISON.md](./CI_LEGENDS_REPOSITORY_COMPARISON.md) — Порівняння репозиторіїв
- [CI_LEGENDS_PLACEMENT.md](./CI_LEGENDS_PLACEMENT.md) — Обґрунтування Kazkar

---

## 📅 Версія

**Створено**: 2025-12-24  
**Версія**: 1.0  
**Статус**: ✅ Готово до використання  
**Автор**: Cimeika Development Team

---

**Підсумок**: cimeika-unified є primary source, ciwiki є documentation mirror. Синхронізація через експорт скрипт (ручна або автоматична).
