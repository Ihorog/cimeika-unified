---
source: Ihorog/cimeika
archived: 2026-02-04
reason: System consolidation
---

ТЗ на оптимізацію Cimeika
=========================

(кожен аспект цього ТЗ ти вправі змінювати на власний розсуд. Реалізуй свій досвід у сучасній розробці інтерактивного якісного ші контенту)

1. Вхідні ресурси
-----------------

API:

Base URL: https://ihorog-cimeika-api.hf.space

Endpoints (обов'язкові до підтримки):

GET /health

POST /story/scene

GET /gallery/feed

POST /weights/recompute

POST /events/notify

POST /telemetry

GitHub репозиторії:

Фронтенд: cimeika-real-time-data-app

Бекенд/ядро: cimeika

README_quickstart.md — інструкції з локального запуску та деплою.
cimeika.config.yaml — централізовані налаштування API, ключів та режимів.

Secrets (HF Variables):

OPENAI_KEY_CI

OPENWEATHER_KEY

TELEGRAM_BOT_KEY

GITHUB_KEY

ENV=staging|prod

---

2. Завдання фронтенду
---------------------

1. Зібрати сучасний React/Vite/Tailwind застосунок (src/ui/).
2. Оптимізувати бандл ≤2.5 MB.
3. Додати Framer Motion анімації: переходи між сценами ≥60 FPS.
4. Реалізувати галерею плиток (src/ui/gallery/):
   - Lazy-load
   - Сортування за weight (мінімум 1.20)
   - Відкриття зображень у мобільному форматі
5. Інтегрувати Service Worker для кешування аудіо-лупів.
6. Забезпечити WCAG AA (контраст ≥4.5:1, субтитри, ARIA).

---

3. Завдання бекенду
-------------------

1. Впорядкувати app/routes/ — окремі контролери для story, gallery, weights, events, telemetry.
2. Додати щоденний пайплайн:
   - refresh даних
   - recompute ваг (≥1.20)
   - boost позитивних аномалій (bias +1, cap 2.0)
   - оновлення /gallery/feed
3. Логувати всі запити у JSON форматі.
4. Налаштувати /events/notify → Telegram & Email.
5. Перевірити /health (200 OK ≥5 хв стабільно).

---

4. CI/CD
--------

Використати GitHub Actions (.github/workflows/deploy.yml):

- Лінтинг (eslint, prettier)
- Тести (jest, playwright)
- Деплой у Hugging Face Space (див. README_quickstart.md)

Звіт по QA: Lighthouse + мобільна перевірка FPS, контрасту, payload (шаблон `mobile-QA-report.md`).

---

5. Acceptance Criteria
----------------------

- Перший екран завантажується ≤2.5 MB.
- Перехід між сценами 60 FPS.
- Аудіо-луп кешується, не рефетчиться.
- Контраст ≥4.5:1, субтитри відображаються.
- Усі weight в галереї ≥1.20.
- Recompute/boost виконується без помилок.
- Алерти приходять у Telegram ≤3 с.

---

6. Вихідні артефакти
--------------------

- README_quickstart.md — запуск локально й деплой.
- cimeika.config.yaml — єдиний конфіг сервісу.
- mobile-QA-report.md — результати тестів.
- Робочий HF Space з деплоєм (посилання у PR).

---

📌 Це формулювання вже підходить як інструкція для команди розробки — вони бачать де код, що робити, які критерії.
