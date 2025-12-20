# Перевірка Розгортання CIMEIKA

Цей документ описує процес перевірки успішності розгортання екосистеми CIMEIKA.

## 📋 Огляд

Перевірка розгортання включає:
- ✅ Перевірку стану Docker контейнерів
- ✅ Перевірку доступності Backend API
- ✅ Перевірку Frontend додатку
- ✅ Перевірку конфігураційних файлів
- ✅ Тестування основних endpoints

---

## 🚀 Швидка Перевірка

### Автоматична перевірка (рекомендовано)

```bash
# Надайте права на виконання скрипту
chmod +x scripts/verify-deployment.sh

# Запустіть перевірку
./scripts/verify-deployment.sh
```

Скрипт автоматично перевірить:
- Docker контейнери
- Backend endpoints
- Frontend доступність
- Конфігураційні файли

### Результат

✅ **PASSED** - Всі сервіси працюють коректно
❌ **FAILED** - Є проблеми, які потребують уваги

---

## 🔍 Ручна Перевірка

### 1. Перевірка Docker Контейнерів

```bash
# Перегляд статусу всіх контейнерів
docker compose ps

# Очікуваний результат: 5 контейнерів у статусі "running"
# - cimeika-postgres
# - cimeika-redis
# - cimeika-backend
# - cimeika-frontend
# - cimeika-celery-worker
```

**Здорові контейнери:**
```
NAME                    STATUS
cimeika-postgres        Up X minutes (healthy)
cimeika-redis           Up X minutes (healthy)
cimeika-backend         Up X minutes
cimeika-frontend        Up X minutes
cimeika-celery-worker   Up X minutes
```

### 2. Перевірка Backend API

#### 2.1 Health Check

```bash
curl http://localhost:5000/health
```

**Очікувана відповідь:**
```json
{
  "status": "healthy",
  "message": "Backend is running",
  "canon_bundle_id": "...",
  "timestamp": "5000"
}
```

#### 2.2 Root Endpoint

```bash
curl http://localhost:5000/
```

**Очікувана відповідь:**
```json
{
  "status": "success",
  "message": "CIMEIKA Backend API is running",
  "version": "0.1.0",
  "canon_bundle_id": "...",
  "modules": [...]
}
```

#### 2.3 Modules API

```bash
curl http://localhost:5000/api/v1/modules
```

**Очікувана відповідь:**
```json
{
  "canon_bundle_id": "...",
  "modules": [
    {
      "id": "ci",
      "name": "Ci",
      "description": "Центральне ядро, оркестрація",
      "status": "in_development"
    },
    // ... інші модулі
  ]
}
```

### 3. Перевірка Frontend

#### 3.1 Homepage

Відкрийте у браузері:
```
http://localhost:3000
```

**Очікуваний результат:**
- ✅ Сторінка завантажується
- ✅ Відображається головна сторінка CIMEIKA
- ✅ Навігаційне меню доступне
- ✅ Немає помилок у консолі браузера

#### 3.2 Health Check UI

Відкрийте у браузері:
```
http://localhost:3000/health
```

**Очікуваний результат:**
- ✅ Сторінка health check завантажується
- ✅ Відображається загальний статус: HEALTHY
- ✅ Frontend Status: healthy
- ✅ Backend Status: healthy (якщо backend доступний)
- ✅ Modules Status: success (відображається список 7 модулів)
- ✅ Автоматичне оновлення кожні 30 секунд

**Можливості Health Check UI:**
- Візуальна перевірка стану всіх компонентів
- Кнопка "Оновити" для ручного оновлення
- Автоматичне оновлення статусу
- Детальна інформація про кожен модуль
- Відображення помилок, якщо вони є

#### 3.3 Маршрути модулів

Перевірте доступність всіх модулів:
- http://localhost:3000/ci
- http://localhost:3000/kazkar
- http://localhost:3000/podija
- http://localhost:3000/nastrij
- http://localhost:3000/malya
- http://localhost:3000/calendar
- http://localhost:3000/gallery

**Швидка перевірка через curl:**
```bash
# Frontend health check (JSON)
curl -s http://localhost:3000/health | grep -o "CIMEIKA"

# Або відкрийте в браузері для візуального інтерфейсу
```

### 4. Перевірка Логів

```bash
# Перегляд логів всіх сервісів
docker compose logs

# Перегляд логів конкретного сервісу
docker compose logs backend
docker compose logs frontend
docker compose logs postgres
docker compose logs redis
docker compose logs celery-worker

# Слідкування за логами в реальному часі
docker compose logs -f
```

**Здорові логи:**
- ✅ Немає критичних помилок (ERROR, CRITICAL)
- ✅ Backend successfully connected to database
- ✅ Redis connection established
- ✅ Frontend compiled successfully

---

## 🌐 Перевірка Production Розгортання (Vercel)

### 1. GitHub Actions

