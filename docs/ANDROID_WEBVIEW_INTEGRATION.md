# Android WebView Voice Integration Guide

## Огляд

Цей документ описує інтеграцію Android WebView з голосовими можливостями (Push-to-Talk), TextToSpeech і системним overlay для Cimeika Unified.

## Архітектура

```
┌─────────────────────────────────────────────────┐
│         Android App (WebView)                    │
├─────────────────────────────────────────────────┤
│                                                   │
│  MainActivity.kt                                  │
│  ├─ WebView (Vercel UI)                         │
│  ├─ TextToSpeech (Ukrainian/English)            │
│  ├─ SpeechRecognizer (Ukrainian)                │
│  └─ JavaScript Bridge (Android)                  │
│      ├─ startVoice()                             │
│      ├─ speak(text)                              │
│      ├─ enableOverlay()                          │
│      └─ disableOverlay()                         │
│                                                   │
│  OverlayService.kt                               │
│  └─ Floating Ci Button                          │
│      ├─ Tap → Open App                          │
│      ├─ Long-press → Move Mode                  │
│      └─ Swipe → Dismiss                         │
│                                                   │
└─────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────┐
│      React Frontend (Vercel)                     │
├─────────────────────────────────────────────────┤
│                                                   │
│  window.onVoiceText = (text) => {...}           │
│  └─ Receives voice text from Android            │
│                                                   │
│  window.Android?.speak(text)                     │
│  └─ Triggers TTS in Android                     │
│                                                   │
│  useVoiceIntegration() Hook                      │
│  └─ Manages Android integration                 │
│                                                   │
└─────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────┐
│      FastAPI Backend                             │
├─────────────────────────────────────────────────┤
│                                                   │
│  POST /api/ci/chat                               │
│  └─ OpenAI GPT Integration                      │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Компоненти

### 1. Android (Kotlin)

#### MainActivity.kt
- **WebView**: Відкриває https://cimeika-unified.vercel.app/
- **TextToSpeech**: Озвучує відповіді чату (українська/англійська)
- **SpeechRecognizer**: Розпізнає голос користувача (українська)
- **JavaScript Bridge**: Інтерфейс між WebView і нативним кодом

**Методи JavaScript Bridge:**
```kotlin
// Розпочати голосове розпізнавання
window.Android.startVoice()

// Озвучити текст через TTS
window.Android.speak("Привіт від Ci!")

// Увімкнути системний overlay
window.Android.enableOverlay()

// Вимкнути overlay
window.Android.disableOverlay()
```

#### OverlayService.kt
- **Floating Button**: Системна плаваюча кнопка з логотипом Ci
- **Gestures**:
  - **Tap**: Відкриває MainActivity
  - **Long-press**: Увімкнює режим переміщення
  - **Swipe** (down/away): Закриває overlay

**Дозволи:**
- `INTERNET` - доступ до Vercel
- `RECORD_AUDIO` - голосове розпізнавання
- `SYSTEM_ALERT_WINDOW` - overlay button

### 2. Frontend (React + TypeScript)

#### useVoiceIntegration.ts Hook
Хук для інтеграції з Android WebView:

```typescript
import { useVoiceIntegration } from '../hooks/useVoiceIntegration';

