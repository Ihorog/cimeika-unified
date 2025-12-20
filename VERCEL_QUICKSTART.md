# 🚀 Швидке розгортання на Vercel

## Автоматичне розгортання (GitHub Actions):

Проєкт вже налаштовано для CI/CD! Просто налаштуйте секрети:

➡️ [docs/GITHUB_ACTIONS_VERCEL.md](docs/GITHUB_ACTIONS_VERCEL.md)

## Один клік (Vercel Dashboard):
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Ihorog/cimeika-unified)

## Або через CLI:

```bash
npm install -g vercel
vercel
```

## Необхідні змінні середовища:

```
VITE_API_URL=https://your-backend-url.com
VITE_APP_NAME=CIMEIKA
```

## Детальна документація:

➡️ [docs/VERCEL_DEPLOYMENT.md](docs/VERCEL_DEPLOYMENT.md)

---

**Увага**: Не забудьте встановити змінні середовища у Vercel Dashboard перед deployment!
