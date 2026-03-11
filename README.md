# CIMEIKA UNIFIED

Центральна екосистема проєкту Cimeika — інтегрована платформа для управління життям через 7 спеціалізованих модулів.

---

## ✅ Що працює зараз

### Backend (FastAPI)
- **7 модулів** — CRUD API: Ci, Kazkar, Podija, Nastrij, Malya, Calendar, Gallery
- **PostgreSQL** — база даних з pgvector для семантичного пошуку
- **Chat API** — інтеграція з OpenAI GPT (GPT-3.5-turbo, GPT-4)
- **Telegram Bot** — повний набір команд для управління подіями (Podija)
- **Google Calendar** — синхронізація подій з Google Calendar
- **Background Workers** — фонові задачі для нагадувань та синхронізації
- **Health Endpoints** — `/health`, `/ready` для моніторингу стану
- **Rate Limiting** — обмеження запитів (60/хв на IP)
- **Sentry Monitoring** — опціональне відстеження помилок (якщо налаштовано)

### Frontend (React + Vite)
- **7 модульних view** — повноекранні інтерфейси для кожного модуля
- **Legend Ci** — система візуалізації легенд з радіальними мапами
- **Chat UI** — інтерфейс для взаємодії з AI
- **Welcome Page** — головна сторінка з онбордингом
- **CiFAB** — глобальний floating action button (завжди видимий, завжди доступний)
- **Детермінована тема** — залежить від модуля:
  - Kazkar: `night`
  - Всі інші: `day`

### Infrastructure
- **Docker Compose** — мінімальна конфігурація (frontend, backend, postgres)
- **GitHub Actions** — CI/CD pipeline з автоматичним тестуванням
- **Database Migrations** — Alembic для версіонування схеми БД
- **Makefile** — 30+ команд для розробки та деплою
- Redis/Celery закоментовані (не використовуються)

---

## 🚀 Запуск

### Вимоги
- Docker & Docker Compose

### Швидкий старт

```bash
# 1. Клонувати репозиторій
git clone https://github.com/Ihorog/cimeika-unified.git
cd cimeika-unified

# 2. Налаштувати environment
cp .env.example .env
# Відредагувати .env (паролі, API ключі)

# 3. Запустити всі сервіси (з Makefile)
make dev

# Або без Makefile:
docker compose up -d

# Доступ:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Основні Makefile команди

```bash
make dev          # Запустити всі сервіси
make down         # Зупинити всі сервіси
make logs         # Переглянути логи всіх сервісів
make logs-backend # Переглянути логи backend
make build        # Перебудувати Docker images
make test         # Запустити тести
make clean        # Видалити volumes (очистити дані!)
```

**Локальна розробка (без Docker):**

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload  # http://localhost:8000
```

Frontend:
```bash
cd frontend
npm ci
npm run dev  # http://localhost:3000
```

### Налаштування інтеграцій

**OpenAI API:**
- Див. [OPENAI_SETUP.md](OPENAI_SETUP.md) для детальних інструкцій
- Додати `OPENAI_API_KEY` в `.env`

