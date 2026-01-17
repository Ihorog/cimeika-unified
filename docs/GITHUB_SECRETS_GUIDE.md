# GitHub Secrets Setup - Quick Guide

## Як додати OPENAI_API_KEY в GitHub Secrets

### Крок 1: Отримання OpenAI API ключа

1. Відкрийте https://platform.openai.com/api-keys
2. Натисніть **"Create new secret key"**
3. Скопіюйте ключ (він виглядає як `YOUR_OPENAI_API_KEY`)
4. ⚠️ Зберігайте його в безпечному місці!

### Крок 2: Додавання секрету в GitHub

1. Перейдіть до репозиторію: **https://github.com/Ihorog/cimeika-unified**

2. Натисніть **Settings** (⚙️ Налаштування) у верхньому меню

3. В лівій панелі знайдіть секцію **Security**

4. Натисніть **Secrets and variables** → **Actions**

5. Натисніть зелену кнопку **"New repository secret"**

6. Заповніть форму:
   ```
   Name: OPENAI_API_KEY
   Secret: YOUR_OPENAI_API_KEY
   ```

7. Натисніть **"Add secret"**

### Крок 3: Перевірка

Секрет додано! Тепер:
- ✅ GitHub Actions зможуть використовувати OpenAI
- ✅ Деплоймент працюватиме з GPT функціями
- ✅ Ключ захищений і не видимий в логах

### Використання в GitHub Actions

Якщо потрібно додати в workflow (`.github/workflows/*.yml`):

```yaml
name: Deploy Backend

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy with OpenAI
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          # Ваш код деплойменту
          echo "OpenAI key is configured"
```

### Важливо! 🔒

- ❌ **НІКОЛИ** не публікуйте ключ в коді
- ❌ **НЕ** додавайте `.env` файл в Git
- ✅ Використовуйте секрети для всіх чутливих даних
- ✅ Регулярно оновлюйте ключі

---

## Інші секрети які можуть знадобитись

Для повноцінної роботи також додайте:

| Секрет | Призначення |
|--------|-------------|
| `OPENAI_API_KEY` | OpenAI GPT інтеграція |
| `POSTGRES_PASSWORD` | База даних |
| `REDIS_PASSWORD` | Redis кеш |
| `SECRET_KEY` | Flask сесії |

Всі ці секрети додаються аналогічно (Steps 1-7 вище).

---

**Потрібна допомога?**
- 📖 Детальніше: [`OPENAI_SETUP.md`](OPENAI_SETUP.md)
- 🐛 Issues: https://github.com/Ihorog/cimeika-unified/issues
