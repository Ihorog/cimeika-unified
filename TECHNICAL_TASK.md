# 🧩 TECHNICAL TASK · CIMEIKA UNIFIED
## Architecture Normalization & UI Skeleton Alignment

Repository: `Ihorog/cimeika-unified`  
Status: active execution  
Language: uk / en (code comments allowed)

---

## 0. CORE PRINCIPLE

The system must be reduced to a **single coherent product skeleton**:

- One backend
- One frontend
- One center (Ci)
- 7 modules as **interfaces**, not services
- Minimal infrastructure
- Deterministic UI behavior

Any redundancy is considered a defect.

---

## 1. TARGET STATE (DEFINITION OF DONE)

The repository must represent a **working product shell**, not a concept demo.

The following must be true:

- The application runs locally via `docker-compose up`
- All 7 modules render visible UI screens
- Ci overlay is accessible from every screen
- Theming is deterministic and module-based
- README describes reality only

---

## 2. BACKEND · NORMALIZATION

### 2.1 Framework Rule

- **FastAPI is the only allowed backend framework**
- Flask must not participate in runtime execution

### 2.2 Required Actions

1. Detect any Flask-based code:
   - Flask app instances
   - Flask routes
   - Flask dependencies

2. Move all Flask-related files to:
   ```
   /archive/flask/
   ```

3. Ensure no Flask imports are used anywhere outside `/archive`

---

### 2.3 Backend Entry Point

Single entry point:
```
backend/main.py
```

Responsibilities:
- Initialize FastAPI app
- Load configuration
- Register module routers
- Expose root health endpoint

---

### 2.4 Backend Structure (MANDATORY)

```
backend/
├─ main.py
├─ app/
│   ├─ core/
│   │   ├─ config.py
│   │   └─ settings.py
│   ├─ modules/
│   │   ├─ ci/
│   │   │   └─ api.py
│   │   ├─ podija/
│   │   │   └─ api.py
│   │   ├─ nastrij/
│   │   │   └─ api.py
│   │   ├─ malya/
│   │   │   └─ api.py
│   │   ├─ kazkar/
│   │   │   └─ api.py
│   │   ├─ calendar/
│   │   │   └─ api.py
│   │   └─ gallery/
│   │       └─ api.py
```

---

## 3. FRONTEND · UI SKELETON

### 3.1 Framework

- React
- Vite
- Existing tooling must be preserved

---

### 3.2 Module-Based UI Architecture

Each module is a **screen**, not a component.

Mandatory structure:

```
frontend/src/modules/
├─ ci/
│   └─ CiView.jsx
├─ podija/
│   └─ PodijaView.jsx
├─ nastrij/
│   └─ NastrijView.jsx
├─ malya/
│   └─ MalyaView.jsx
├─ kazkar/
│   └─ KazkarView.jsx
├─ calendar/
│   └─ CalendarView.jsx
└─ gallery/
    └─ GalleryView.jsx
```

---

## 4. CI · GLOBAL OVERLAY

### 4.1 Ci Role

Ci is the **global interaction anchor**.

Rules:
- Always visible
- Always clickable
- Never blocks navigation state

---

### 4.2 Overlay Behavior

- Opens as overlay or drawer
- Appears above current screen
- Can be closed without losing context

Scope:
- UI shell only
- Text + voice placeholders allowed
- No AI integration required

---

## 5. THEME SYSTEM (NON-OPTIONAL)

### 5.1 Theme Determinism

Themes are NOT user-controlled.

They are derived strictly from module context.

---

### 5.2 Theme Map

| Module     | Theme  |
|-----------|--------|
| kazkar    | night  |
| ci        | day    |
| podija   | day    |
| nastrij  | day    |
| malya    | day    |
| calendar | day    |
| gallery  | day    |

---

## 6. INFRASTRUCTURE · MINIMAL MODE

### 6.1 docker-compose.yml

Allowed services:
- frontend
- backend
- postgres (only if already used)

Forbidden (must be commented):
- Redis
- Message brokers
- Background workers

---

## 7. README · REALITY-ONLY DOCUMENT

Rewrite `README.md` to include ONLY:

1. What works now
2. What is in progress
3. What is disabled / archived
4. Local run instructions (max 3 commands)
5. Module map (7 modules, 1 line each)

Forbidden content:
- Vision statements
- Roadmaps
- Marketing language
- Speculative features

---

## 8. IMPLEMENTATION ORDER (STRICT)

1. Backend normalization
2. UI skeletons (7 modules)
3. Ci overlay
4. Theme system
5. docker-compose cleanup
6. README rewrite

Deviation is not allowed.

---

## 9. ACCEPTANCE CHECKLIST (BINARY)

- [ ] FastAPI is the only backend
- [ ] Flask code is archived
- [ ] All 7 modules render UI
- [ ] Ci overlay works globally
- [ ] Theme is deterministic
- [ ] docker-compose is minimal
- [ ] README reflects reality

If any item is false → task is NOT complete.

---

END OF TECHNICAL TASK
