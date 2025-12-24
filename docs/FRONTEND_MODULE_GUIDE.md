# Frontend Module Development Guide

## Створено: 2024-12-24
## Статус: Активний розвиток (4/7 модулів готові)

---

## Структура проєкту

### Frontend Modules Pattern
Кожен модуль має **однакову архітектуру**:

```
frontend/src/modules/{module}/
  └── {Module}View.jsx    # Головний компонент модуля
```

### API Services
Всі API сервіси знаходяться в:
```
frontend/src/services/modules/
  ├── ciService.ts         # Ci API
  ├── kazkarService.ts     # Kazkar API
  ├── podijaService.ts     # Podija API
  ├── nastrijService.ts    # Nastrij API
  ├── malyaService.ts      # Malya API
  ├── calendarService.ts   # Calendar API
  ├── galleryService.ts    # Gallery API
  └── index.ts            # Експорт всіх сервісів
```

---

## Готові модулі (4/7)

### 1. Ci View ✅
**Статус:** Повністю функціональний

**Функції:**
- `ci.capture()` - Головна точка входу з текстовим вводом
- Аналіз та класифікація вводу (емоції, наміри, теги)
- Навігаційна сітка для всіх 7 модулів
- Інформаційні секції з принципами Ci

**Особливості:**
- Hero секція з градієнтом
- Response grid для відображення результатів аналізу
- Responsive дизайн

---

### 2. Kazkar View ✅
**Статус:** Повністю функціональний

**Функції:**
- **CREATE**: Форма для створення історій з полями:
  - Назва, зміст
  - Тип історії (спогад, легенда, історія, подія)
  - Місце, учасники, теги
- **READ**: Сітка карток з історіями
- **Статистика**: Кількість історій по типах
- **Filtering**: По типу історії

**API Endpoints:**
- `GET /api/v1/kazkar/stories` - Список
- `POST /api/v1/kazkar/stories` - Створення
- `GET /api/v1/kazkar/stats` - Статистика

---

### 3. Podija View ✅
**Статус:** Повністю функціональний