**Telegram Bot (опціонально):**
- Створити бота через [@BotFather](https://t.me/BotFather)
- Додати `TELEGRAM_BOT_TOKEN` в `.env`
- Команди бота: `/add`, `/today`, `/week`, `/done`, `/cancel`, `/help`

**Google Calendar (опціонально):**
- Налаштувати Service Account credentials
- Додати `GOOGLE_CALENDAR_CREDENTIALS` в `.env`

**Sentry Monitoring (опціонально):**
- Додати `SENTRY_DSN` в `.env`

---

## 📦 Модулі

| Модуль | Маршрут | Опис | Основні можливості | Тема |
|--------|---------|------|-------------------|------|
| Ci | `/app/ci` | Центральне ядро, оркестрація | Координація модулів, легенди та історії, сигнали стану | day |
| Kazkar | `/app/kazkar` | Пам'ять, історії, легенди | WebSocket підтримка, семантичний пошук, seed легенд | night |
| Podija | `/app/podija` | Події, майбутнє, сценарії | Telegram бот, нагадування, парсинг подій, категорії | day |
| Nastrij | `/app/nastrij` | Емоційні стани, контекст | Відстеження настрою, емоційний контекст | day |
| Malya | `/app/malya` | Ідеї, творчість, інновації | Управління ідеями, креативне сховище | day |
| Calendar | `/app/calendar` | Час, ритми, планування | Google Calendar sync, управління часом | day |
| Gallery | `/app/gallery` | Візуальний архів, медіа | Управління медіа, візуальний архів | day |

### Детальніше про ключові модулі

**Ci (Центральне ядро):**
- Координатор всіх модулів
- Система легенд та історій з великим контентом
- Візуалізація легенд через радіальні мапи
- Управління станом через сигнали

**Kazkar (Пам'ять):**
- Real-time оновлення через WebSocket
- Семантичний пошук з pgvector
- Seed-дані для легенд
- Збереження історій

**Podija (Події):**
- Повна інтеграція з Telegram ботом
- Background worker для нагадувань
- Парсинг дат/часу подій українською
- 7 категорій подій (погода, гороскопи, події, ігри, свята, дозвілля, квести)
- Статуси: planned/done/cancelled

---

## 🏗️ Структура

```
cimeika-unified/
├── backend/
│   ├── main.py              # FastAPI entry point з lifespan manager
│   ├── app/
│   │   ├── api/v1/          # API версії 1
│   │   │   ├── router.py    # Головний роутер
│   │   │   ├── health.py    # Health/readiness endpoints
│   │   │   └── modules.py   # Управління модулями
│   │   ├── core/            # Ядро системи
│   │   │   ├── config.py    # Конфігурація
│   │   │   ├── logging.py   # Структуроване логування
│   │   │   ├── rate_limit.py # Rate limiting middleware
│   │   │   ├── monitoring.py # Sentry інтеграція
│   │   │   └── interfaces.py # Контракти модулів
│   │   └── modules/         # 7 модулів
│   │       ├── ci/          # + legend_ci_content.py, coordinator.py
│   │       ├── kazkar/      # + websocket.py, semantic search
│   │       ├── podija/      # + telegram.py, reminder_worker.py, parser.py
│   │       ├── nastrij/
│   │       ├── malya/
│   │       ├── calendar/    # + google_calendar.py, worker.py
│   │       └── gallery/
│   ├── alembic/             # Database migrations
│   ├── tests/               # Comprehensive test suite
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── modules/         # 7 module views + Legend Ci
│       │   ├── ci/CiView.jsx
│       │   ├── kazkar/KazkarView.jsx
│       │   ├── podija/PodijaView.jsx
│       │   ├── nastrij/NastrijView.jsx
│       │   ├── malya/MalyaView.jsx
│       │   ├── calendar/CalendarView.jsx
│       │   ├── gallery/GalleryView.jsx
│       │   └── legends/LegendCiView.jsx  # Візуалізація легенд
│       ├── pages/
│       │   ├── Chat.jsx     # AI чат інтерфейс
│       │   └── WelcomePage.jsx # Головна сторінка
│       ├── components/      # Спільні компоненти (CiFAB)
│       ├── core/            # ThemeManager, service layer
│       ├── services/        # API clients, hooks
│       └── layouts/         # MainLayout
│
├── android-webview/         # Android WebView app
│   ├── app/src/main/        # Kotlin code
│   │   └── java/           # Voice, TTS, overlay system
│   ├── README.md           # Android setup guide
│   └── build.gradle
│
├── archive/
│   └── flask/               # Archived Flask code
│
├── .github/
│   └── workflows/ci.yml     # GitHub Actions CI/CD
│
├── Makefile                 # 30+ development commands
├── docker-compose.yml       # Infrastructure orchestration
└── .env.example            # Environment template
```

---

## 📝 Архівовано

- **Flask backend** → `/archive/flask/`
  - Попередня реалізація (збережено для reference)
  - Включає: API modules, servers, AUTOHEAL scripts

- **Redis/Celery** → закоментовано в `docker-compose.yml`
  - Доступно для активації при потребі

---

## 🔧 Технічний стек

**Backend:**
- FastAPI 0.104
- SQLAlchemy 2.0
- PostgreSQL 15 + pgvector (семантичний пошук)
- Pydantic v2
- Alembic (migrations)
- pytest (тестування)

**Frontend:**
- React 18
- Vite
- React Router
- Axios

**Infrastructure:**
- Docker Compose
- GitHub Actions (CI/CD)
- Uvicorn (ASGI server)

**Інтеграції:**
- OpenAI GPT (GPT-3.5-turbo, GPT-4)
- Anthropic Claude (опціонально)
- Telegram Bot API
- Google Calendar API
- Sentry (опціонально)

**Майбутнє (закоментовано, готове до активації):**
- Redis (кешування, rate limiting)
- Celery (фонові задачі)

---

## 📖 Документація

### Основна документація
- [Backend README](backend/README.md) — детальна документація backend
- [TECHNICAL_TASK.md](TECHNICAL_TASK.md) — технічне завдання
- [CHANGELOG.md](CHANGELOG.md) — історія змін та версії
- [CONTRIBUTING.md](CONTRIBUTING.md) — як контрибутити

### Налаштування та розгортання
- [OPENAI_SETUP.md](OPENAI_SETUP.md) — налаштування OpenAI API
- [DEPLOYMENT_QUICKREF.md](DEPLOYMENT_QUICKREF.md) — швидкий посібник з деплою
- [QUICKSTART_DEV.md](QUICKSTART_DEV.md) — швидкий старт для розробників
- [VERCEL_QUICKSTART.md](VERCEL_QUICKSTART.md) — деплой на Vercel

### Android платформа
- [android-webview/README.md](android-webview/README.md) — Android WebView app з голосовими можливостями

### API та розробка
- [API_REFERENCE.md](API_REFERENCE.md) — довідник API endpoints
- [API Docs (Swagger)](http://localhost:8000/api/docs) — інтерактивна документація (коли backend запущений)
- [API Docs (ReDoc)](http://localhost:8000/api/redoc) — альтернативна документація

### Проблеми та покращення
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) — відомі проблеми та плани покращення

---

## 🚢 Платформи та деплой

**Web (основна платформа):**
- Frontend: Vercel або будь-який статичний хостинг
- Backend: Docker container на будь-якому хості

**Mobile:**
- Android: WebView app з нативними можливостями (голос, TTS, overlay)
- iOS: Progressive Web App (PWA)

**Development:**
- Docker Compose для локальної розробки
- Makefile для автоматизації команд

---

## 🧪 Тестування

```bash
# Запустити всі тести
make test

# Або без Makefile:
cd backend
pytest tests/ -v

# З coverage
pytest tests/ --cov=app --cov-report=html
```

**Test Suite:**
- 47+ тестів
- Health endpoints тести
- Module endpoints тести
- Security тести (rate limiting, CORS)
- Monitoring тести

---

## 🔒 Безпека

- **Rate Limiting:** 60 запитів/хв на IP, 1000/год
- **CORS:** Валідація origins, не дозволено wildcards в production
- **Pydantic Validation:** Валідація всіх вхідних даних
- **Sentry Monitoring:** Автоматичне відстеження помилок (опціонально)
- **Environment Validation:** Перевірка конфігурації при старті

---

**Створено з ❤️ для організації життя**
