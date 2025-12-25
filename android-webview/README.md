# Cimeika Android WebView

Android wrapper для Cimeika з голосовою розмовою (Push-to-Talk), TextToSpeech і системним overlay.

## Функції

### ✅ Основні можливості

- **WebView** відкриває https://cimeika-unified.vercel.app/
- **Push-to-Talk голос** (українська мова)
  - Tap на Ci кнопку → відкрити/закрити чат
  - Long-press на Ci кнопку → розпізнавання голосу
- **TextToSpeech** автоматично озвучує відповіді чату
- **Системний Overlay** — плаваюча кнопка Ci по всьому екрану

### 🎯 Архітектура

```
MainActivity.kt         # Головна активність з WebView
├── VoiceBridge        # JavaScript interface для голосу
│   ├── startVoice()   # Запуск розпізнавання мови
│   ├── speak(text)    # TTS озвучення
│   ├── enableOverlay()
│   └── disableOverlay()
└── TextToSpeech       # Озвучення української/англійської

OverlayService.kt      # Системна плаваюча кнопка
├── Tap               → відкриває MainActivity
├── Long-press        → режим переміщення
└── Swipe down/away   → закрити overlay
```

## Вимоги

- Android SDK 24+ (Android 7.0 Nougat і вище)
- Android Studio Giraffe (2022.3.1) або новіше
- JDK 8+
- Gradle 8.0+

## Швидкий старт

### 1. Клонування репозиторію

```bash
cd android-webview
```

### 2. Відкрити в Android Studio

1. Запустіть Android Studio
2. `File > Open` → виберіть папку `android-webview`
3. Дочекайтесь sync Gradle

### 3. Збірка Debug APK

#### Через Android Studio:
```
Build > Build Bundle(s) / APK(s) > Build APK(s)
```

#### Через командний рядок:
```bash
./gradlew assembleDebug
```

**Результат:** `app/build/outputs/apk/debug/app-debug.apk`

### 4. Збірка Release APK

#### Через командний рядок:
```bash
./gradlew assembleRelease
```

**Результат:** `app/build/outputs/apk/release/app-release-unsigned.apk`

#### Підписати Release APK (опціонально):

1. Створіть keystore:
```bash
keytool -genkey -v -keystore cimeika-release.keystore -alias cimeika -keyalg RSA -keysize 2048 -validity 10000
```

2. Додайте в `app/build.gradle`:
```gradle
android {
    signingConfigs {
        release {
            storeFile file("../cimeika-release.keystore")
            storePassword "your_password"
            keyAlias "cimeika"
            keyPassword "your_password"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
            ...
        }
    }
}
```

3. Зберіть signed APK:
```bash
./gradlew assembleRelease
```

## Встановлення на пристрій

### Через ADB:
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Через USB:
1. Увімкніть "USB Debugging" на Android пристрої
2. Підключіть пристрій до комп'ютера
3. В Android Studio: `Run > Run 'app'`

### Через файл:
1. Скопіюйте APK на пристрій
2. Відкрийте файловий менеджер
3. Натисніть на APK і підтвердіть встановлення

## Дозволи

Додаток запитує наступні дозволи:

