# CIMEIKA UNIFIED

Центральна екосистема проєкту Cimeika — інтегрована платформа для управління життям через 7 спеціалізованих модулів.

---

## ✅ Що працює зараз

### Backend
- **FastAPI** — єдиний backend framework
- **PostgreSQL** — основна база даних
- **7 модулів** — повний CRUD API для кожного модуля
  - Ci, Kazkar, Podija, Nastrij, Malya, Calendar, Gallery

### Frontend
- **React + Vite** — сучасний UI stack
- **7 модульних view** — повноекранні інтерфейси
- **Ci Overlay** — глобальний асистент
- **Детермінована тема** — залежить від модуля (kazkar=night, інші=day)

### Infrastructure
- **Docker Compose** — одна команда для запуску
- **Мінімальна конфігурація** — тільки необхідне

---

## 🚀 Запуск

```bash
# 1. Клонування
git clone https://github.com/Ihorog/cimeika-unified.git
cd cimeika-unified

# 2. Налаштування
cp .env.template .env
# Відредагуйте .env з вашими ключами

# 3. Запуск
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs
```

---

## 📦 Модулі

| Модуль | Маршрут | Опис | Тема |
|--------|---------|------|------|
| **Ci** | `/ci` | Центральне ядро, оркестрація | Day |
| **Казкар** | `/kazkar` | Пам'ять, історії, легенди | Night |
| **Подія** | `/podija` | Події, майбутнє, сценарії | Day |
| **Настрій** | `/nastrij` | Емоційні стани, контекст | Day |
| **Маля** | `/malya` | Ідеї, творчість, інновації | Day |
| **Галерея** | `/gallery` | Візуальний архів, медіа | Day |
| **Календар** | `/calendar` | Час, ритми, планування | Day |

---

## 🏗️ Структура

```
cimeika-unified/
├── backend/                # FastAPI application
│   ├── main.py            # Entry point
│   ├── app/
│   │   ├── modules/       # 7 module implementations
│   │   ├── core/          # Configuration
│   │   └── config/        # Database setup
│   └── Dockerfile
│
├── frontend/              # React application
│   ├── src/
│   │   ├── modules/       # 7 module views
│   │   ├── components/    # Shared components (CiOverlay)
│   │   ├── core/          # ThemeManager
│   │   └── styles/        # Global styles + themes
│   └── Dockerfile
│
├── archive/               # Archived code
│   └── flask/            # Previous Flask implementation
│
└── docker-compose.yml     # Orchestration
```

---

## 🔧 Технології

**Backend:**
- FastAPI 0.104
- SQLAlchemy 2.0
- PostgreSQL 15
- Pydantic

**Frontend:**
- React 18
- Vite
- React Router

**Infrastructure:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)

---

## 📝 Архівовано

- **Flask backend** → `/archive/flask/`  
  Попередня реалізація збережена для reference

- **Redis/Celery** → закоментовано в `docker-compose.yml`  
  Доступно для активації при потребі async tasks

---

## 📖 Документація