const { isAndroid, startVoice, speak, enableOverlay, disableOverlay } = useVoiceIntegration({
  onVoiceText: (text) => {
    // Обробити текст з голосу
    console.log('Voice input:', text);
  },
  onError: (error) => {
    // Обробити помилку
    console.error('Voice error:', error);
  }
});
```

#### Chat.jsx
Інтегрований чат з голосовими можливостями:
- Автоматично приймає текст з `window.onVoiceText`
- Автоматично надсилає повідомлення
- Озвучує відповідь через `window.Android.speak()`
- Показує кнопку мікрофону (🎤) коли запущений в Android

### 3. Backend (FastAPI)

#### POST /api/ci/chat
Endpoint для чату з OpenAI:

**Request:**
```json
{
  "message": "Привіт, Ci!",
  "context": {
    "history": [
      {"role": "user", "content": "Попереднє питання"},
      {"role": "assistant", "content": "Попередня відповідь"}
    ]
  }
}
```

**Response:**
```json
{
  "reply": "Привіт! Як я можу тобі допомогти? 😊",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Потік роботи (Voice Flow)

### Голосовий режим (Push-to-Talk)

1. **Користувач**: Long-press на кнопку 🎤 в Chat UI або викликає `Android.startVoice()`
2. **Android**: Запускає SpeechRecognizer з українською мовою
3. **Користувач**: Говорить текст
4. **Android**: Розпізнає текст і викликає `window.onVoiceText(text)`
5. **Frontend**: Отримує текст, вставляє в input, автоматично надсилає
6. **Backend**: Обробляє через OpenAI GPT
7. **Frontend**: Отримує відповідь, викликає `window.Android.speak(reply)`
8. **Android**: Озвучує відповідь через TTS

### Приклад коду

**Frontend (Chat.jsx):**
```javascript
const { isAndroid, startVoice, speak } = useVoiceIntegration({
  onVoiceText: (text) => {
    setInputMessage(text);
    // Auto-submit
    setTimeout(() => {
      document.querySelector('form')?.dispatchEvent(new Event('submit'));
    }, 100);
  }
});

// Send message
const response = await fetch('/api/ci/chat', {
  method: 'POST',
  body: JSON.stringify({ message: userMessage })
});
const data = await response.json();

// Speak response on Android
if (isAndroid) {
  speak(data.reply);
}
```

## Збірка та розгортання

### Збірка APK

```bash
cd android-webview

# Debug build
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk

# Release build
./gradlew assembleRelease
# Output: app/build/outputs/apk/release/app-release-unsigned.apk
```

### Встановлення

```bash
# Via ADB
adb install app/build/outputs/apk/debug/app-debug.apk

# Via USB
# 1. Enable USB Debugging on device
# 2. Connect device
# 3. In Android Studio: Run > Run 'app'
```

### Налаштування дозволів

При першому запуску:
1. **RECORD_AUDIO**: Дозволити для голосового введення
2. **SYSTEM_ALERT_WINDOW**: Дозволити для overlay (опціонально)

## Тестування

### Перевірка інтеграції

1. **WebView завантаження**:
   ```
   Відкрити додаток → має завантажитись Vercel UI
   ```

2. **Голосове введення**:
   ```
   Відкрити /chat → Натиснути 🎤 → Говорити → Текст з'являється → Відправити
   ```

3. **TTS відповідь**:
   ```
   Після відповіді від чату → Android озвучує текст
   ```

4. **Overlay**:
   ```
   Викликати enableOverlay() → Дозволити permission → Кнопка з'являється
   Tap → Відкриває додаток
   Long-press → Можна рухати
   Swipe → Закривається
   ```

### Debug логи

```bash
# Android logs
adb logcat | grep -i cimeika

# WebView console (Chrome DevTools)
chrome://inspect
```

## Конфігурація

### Android (build.gradle)

```gradle
android {
    namespace 'com.cimeika.app'
    applicationId "com.cimeika.app"
    versionCode 1
    versionName "1.0.0"
    minSdk 24  // Android 7.0+
    targetSdk 34  // Android 14
}
```

### Frontend (.env)

```bash
# API endpoint (default: localhost для розробки)
VITE_API_URL=http://localhost:5000

# Для production (Vercel автоматично підставить)
VITE_API_URL=https://your-backend.com
```

### Backend (.env)

```bash
# OpenAI API key для чату
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=500
```

## Розширення

### Додати нову Android функцію

1. **MainActivity.kt**:
```kotlin
@JavascriptInterface
fun yourNewMethod(param: String) {
    // Your Android code
}
```

2. **TypeScript definitions**:
```typescript
interface AndroidBridge {
  yourNewMethod: (param: string) => void;
}
```

3. **Frontend hook**:
```typescript
const yourNewMethod = useCallback((param: string) => {
  window.Android?.yourNewMethod(param);
}, [isAndroid]);
```

### Підтримка інших API

Можна замінити OpenAI на інший сервіс:
1. Створити новий service в `backend/services/`
2. Імпортувати в `backend/app/modules/ci/api.py`
3. Замінити `openai_service.chat()` на ваш сервіс

## Troubleshooting

### Голос не працює
- Перевірте дозвіл RECORD_AUDIO
- Переконайтесь, що мікрофон не зайнятий
- Перевірте підключення до інтернету

### TTS не озвучує
- Встановіть Google TTS або інший TTS engine
- Перевірте, що українська мова доступна в TTS
- Settings > Languages > Text-to-speech

### Overlay не з'являється
- Надайте дозвіл SYSTEM_ALERT_WINDOW
- Settings > Apps > Cimeika > Appear on top
- На деяких пристроях (Xiaomi, Huawei) є додаткові обмеження

### WebView не завантажується
- Перевірте підключення до інтернету
- Перевірте, що Vercel deployment активний
- Очистіть кеш WebView: Settings > Apps > Cimeika > Storage > Clear cache

## Ресурси

- **Android Docs**: https://developer.android.com/
- **React Docs**: https://react.dev/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenAI Docs**: https://platform.openai.com/docs/

## Контакти

Cimeika Team — https://github.com/Ihorog/cimeika-unified

## Ліцензія

Див. головний README проєкту.
