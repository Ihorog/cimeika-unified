# OpenAI Integration Setup Guide

## Налаштування OpenAI API для Cimeika

### 1. Отримання API ключа

1. Перейдіть на https://platform.openai.com/api-keys
2. Увійдіть або зареєструйтесь
3. Натисніть "Create new secret key"
4. Скопіюйте згенерований ключ (він показується лише один раз!)

### 2. Локальна розробка

#### Для локального запуску:

1. Створіть файл `.env` в корені проекту:
```bash
cp .env.template .env
```

2. Відкрийте `.env` та додайте ваш ключ:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

3. Запустіть бекенд:
```bash
cd backend
python main.py
```

### 3. GitHub Repository Secrets (для CI/CD)

#### Додавання секрету в GitHub:

1. Перейдіть до вашого репозиторію на GitHub
2. Натисніть **Settings** (Налаштування)
3. В лівому меню виберіть **Secrets and variables** → **Actions**
4. Натисніть **New repository secret**
5. Введіть:
   - **Name**: `OPENAI_API_KEY`
   - **Secret**: ваш OpenAI API ключ
6. Натисніть **Add secret**

#### Використання в GitHub Actions:

Якщо у вас є workflow файл (`.github/workflows/*.yml`), додайте:

```yaml
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

Або передайте як змінну середовища:

```yaml
- name: Run Backend Tests
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    cd backend
    python -m pytest
```

### 4. Vercel Deployment (якщо використовується)

1. Перейдіть до Vercel Dashboard
2. Виберіть ваш проект
3. Перейдіть до **Settings** → **Environment Variables**
4. Додайте:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: ваш OpenAI API ключ
   - **Environments**: Production, Preview, Development (за потребою)
5. Натисніть **Save**

### 5. Docker (якщо використовується)

При запуску Docker контейнера передайте змінну:

```bash
docker run -e OPENAI_API_KEY=your-key-here your-image-name
```

Або через docker-compose.yml:

```yaml
services:
  backend:
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

### 6. Перевірка роботи

Після налаштування перевірте чи працює інтеграція:

1. Запустіть бекенд
2. Відкрийте фронтенд
3. Перейдіть до `/chat`
4. Надішліть повідомлення
5. Ви повинні отримати відповідь від GPT

### Безпека

⚠️ **ВАЖЛИВО:**

- ❌ **НІКОЛИ** не комітьте файл `.env` в Git
- ❌ **НІКОЛИ** не публікуйте API ключ в коді
- ✅ `.env` вже додано в `.gitignore`
- ✅ Використовуйте GitHub Secrets для CI/CD
- ✅ Регулярно ротуйте ключі
- ✅ Встановіть ліміти використання в OpenAI Dashboard

### Troubleshooting

**Проблема**: Chat не відповідає

**Рішення**:
1. Перевірте чи додано `OPENAI_API_KEY` в `.env`
2. Перезапустіть бекенд
3. Перевірте логи бекенда на помилки
4. Переконайтеся що ключ дійсний (не протермінований)
5. Перевірте що у вас є кредити на OpenAI аккаунті

**Проблема**: GitHub Actions падає

**Рішення**:
1. Переконайтесь що секрет `OPENAI_API_KEY` додано в Settings → Secrets
2. Перевірте чи правильно використовується в workflow файлі
3. Перевірте логи GitHub Actions

### Додаткові ресурси

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

---

**Статус**: Інтеграція OpenAI GPT-3.5-turbo активна ✅

**Версія**: 1.0.0
