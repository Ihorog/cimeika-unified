# CIMEIKA Deployment Testing Examples

Цей документ містить приклади команд та очікувані результати для тестування розгортання.

## 📋 Швидке тестування

### 1. Автоматична перевірка (найпростіший спосіб)

```bash
# З кореня проєкту
./scripts/verify-deployment.sh
```

**Очікуваний вивід при успішному розгортанні:**

```
=========================================
  CIMEIKA Deployment Verification
=========================================

[1/6] Checking prerequisites...

✅ curl is installed
✅ jq is installed

[2/6] Checking Docker Compose services...

Checking Docker container cimeika-postgres... ✅ Running
Checking Docker container cimeika-redis... ✅ Running
Checking Docker container cimeika-backend... ✅ Running
Checking Docker container cimeika-frontend... ✅ Running
Checking Docker container cimeika-celery-worker... ✅ Running

[3/6] Checking Backend API...

Checking Backend root endpoint... ✅ OK (HTTP 200)
Checking Backend health endpoint... ✅ OK (HTTP 200)
Checking Modules API... ✅ OK (modules: [...])

[4/6] Checking Frontend...

Checking Frontend homepage... ✅ OK (HTTP 200)
Checking Frontend health page... ✅ OK (HTTP 200)

[5/6] Checking configuration files...

Checking docker-compose.yml... ✅ Found
Checking vercel.json... ✅ Found
Checking .env file... ✅ Found
Checking GitHub Actions workflow... ✅ Found

[6/6] Deployment Summary

===========================================
Backend Health:    ✅ HEALTHY (3/3 checks passed)
Frontend Health:   ✅ HEALTHY (2/2 checks passed)
===========================================

✅ Deployment verification PASSED

Your CIMEIKA ecosystem is running correctly!

Access points:
  • Frontend:  http://localhost:3000
  • Backend:   http://localhost:5000
  • Health UI: http://localhost:3000/health
  • API Docs:  http://localhost:5000/api/v1/modules
```

---

## 🔍 Покрокове ручне тестування

### Крок 1: Перевірка Docker контейнерів

```bash
docker compose ps
```

**Очікуваний результат:**
```
NAME                      IMAGE                       STATUS
cimeika-backend           cimeika-unified-backend     Up X minutes
cimeika-celery-worker     cimeika-unified-backend     Up X minutes
cimeika-frontend          cimeika-unified-frontend    Up X minutes
cimeika-postgres          postgres:15-alpine          Up X minutes (healthy)
cimeika-redis             redis:7-alpine              Up X minutes (healthy)
```

---

### Крок 2: Тестування Backend

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
  "modules": [
    "Ci - Центральне ядро",
    "Казкар - Пам'ять",
    "Подія - Події",
    "Настрій - Емоції",
    "Маля - Ідеї",
    "Галерея - Медіа",
    "Календар - Час"
  ]
}
```

#### 2.3 Modules API

```bash
curl http://localhost:5000/api/v1/modules | jq
```

**Очікувана відповідь (фрагмент):**
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
    {
      "id": "kazkar",
      "name": "Казкар",
      "description": "Пам'ять, історії, легенди",
      "status": "in_development"
    }
    // ... та інші 5 модулів
  ]
}
```

**Перевірка кількості модулів:**
```bash
curl -s http://localhost:5000/api/v1/modules | jq '.modules | length'
# Має вивести: 7
```

---

### Крок 3: Тестування Frontend

#### 3.1 Homepage

```bash
curl -I http://localhost:3000
```

**Очікувана відповідь:**
```
HTTP/1.1 200 OK
Content-Type: text/html
...
```

#### 3.2 Health Check UI

**Через curl:**
```bash
curl -s http://localhost:3000/health | grep -o "CIMEIKA" | head -1
# Має вивести: CIMEIKA
```

**Через браузер:**
1. Відкрийте: http://localhost:3000/health
2. Перевірте:
   - ✅ Загальний статус: HEALTHY
   - ✅ Frontend Status: healthy
   - ✅ Backend Status: healthy
   - ✅ Modules Status: success
   - ✅ Список з 7 модулів відображається

---

### Крок 4: Тестування логів

#### 4.1 Backend логи

```bash
docker compose logs backend --tail=20
```

**Здорові ознаки:**
- Немає ERROR або CRITICAL
- `* Running on http://0.0.0.0:5000`
- Відповіді на запити: `200 OK`

#### 4.2 Frontend логи

```bash
docker compose logs frontend --tail=20
```

**Здорові ознаки:**
- `VITE ... ready in ... ms`
- `Local: http://localhost:3000/`
- Немає помилок компіляції

#### 4.3 PostgreSQL логи

```bash
docker compose logs postgres --tail=10
```

**Здорові ознаки:**
- `database system is ready to accept connections`
- Немає критичних помилок

#### 4.4 Redis логі

```bash
docker compose logs redis --tail=10
```

**Здорові ознаки:**
- `Ready to accept connections`
- Немає помилок з'єднання

---

## 🌐 Тестування Production (Vercel)

### Перевірка GitHub Actions