- [TECHNICAL_TASK.md](TECHNICAL_TASK.md) — повне технічне завдання
- [API Documentation](http://localhost:8000/api/docs) — Swagger UI (коли backend запущений)
- [QUICKSTART_DEV.md](QUICKSTART_DEV.md) — детальна інструкція для розробників

---

## 🤝 Розробка

```bash
# Backend (локально без Docker)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (локально без Docker)
cd frontend
npm install
npm run dev
```

---

**Створено з ❤️ для організації життя**

### Запуск
```bash
# Клонування
git clone https://github.com/Ihorog/cimeika-unified.git
cd cimeika-unified

# Налаштування environment
cp .env.template .env
# Відредагувати .env з вашими ключами (включно з OPENAI_API_KEY)
# Детальні інструкції: OPENAI_SETUP.md

# Запуск всього ecosystem
docker-compose up -d

# Backend буде доступний на http://localhost:5000
# Frontend буде доступний на http://localhost:3000
```

### 🤖 OpenAI Integration

Для роботи чат-функціоналу з GPT потрібен OpenAI API ключ:

1. Отримайте ключ на https://platform.openai.com/api-keys
2. Додайте `OPENAI_API_KEY` в `.env` файл
3. **Для CI/CD**: Додайте секрет в GitHub Settings → Secrets → Actions

📖 **Детальна інструкція**: [`OPENAI_SETUP.md`](OPENAI_SETUP.md)

---

## 📁 Структура проєкту
```
cimeika-unified/
├── backend/                 # Flask + FastAPI backend
│   ├── app/                # Application code
│   ├── api/                # REST API endpoints
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── ai/                 # AI integration layer
│   └── Dockerfile
│
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── modules/       # 7 модулів як компоненти
│   │   ├── shared/        # Спільні компоненти
│   │   └── layouts/       # Layout templates
│   └── Dockerfile
│
├── docker-compose.yml      # Orchestration
├── .env.template          # Environment template
└── docs/                  # Документація
```

---

## 🌐 Розгортання

### Vercel (Frontend)

#### Автоматичне розгортання (CI/CD)

Проєкт налаштовано для автоматичного розгортання через GitHub Actions:
- Push у `main` → Production deployment
- Pull Request → Preview deployment

**Інструкція налаштування:** [docs/GITHUB_ACTIONS_VERCEL.md](docs/GITHUB_ACTIONS_VERCEL.md)

#### Ручне розгортання

Фронтенд можна також розгорнути вручну:

```bash
# Використовуючи Vercel CLI
npm install -g vercel
vercel
```

Або підключіть репозиторій безпосередньо через [Vercel Dashboard](https://vercel.com).

**Детальна інструкція:** [docs/VERCEL_DEPLOYMENT.md](docs/VERCEL_DEPLOYMENT.md)

### Docker (Full Stack)

Для локальної розробки або самостійного хостингу:

```bash
docker-compose up -d
```

### Перевірка Розгортання

Після розгортання перевірте стан системи:

```bash
# Автоматична перевірка
./scripts/verify-deployment.sh

# Або вручну
curl http://localhost:5000/health
curl http://localhost:3000
```

**Документація:**
- [Повна інструкція з перевірки](docs/DEPLOYMENT_VERIFICATION.md)
- [Швидкий довідник](DEPLOYMENT_QUICKREF.md)

---

## 🔧 Технології

### Backend
- **Framework:** Flask, FastAPI
- **Database:** PostgreSQL (main), Redis (cache)
- **ORM:** SQLAlchemy
- **AI:** OpenAI API, Anthropic Claude API
- **Tasks:** Celery (async processing)

### Frontend
- **Framework:** React 18
- **Build:** Vite
- **State:** Zustand / Redux Toolkit
- **UI:** Tailwind CSS
- **i18n:** react-i18next (мультимовність)

### Infrastructure
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Hosting:** Vercel (frontend), Railway (backend)
- **Monitoring:** Sentry

---

## 🌍 Мови

**Основна мова:** Українська

**Підтримка:** Автоматична мультимовність для розширення аудиторії

---

## 📊 Статус розробки

**Поточна фаза:** Архітектура та API інтеграція

**Прогрес:** 50% (база готова, API endpoints реалізовано, активна розробка)

**Завершені етапи:**
1. ✅ Структура monorepo
2. ✅ Deployment verification
3. ✅ База даних schema
4. ✅ API endpoints (FastAPI з повним CRUD)
5. ✅ Service layer для всіх модулів
6. 🟡 AI integration
7. 🟡 Frontend модулі (базова інтеграція)
8. ⚪ Production deployment

**Детальна документація:**
- [API Documentation](docs/API_DOCUMENTATION.md)
- [Development Summary](docs/DEVELOPMENT_SUMMARY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Легенди Ci](docs/CI_LEGENDS_PLACEMENT.md) — Бібліотека легенд системи ✨
- [Дорожня карта дослідницької публікації](docs/CI_LEGEND_RESEARCH_ROADMAP.md) — "Легенда Ci" 📖

---

## 🤝 Контрибуція

Проєкт знаходиться в активній розробці. Контрибуції вітаються після стабілізації архітектури.

---

## 📄 Ліцензія

TBD

---

## 📖 Легенда Сі

**Легенда Сі** — бібліотека легенд системи Cimeika, що описує філософію, походження та принципи роботи.

### Доступ до легенд

- **Інтерактивний UI**: `/kazkar/legends` — галерея з пошуком та фільтрами
- **API**: `/api/v1/kazkar/legends` — REST endpoint
- **Документація**: [`docs/CI_LEGENDS_UNIFIED_RESOURCE.md`](./docs/CI_LEGENDS_UNIFIED_RESOURCE.md) ⭐

### Шість легенд Ci

1. Легенда про народження Ci
2. Легенда про семеро охоронців
3. Легенда про Kazkar — хранителя легенд
4. Принцип одного дотику
5. Легенда про бібліотеку без меж
6. Тиша і перша іскра: легенда про дуальність світобудови (15 вузлів)

**Детальна інформація**: [`docs/CI_LEGENDS_INDEX.md`](./docs/CI_LEGENDS_INDEX.md)

---

## 🔗 Посилання

- **Документація:** [ciwiki](https://github.com/Ihorog/ciwiki)
- **Legacy Backend:** [cimeika](https://github.com/Ihorog/cimeika)
- **Legacy Frontend:** [cimeika-real-time-data-app](https://github.com/Ihorog/cimeika-real-time-data-app)

---

**Створено з ❤️ для організації життя** 
