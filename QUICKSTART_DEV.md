# Швидкий старт для розробки / Quick Start for Development

## 🚀 Запуск frontend для розробки

### Варіант 1: Тільки frontend (без backend)

Якщо вам потрібно працювати тільки з інтерфейсом:

```bash
# 1. Встановити залежності
cd frontend
npm install

# 2. Запустити dev server
npm run dev

# Frontend буде доступний на http://localhost:3000
```

**Що працює без backend:**
- ✅ Вітальна сторінка
- ✅ Навігація між модулями
- ✅ Інтерфейс чату (без відправки повідомлень)
- ✅ Інтерфейс всіх модулів (без даних з API)

**Що НЕ працює:**
- ❌ Відправка повідомлень в чаті
- ❌ Завантаження даних з API
- ❌ AI-функціонал

### Варіант 2: Frontend + Backend (повний стек)

Для повної функціональності:

```bash
# 1. Створити .env файл
cp .env.template .env

# 2. Відредагувати .env (мінімум потрібен OPENAI_API_KEY для чату)
nano .env  # або vim, або будь-який редактор

# 3. Запустити через Docker
docker-compose up -d

# АБО запустити окремо:

# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

**Доступ:**
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- API Docs: http://localhost:5000/api/docs

---

## 🐳 Local Development with Docker

### Prerequisites
- Docker 24+
- Docker Compose 2.20+

### Quick Start

1. **Clone and setup:**
```bash
git clone https://github.com/Ihorog/cimeika-unified.git
cd cimeika-unified
cp .env.example .env
# Edit .env and set your passwords and API keys
```

2. **Start all services:**
```bash
make dev
# or
docker compose up -d
```

3. **Check status:**
```bash
docker compose ps
docker compose logs backend
```

4. **Access:**
- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432

5. **Run migrations:**
```bash
make db-init
```

### Useful Commands

- `make db-up` - Start only PostgreSQL
- `make db-migrate msg="description"` - Create new migration
- `make stop` - Stop all services
- `make clean` - Remove all containers and volumes

### Testing PostgreSQL with pgvector

Check that pgvector extension is installed:
```bash
docker compose exec postgres psql -U cimeika_user -d cimeika -c "SELECT * FROM pg_extension WHERE extname='vector';"
```

Verify backend health:
```bash
curl http://localhost:8000/health
```

---

## 🔧 Виправлення помилок

### Помилка: "Порожня сторінка після навігації"

Якщо ви бачите порожню сторінку після переходу до модуля або чату, перевірте консоль браузера. Якщо там є помилка про React Hooks - переконайтеся, що використовуєте останню версію коду.

### Помилка: "ERR_CONNECTION_REFUSED"

Це нормально, якщо backend не запущений. Інтерфейс працюватиме, але без даних з API.

## 📝 Структура проекту

```
cimeika-unified/
├── frontend/          # React + Vite frontend
│   ├── src/
│   │   ├── components/  # Спільні компоненти
│   │   ├── modules/     # 7 модулів системи
│   │   ├── pages/       # Сторінки (Welcome, Chat, etc.)
│   │   └── App.jsx      # Головний роутинг
│   └── package.json
│
├── backend/           # Flask + FastAPI backend
│   ├── api/          # REST API endpoints
│   ├── models/       # Database models
│   ├── services/     # Business logic
│   └── main.py       # Flask entry point
│
└── docker-compose.yml  # Orchestration
```

## 🎯 Модулі системи

1. **Ci** - Центральне ядро, оркестрація
2. **Казкар** - Пам'ять, історії, легенди
3. **ПоДія** - Події, майбутнє, сценарії
4. **Настрій** - Емоційні стани, контекст
5. **Маля** - Ідеї, творчість, інновації
6. **Галерея** - Візуальний архів, медіа
7. **Календар** - Час, ритми, планування

## 🐛 Відомі проблеми

- Module initialization warnings в консолі - нормально, якщо backend не запущений
- "Failed to fetch" помилки - нормально без backend

## 📚 Додаткова документація

- [README.md](./README.md) - Головна документація
- [DEPLOYMENT_QUICKREF.md](./DEPLOYMENT_QUICKREF.md) - Швидкий довідник з розгортання
- [docs/](./docs/) - Детальна документація

---

**Створено з ❤️ для організації життя**
