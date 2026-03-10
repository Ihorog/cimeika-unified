# CIMEIKA UNIFIED

Центральна екосистема проєкту Cimeika — інтегрована платформа для управління життям через 7 спеціалізованих модулів.

---

## ✅ Що працює зараз

### Backend (FastAPI)
- **7 модулів** — CRUD API: Ci, Kazkar, Podija, Nastrij, Malya, Calendar, Gallery
- **PostgreSQL** — база даних з pgvector
- **Chat API** — інтеграція з OpenAI GPT

### Frontend (React + Vite)
- **7 модульних view** — повноекранні інтерфейси для кожного модуля
- **CiFAB** — глобальний floating action button (завжди видимий, завжди доступний)
- **Детермінована тема** — залежить від модуля:
  - Kazkar: `night`
  - Всі інші: `day`

### Infrastructure
- **Docker Compose** — мінімальна конфігурація (frontend, backend, postgres)
- Redis/Celery закоментовані (не використовуються)

---

## 🚀 Запуск

### Вимоги
- Docker & Docker Compose

### Команди

```bash
# 1. Клонувати репозиторій
git clone https://github.com/Ihorog/cimeika-unified.git
cd cimeika-unified

# 2. Налаштувати environment
cp .env.example .env
# Відредагувати .env (паролі, API ключі)

# 3. Запустити всі сервіси
docker compose up -d

# Доступ:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
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

---

## 📦 Модулі

| Модуль | Маршрут | Опис | Тема |
|--------|---------|------|------|
| Ci | `/app/ci` | Центральне ядро, оркестрація | day |
| Kazkar | `/app/kazkar` | Пам'ять, історії, легенди | night |
| Podija | `/app/podija` | Події, майбутнє, сценарії | day |
| Nastrij | `/app/nastrij` | Емоційні стани, контекст | day |
| Malya | `/app/malya` | Ідеї, творчість, інновації | day |
| Calendar | `/app/calendar` | Час, ритми, планування | day |
| Gallery | `/app/gallery` | Візуальний архів, медіа | day |

---

## 🏗️ Структура

```
cimeika-unified/
├── backend/
│   ├── main.py              # FastAPI entry point
│   └── app/
│       ├── core/            # Configuration
│       └── modules/         # 7 module implementations
│           ├── ci/
│           ├── kazkar/
│           ├── podija/
│           ├── nastrij/
│           ├── malya/
│           ├── calendar/
│           └── gallery/
│
├── frontend/
│   └── src/
│       ├── modules/         # 7 module views (.jsx)
│       │   ├── ci/CiView.jsx
│       │   ├── kazkar/KazkarView.jsx
│       │   ├── podija/PodijaView.jsx
│       │   ├── nastrij/NastrijView.jsx
│       │   ├── malya/MalyaView.jsx
│       │   ├── calendar/CalendarView.jsx
│       │   └── gallery/GalleryView.jsx
│       ├── components/      # Shared components (CiFAB)
│       ├── core/            # ThemeManager
│       └── layouts/         # MainLayout
│
├── archive/
│   └── flask/               # Archived Flask code
│
└── docker-compose.yml       # Minimal orchestration
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
- PostgreSQL 15 + pgvector
- Pydantic

**Frontend:**
- React 18
- Vite
- React Router

**Infrastructure:**
- Docker Compose
- GitHub Actions

---

## 📖 Документація

- [TECHNICAL_TASK.md](TECHNICAL_TASK.md) — технічне завдання
- [API Docs](http://localhost:8000/api/docs) — Swagger UI (коли backend запущений)

---

**Створено з ❤️ для організації життя**