**Функції:**
- **CREATE**: Форма для подій з полями:
  - Назва, опис
  - Дата події (datetime)
  - Тип події (особиста, робота, сім'я, свято, зустріч)
  - Теги
- **READ**: Список подій
- **UPDATE**: Відмітка завершення події (checkbox)
- **Filtering**: Всі / Майбутні / Завершені

**API Endpoints:**
- `GET /api/v1/podija/events` - Список
- `POST /api/v1/podija/events` - Створення
- `PUT /api/v1/podija/events/{id}` - Оновлення

---

### 4. Malya View ✅
**Статус:** Повністю функціональний

**Функції:**
- **CREATE**: Форма для ідей з полями:
  - Назва, опис
  - Тип ідеї (особиста, проєкт, бізнес, творча, покращення, винахід)
  - Статус (активна, в процесі, реалізована, архівна)
  - Теги
- **READ**: Сітка карток з іконками 💡
- **Filtering**: За статусом (всі, активні, архівні)

**Стилізація:**
- Кольорові статус-бейджі (зелений/помаранчевий/синій/сірий)
- Hover effects з підняттям картки

**API Endpoints:**
- `GET /api/v1/malya/ideas` - Список
- `POST /api/v1/malya/ideas` - Створення

---

## Модулі в розробці (3/7)

### 5. Nastrij View ⚪
**Потрібно:** CRUD для емоційних станів

**Рекомендовані поля:**
- Назва, опис
- Емоційний стан (радість, сум, тривога, спокій)
- Інтенсивність (1-10)
- Тригери (масив текстів)
- Теги

**API:**
```typescript
nastrijService.createEmotion()
nastrijService.getEmotions()
```

---

### 6. Calendar View ⚪
**Потрібно:** CRUD для календарних записів

**Рекомендовані поля:**
- Назва, опис
- Дата/час події
- Повторення (так/ні)
- Патерн повторення (щодня, щотижня, щомісяця)
- Теги

**API:**
```typescript
calendarService.createEntry()
calendarService.getEntries()
calendarService.getTodayEntries()
```

---

### 7. Gallery View ⚪
**Потрібно:** CRUD для медіа файлів

**Рекомендовані поля:**
- Назва, опис
- Тип медіа (фото, відео, аудіо)
- URL файлу
- Thumbnail URL
- Metadata (JSON)
- Теги

**API:**
```typescript
galleryService.createItem()
galleryService.getItems()
galleryService.getItemsByType()
```

---

## Стилі та UI Components

### Готові CSS класи

**Buttons:**
```css
.btn-primary       /* Основна кнопка (синя) */
.btn-secondary     /* Другорядна кнопка (прозора з рамкою) */
.btn-large         /* Велика кнопка */
```

**Forms:**
```css
.story-form / .event-form / .idea-form  /* Форми для створення */
.form-group        /* Група полів */
.form-row          /* Ряд з двома полями */
```

**Cards:**
```css
.story-card        /* Картка історії (Kazkar) */
.event-card        /* Картка події (Podija) */
.idea-card         /* Картка ідеї (Malya) */
```

**Filters:**
```css
.filter-buttons    /* Контейнер фільтрів */
.filter-btn        /* Неактивний фільтр */
.filter-active     /* Активний фільтр */
```

**States:**
```css
.loading-state     /* Стан завантаження */
.empty-state       /* Порожній стан */
.error-banner      /* Банер помилки */
```

**Badges & Tags:**
```css
.badge             /* Основний бейдж (синій) */
.stat-badge        /* Статистичний бейдж */
.status-badge      /* Бейдж статусу */
.tag               /* Тег */
```

---

## Pattern для створення нового модуля

### 1. Підключити service
```jsx
import { moduleService } from '../../services/modules';
```

### 2. State management
```jsx
const [items, setItems] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
const [showForm, setShowForm] = useState(false);
const [newItem, setNewItem] = useState({ /* initial values */ });
```

### 3. Load data on mount
```jsx
useEffect(() => {
  loadData();
}, []);

const loadData = async () => {
  setLoading(true);
  setError(null);
  try {
    const data = await moduleService.getItems();
    setItems(data);
  } catch (err) {
    setError('Помилка завантаження');
  } finally {
    setLoading(false);
  }
};
```

### 4. Form submission
```jsx
const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    await moduleService.createItem(newItem);
    setNewItem({ /* reset */ });
    setShowForm(false);
    loadData();
  } catch (err) {
    setError('Помилка створення');
  }
};
```

### 5. JSX Structure
```jsx
return (
  <div className="module-view {module}-view">
    <header className="module-header">
      <h1>Назва</h1>
      <p className="module-subtitle">Опис</p>
    </header>
    
    <main className="module-content">
      {/* Error banner */}
      {/* Actions + Filters */}
      {/* Form (conditional) */}
      {/* Loading / Empty / Items list */}
    </main>
  </div>
);
```

---

## API Patterns

### Всі сервіси мають стандартні методи:

```typescript
// Status
await service.getStatus()

// CRUD
await service.create{Entity}(data)
await service.get{Entities}(params?)
await service.get{Entity}(id)
await service.update{Entity}(id, updates)
await service.delete{Entity}(id)
```

### Response handling
```jsx
try {
  const result = await service.method();
  // Success
} catch (err) {
  // Error - може бути:
  // - err.response?.data?.detail (FastAPI error)
  // - err.message (Network error)
  // - 'Backend offline' (no connection)
}
```

---

## Запуск та тестування

### Локальна розробка

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
# або
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
# http://localhost:3000 або 5173
```

**Docker Compose (Full Stack):**
```bash
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs
```

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Create story
curl -X POST http://localhost:8000/api/v1/kazkar/stories \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Content"}'
```

---

## Важливі нотатки

### Теми (Themes)
Система має **детерміновану** тематизацію:
- Kazkar → `night` (темна тема)
- Інші модулі → `day` (світла тема)

Керується через `ThemeManager.jsx` на основі роутінгу.

### Backend port
Backend працює на порті **8000** (не 5000!)
```
VITE_API_URL=http://localhost:8000
```

### Ci Overlay
Глобальний FAB (Floating Action Button) завжди доступний:
- Правий нижній кут
- Відкриває drawer з Ci capture
- Інтегрований з ciService

---

## Контрольний список для нового модуля

- [ ] Створити `{Module}View.jsx`
- [ ] Імпортувати відповідний service
- [ ] Додати state management (items, loading, error, form)
- [ ] Реалізувати loadData()
- [ ] Створити форму з необхідними полями
- [ ] Додати handleSubmit()
- [ ] Зробити список/сітку items
- [ ] Додати фільтрацію (якщо потрібно)
- [ ] Стилізувати використовуючи готові CSS класи
- [ ] Тестувати CRUD операції
- [ ] Перевірити responsive design

---

**Створено командою Cimeika Development** 🚀
**Версія:** 0.1.0 (Beta)
