# CIMEIKA Frontend

React + Vite frontend для CIMEIKA екосистеми.

## Структура

```
frontend/
├── src/
│   ├── modules/        # 7 модулів CIMEIKA
│   ├── shared/         # Спільні компоненти
│   ├── layouts/        # Layout шаблони
│   ├── App.jsx         # Головний компонент
│   ├── main.jsx        # Точка входу
│   └── index.css       # Глобальні стилі
├── index.html          # HTML шаблон
├── package.json        # npm залежності
├── vite.config.js      # Vite конфігурація
└── Dockerfile         # Docker конфігурація
```

## Розробка

### Локальний запуск

1. Встановіть залежності:
   ```bash
   npm install
   ```

2. Запустіть dev server:
   ```bash
   npm run dev
   ```

Frontend буде доступний на http://localhost:3000 (або http://localhost:5173 для локальної розробки)

### Скрипти

- `npm run dev` - Запуск development server
- `npm run build` - Збірка для production
- `npm run preview` - Попередній перегляд production збірки
- `npm run lint` - Перевірка коду

## Технології

- **React 18** - UI бібліотека
- **Vite** - Build tool
- **Zustand** - State management
- **Axios** - HTTP клієнт
- **react-i18next** - Інтернаціоналізація
- **Tailwind CSS** - CSS framework (планується)

## 7 Модулів

1. **Ci** - Центральне ядро
2. **Казкар** - Пам'ять
3. **Подія** - Події
4. **Настрій** - Емоції
5. **Маля** - Ідеї
6. **Галерея** - Медіа
7. **Календар** - Час