```bash
# Або відвідайте: https://github.com/Ihorog/cimeika-unified/actions
gh run list --workflow="Vercel Deployment" --limit 5
```

**Очікувані результати:**
- Останній run має статус: ✅ completed
- Жоден step не failed

### Перевірка Vercel Deployment

**Через curl:**
```bash
# Замініть URL на ваш
curl -I https://your-cimeika-app.vercel.app
```

**Очікувана відповідь:**
```
HTTP/2 200
content-type: text/html
x-vercel-id: ...
```

**Перевірка Health UI:**
```bash
curl -s https://your-cimeika-app.vercel.app/health | grep -o "CIMEIKA"
```

---

## 🐛 Приклади діагностики проблем

### Проблема: Backend не відповідає

**Діагностика:**

```bash
# 1. Перевірити статус контейнера
docker compose ps backend

# 2. Перевірити логи
docker compose logs backend --tail=50

# 3. Перевірити порт
netstat -tlnp | grep 5000

# 4. Перевірити підключення до БД
docker compose exec backend python -c "
import psycopg2
conn = psycopg2.connect(
    host='postgres',
    database='cimeika',
    user='cimeika_user',
    password='your_password'
)
print('Database connection: OK')
"
```

**Очікуваний результат:**
```
Database connection: OK
```

### Проблема: Frontend не завантажується

**Діагностика:**

```bash
# 1. Перевірити статус
docker compose ps frontend

# 2. Перевірити логи
docker compose logs frontend --tail=50

# 3. Перевірити порт
netstat -tlnp | grep 3000

# 4. Тест компіляції
docker compose exec frontend npm run build
```

**Очікуваний результат білда:**
```
vite v5.x.x building for production...
✓ X modules transformed.
dist/index.html  X.XX kB
...
✓ built in XXXms
```

### Проблема: Database connection failed

**Діагностика:**

```bash
# 1. Перевірити PostgreSQL
docker compose exec postgres pg_isready -U cimeika_user

# 2. Перевірити підключення
docker compose exec postgres psql -U cimeika_user -d cimeika -c "SELECT version();"

# 3. Перевірити credentials
docker compose exec backend printenv | grep POSTGRES
```

**Очікувані результати:**
```bash
# pg_isready:
/var/run/postgresql:5432 - accepting connections

# psql:
PostgreSQL 15.x on ...

# printenv:
POSTGRES_HOST=postgres
POSTGRES_USER=cimeika_user
POSTGRES_DB=cimeika
```

### Проблема: Redis connection failed

**Діагностика:**

```bash
# 1. Перевірити Redis
docker compose exec redis redis-cli -a your_password ping

# 2. Перевірити підключення
docker compose exec redis redis-cli -a your_password INFO server

# 3. Тест з backend
docker compose exec backend python -c "
import redis
r = redis.Redis(host='redis', port=6379, password='your_password')
print(r.ping())
"
```

**Очікувані результати:**
```bash
# ping:
PONG

# INFO:
# Server
redis_version:7.x.x
...

# Python test:
True
```

---

## 📊 Benchmark тести (опціонально)

### Backend Response Time

```bash
# Тест часу відповіді
time curl -s http://localhost:5000/health > /dev/null

# Множинні запити
for i in {1..10}; do
  time curl -s http://localhost:5000/api/v1/modules > /dev/null
done
```

**Очікуваний час відповіді:**
- Health endpoint: < 100ms
- Modules API: < 200ms

### Frontend Load Time

```bash
# Використовуючи curl
time curl -s http://localhost:3000 > /dev/null

# Або за допомогою wget
wget --spider --server-response http://localhost:3000 2>&1 | grep "HTTP/"
```

**Очікуваний час:**
- Initial load: < 500ms
- Subsequent loads (cached): < 100ms

---

## ✅ Контрольний список (Checklist)

Використовуйте цей список для швидкої перевірки:

### Локальне розгортання

```bash
# Базові перевірки
✓ docker compose ps                           # Всі контейнери Up
✓ curl http://localhost:5000/health           # 200 OK
✓ curl http://localhost:3000                  # 200 OK
✓ curl http://localhost:3000/health           # 200 OK

# Детальні перевірки
✓ curl http://localhost:5000/api/v1/modules   # 7 модулів
✓ docker compose logs backend --tail=20       # Немає ERROR
✓ docker compose logs frontend --tail=20      # Немає помилок
✓ docker compose exec postgres pg_isready    # accepting connections
✓ docker compose exec redis redis-cli ping   # PONG
```

### Production (Vercel)

```bash
# GitHub Actions
✓ gh run list --workflow="Vercel Deployment"  # ✅ completed

# Vercel
✓ curl -I https://your-app.vercel.app         # HTTP/2 200
✓ curl https://your-app.vercel.app/health     # CIMEIKA visible
```

---

## 🔗 Корисні ресурси

- [Повна документація](./DEPLOYMENT_VERIFICATION.md)
- [Швидкий довідник](../DEPLOYMENT_QUICKREF.md)
- [Docker Documentation](https://docs.docker.com/)
- [Vercel Documentation](https://vercel.com/docs)

---

**Версія:** 1.0.0  
**Останнє оновлення:** Грудень 2024
