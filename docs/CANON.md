# CANON — Cimeika Architecture Canon v1

## Overview

Cimeika is a modular personal-AI ecosystem built on a single PostgreSQL database with 7 core modules. The **Face vs Library** boundary is strict: Face components (Telegram, Web UI) never access DB directly; they go through module APIs only.

## Module Map

| Module     | Role                              | Face access |
|------------|-----------------------------------|-------------|
| **Ci**     | Central orchestration bus         | /api/v1/ci  |
| **Kazkar** | Memory & story keeper             | /api/v1/kazkar |
| **PoDiya** | Events, scenarios, reminders      | /api/v1/podija |
| **Nastrij**| Emotional state tracker           | /api/v1/nastrij |
| **Malya**  | Creativity / idea engine          | /api/v1/malya |
| **Gallery**| Visual archive (library only)     | /api/v1/gallery |
| **Calendar**| Time rhythms / scheduling (library) | /api/v1/calendar |

## Boundary Rules

- **Face** = Telegram bot + Web frontend. Reads/writes via REST API only.
- **Library** = Calendar, Gallery. No direct Telegram commands; data surfaces through Ci signals.
- **Ci orchestration bus** = `ci_signals` table. Modules post signals; Ci routes them.

## Reminder T-10m Contract

1. When a PoDiya event is created with `event_date`, a `ReminderJob` is scheduled at `event_date - 10min`.
2. A background worker queries `reminder_jobs WHERE status='pending' AND remind_at <= NOW()`.
3. Worker fires via `channel` (telegram / web / both), sets `status='sent'`.
4. If delivery fails, `status='failed'`; max 3 retries.

## Theme System

- `kazkar` module → **night** theme.
- All other modules → **day** theme.
- No user override.

## Canon Bundle ID

Every ORM entity carries `canon_bundle_id = "cimeika-v1"` for traceability.