- **INTERNET** — доступ до Vercel UI
- **RECORD_AUDIO** — розпізнавання голосу (обов'язково для Push-to-Talk)
- **SYSTEM_ALERT_WINDOW** — системний overlay (опціонально)

## Використання

### Голосовий режим (Push-to-Talk)

1. **Дозвіл на мікрофон**: При першому запуску дайте дозвіл на аудіо
2. **Long-press** на кнопку Ci в UI → розпізнавання голосу
3. Говоріть українською
4. Текст автоматично вставляється в чат і надсилається
5. Відповідь озвучується через TTS

### Overlay кнопка

1. Викличте `window.Android.enableOverlay()` з WebView або додайте кнопку в UI
2. Надайте дозвіл на overlay
3. Плаваюча кнопка Ci з'явиться
4. **Tap** → відкриває додаток
5. **Long-press** → режим переміщення (кнопка стає напівпрозорою)
6. **Swipe down/away** → закрити overlay

## JavaScript інтеграція

### Доступні методи (window.Android):

```javascript
// Запустити розпізнавання голосу
window.Android.startVoice()

// Озвучити текст (TTS)
window.Android.speak("Привіт, це Cimeika!")

// Увімкнути системний overlay
window.Android.enableOverlay()

// Вимкнути overlay
window.Android.disableOverlay()
```

### Callback для прийому голосу:

```javascript
// Встановити обробник в frontend
window.onVoiceText = (text) => {
  console.log("Voice text received:", text)
  // Вставити в поле чату
  // Автоматично надіслати повідомлення
}
```

### Приклад інтеграції з чатом:

```javascript
// 1. Прийняти голосовий текст
window.onVoiceText = async (text) => {
  // Вставити в input
  document.querySelector('#chat-input').value = text
  
  // Надіслати повідомлення
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message: text })
  })
  const data = await response.json()
  
  // Озвучити відповідь
  if (window.Android) {
    window.Android.speak(data.response)
  }
}
```

## Технічні деталі

### Версії
- **applicationId**: `com.cimeika.app`
- **versionCode**: 1
- **versionName**: 1.0.0
- **minSdk**: 24 (Android 7.0)
- **targetSdk**: 34 (Android 14)

### Залежності
- AndroidX Core KTX 1.12.0
- AndroidX AppCompat 1.6.1
- Material Components 1.11.0
- Activity KTX 1.8.2

### Підтримувані мови TTS
- Українська (uk-UA) — перший пріоритет
- English (en-US) — fallback

## Troubleshooting

### Голос не працює
1. Перевірте дозвіл RECORD_AUDIO в налаштуваннях додатку
2. Переконайтесь, що мікрофон не використовується іншим додатком
3. Перевірте підключення до інтернету (для деяких систем STT)

### TTS не озвучує
1. Перевірте, чи встановлено голосові дані для української
2. Settings > System > Languages & input > Text-to-speech
3. Встановіть Google TTS або інший голосовий движок

### Overlay не з'являється
1. Надайте дозвіл SYSTEM_ALERT_WINDOW
2. Settings > Apps > Cimeika > Appear on top (Дозволити)
3. Деякі виробники (Xiaomi, Huawei) мають додаткові обмеження

### Gradle sync failed
```bash
# Очистити і перезібрати
./gradlew clean
./gradlew build --refresh-dependencies
```

## Структура проєкту

```
android-webview/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/cimeika/webview/
│   │       │   ├── MainActivity.kt        # Головна активність
│   │       │   └── OverlayService.kt      # Системний overlay
│   │       └── AndroidManifest.xml
│   ├── build.gradle                       # Конфігурація додатку
│   └── proguard-rules.pro
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties
├── build.gradle                           # Root build config
├── settings.gradle
├── gradle.properties
├── gradlew
├── gradlew.bat
└── README.md                              # Цей файл
```

## Розробка

### Логування

```bash
# Відстежувати всі логи додатку
adb logcat | grep -i cimeika

# Відстежувати тільки помилки
adb logcat *:E
```

### Debugging

1. В Android Studio підключіть пристрій
2. Встановіть breakpoints в Kotlin коді
3. `Run > Debug 'app'`
4. Для WebView debugging:
   - Chrome: `chrome://inspect`
   - Виберіть WebView з Cimeika

## Roadmap

- [ ] Додати анімації для UI взаємодії
- [ ] Підтримка офлайн режиму
- [ ] Кастомізація кольорів overlay кнопки
- [ ] Жести для швидких дій
- [ ] Віджет на головний екран

## Ліцензія

Дивіться головний README проєкту Cimeika Unified.

## Автори

Cimeika Team — https://github.com/Ihorog/cimeika-unified