1. Перейдіть до [GitHub Actions](https://github.com/Ihorog/cimeika-unified/actions)
2. Знайдіть workflow "Vercel Deployment"
3. Перевірте останній run

**Здоровий статус:**
- ✅ All steps completed successfully
- ✅ Deploy to Vercel - Success
- ✅ No errors in logs

### 2. Vercel Dashboard

1. Відкрийте [Vercel Dashboard](https://vercel.com/dashboard)
2. Виберіть проєкт CIMEIKA
3. Перевірте статус останнього deployment

**Здоровий deployment:**
- ✅ Status: Ready
- ✅ Build completed without errors
- ✅ All checks passed

### 3. Production URL

Перевірте live deployment:

```bash
# Замініть URL на ваш Vercel URL
curl https://your-cimeika-app.vercel.app
```

**Або відкрийте у браузері:**
```
https://your-cimeika-app.vercel.app
```

**Очікуваний результат:**
- ✅ Сторінка завантажується швидко
- ✅ Відображається весь контент
- ✅ Навігація працює
- ✅ Немає помилок у консолі

---

## 🐛 Troubleshooting

### Backend не відповідає

**Симптоми:**
- `curl: (7) Failed to connect`
- `Connection refused`

**Рішення:**

1. Перевірте, чи запущений контейнер:
   ```bash
   docker compose ps backend
   ```

2. Перевірте логи:
   ```bash
   docker compose logs backend
   ```

3. Перезапустіть backend:
   ```bash
   docker compose restart backend
   ```

### Frontend не завантажується

**Симптоми:**
- Пуста сторінка
- ERR_CONNECTION_REFUSED

**Рішення:**

1. Перевірте статус контейнера:
   ```bash
   docker compose ps frontend
   ```

2. Перевірте логи:
   ```bash
   docker compose logs frontend
   ```

3. Перевірте, чи компіляція успішна:
   ```bash
   docker compose exec frontend npm run build
   ```

### Database Connection Failed

**Симптоми:**
- Backend логи: `could not connect to server`
- `FATAL: password authentication failed`

**Рішення:**

1. Перевірте PostgreSQL контейнер:
   ```bash
   docker compose ps postgres
   ```

2. Перевірте credentials у `.env`:
   ```env
   POSTGRES_USER=cimeika_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=cimeika
   ```

3. Перезапустіть PostgreSQL:
   ```bash
   docker compose restart postgres
   ```

### Redis Connection Failed

**Симптоми:**
- Backend логи: `Error connecting to Redis`
- Celery не запускається

**Рішення:**

1. Перевірте Redis контейнер:
   ```bash
   docker compose ps redis
   ```

2. Перевірте підключення:
   ```bash
   docker compose exec redis redis-cli -a your_password ping
   ```

3. Перезапустіть Redis:
   ```bash
   docker compose restart redis
   ```

### Vercel Deployment Failed

**Симптоми:**
- GitHub Actions показує помилку
- Build failed in Vercel

**Рішення:**

1. Перевірте логи у GitHub Actions:
   - Відкрийте failed run
   - Перегляньте детальні логи кожного step

2. Перевірте Vercel Environment Variables:
   - `VITE_API_URL` має бути встановлено
   - Всі required змінні налаштовані

3. Перевірте локальну збірку:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

4. Перевірте GitHub Secrets:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`

---

## 📊 Чеклист Перевірки

### Локальне Розгортання

- [ ] Docker встановлено та запущено
- [ ] `.env` файл створено та налаштовано
- [ ] `docker compose up -d` виконано успішно
- [ ] Всі 5 контейнерів у статусі "running"
- [ ] Backend health check повертає 200 OK
- [ ] Backend API endpoints доступні
- [ ] Frontend homepage завантажується
- [ ] Всі маршрути модулів працюють
- [ ] Немає критичних помилок у логах

### Production Розгортання (Vercel)

- [ ] GitHub репозиторій підключено до Vercel
- [ ] GitHub Secrets налаштовано
- [ ] Vercel Environment Variables налаштовано
- [ ] GitHub Actions workflow виконується успішно
- [ ] Vercel deployment статус: Ready
- [ ] Production URL доступний
- [ ] Frontend працює коректно
- [ ] Backend API доступний та працює

---

## 🔗 Додаткові Ресурси

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Vercel Deployment Guide](./VERCEL_DEPLOYMENT.md)
- [GitHub Actions Setup](./GITHUB_ACTIONS_VERCEL.md)
- [Troubleshooting Guide](./README.md#troubleshooting)

---

## 📞 Підтримка

Якщо виникають проблеми:

1. Запустіть автоматичну перевірку: `./scripts/verify-deployment.sh`
2. Перегляньте логи: `docker compose logs`
3. Перевірте документацію у папці `docs/`
4. Створіть issue на GitHub з деталями проблеми

---

**Версія:** 1.0.0  
**Останнє оновлення:** Грудень 2024  
**Статус:** Активний
