---
source: Ihorog/cimeika
archived: 2026-02-04
reason: System consolidation
---

# Швидкий старт

## Локальний запуск

### Frontend (Next.js)
1. Встановіть залежності:
   ```sh
   npm install
   ```
2. Запустіть dev-сервер:
   ```sh
   npm run dev
   ```
   Інтерфейс буде доступний на `http://localhost:8000`.

### Backend (Uvicorn)
1. Встановіть Python-залежності:
   ```sh
   pip install -r requirements.txt
   ```
2. Запустіть сервер:
   ```sh
   uvicorn app:app --reload --port 8001
   ```
   API буде доступне на `http://localhost:8001`.

## Деплой до Hugging Face Space
1. Підготуйте `.env` із потрібними ключами (див. `README.md`).
2. Використайте скрипт для деплою:
   ```sh
   bash push_to_hf.sh
   ```
   або вручну створіть Space і надішліть останній коміт:
   ```sh
   huggingface-cli repo create your-user/cimeika --type space
   git remote add space https://huggingface.co/spaces/your-user/cimeika
   git push space main
   ```
3. Перевірте розгортання у вашому Space.
