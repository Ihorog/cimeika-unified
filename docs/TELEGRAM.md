# TELEGRAM — Cimeika Telegram Bot Integration

## Overview

The Telegram Face layer is a thin bot that maps user commands to module REST API calls. It never reads the database directly.

## Bot Commands (PoDiya MVP)

| Command                     | Action                              | API call                              |
|-----------------------------|-------------------------------------|---------------------------------------|
| `/event <title>`            | Create a new event (today)          | `POST /api/v1/podija/events`          |
| `/today`                    | List today's events                 | `GET  /api/v1/podija/events/today`    |
| `/week`                     | List this week's events             | `GET  /api/v1/podija/events/week`     |
| `/done <id>`                | Mark event as done                  | `POST /api/v1/podija/events/{id}/done`|
| `/cancel <id>`              | Cancel an event                     | `POST /api/v1/podija/events/{id}/cancel`|
| `/health`                   | Show system health                  | `GET  /health`                        |
| `/status`                   | Show system status                  | `GET  /api/status`                    |

## Reminder T-10m

When a `ReminderJob` fires, the worker calls the Telegram Bot API:

```
POST https://api.telegram.org/bot{TOKEN}/sendMessage
{
  "chat_id": "<user_chat_id>",
  "text": "⏰ Reminder: <event_title> starts in 10 minutes"
}
```

## Environment Variables

| Variable            | Description                          |
|---------------------|--------------------------------------|
| `TELEGRAM_BOT_TOKEN`| BotFather token                      |
| `TELEGRAM_CHAT_ID`  | Default chat/user ID for reminders   |

## Webhook Setup

```bash
curl -X POST "https://api.telegram.org/bot${TOKEN}/setWebhook" \
  -d "url=https://<your-domain>/telegram/webhook"
```

## Security

- Validate `X-Telegram-Bot-Api-Secret-Token` header on webhook endpoint.
- Never store raw message content in logs.
- Bot token stored only in GitHub Secrets / `.env` (not committed).
