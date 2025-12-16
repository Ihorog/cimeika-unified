# CIMEIKA Backend

Flask + FastAPI backend для CIMEIKA екосистеми.

## Структура

```
backend/
├── app/                # Основний код додатку
├── api/                # REST API endpoints
├── models/             # Моделі бази даних (SQLAlchemy)
├── services/           # Бізнес-логіка
├── ai/                 # Інтеграція з AI (OpenAI, Claude)
├── main.py             # Точка входу
├── requirements.txt    # Python залежності
└── Dockerfile         # Docker конфігурація
```

## Розробка

### Локальний запуск

1. Створіть віртуальне середовище:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустіть сервер:
   ```bash
   python main.py
   ```

Backend буде доступний на http://localhost:5000

### API Endpoints

- `GET /` - Статус API
- `GET /health` - Health check
- `GET /api/v1/modules` - Список модулів

## Технології

- **Flask** - Web framework
- **FastAPI** - Modern API framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - База даних
- **Redis** - Кеш
- **Celery** - Асинхронні задачі
- **OpenAI/Anthropic** - AI інтеграція
