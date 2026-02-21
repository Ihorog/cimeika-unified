"""
Podija Telegram bot — MVP command handlers.

Commands:
  /add <date> <time> <title> [duration_minutes]
  /today   — events for today
  /week    — events for the next 7 days
  /done <id>   — mark event as completed
  /cancel <id> — delete event
  /help    — show this help

Environment variables required:
  TELEGRAM_BOT_TOKEN   — bot token from @BotFather
  TELEGRAM_CHAT_ID     — allowed chat/user ID (security filter)
"""
import os
import logging

try:
    import telebot  # pyTelegramBotAPI
    _TELEBOT_AVAILABLE = True
except ImportError:  # pragma: no cover
    _TELEBOT_AVAILABLE = False

from app.config.database import SessionLocal
from app.modules.podija.parser import parse_add_args
from app.modules.podija.schema import PodijaEventCreate
from app.modules.podija.service import PodijaService

logger = logging.getLogger(__name__)

_service = PodijaService()
_service.initialize()

_HELP_TEXT = (
    "📅 *Podija — команди бота*\n\n"
    "/add <дата> <час> <назва> [хв]\n"
    "  Додати подію. Дата: сьогодні/завтра/РРРР-ММ-ДД/ДД.ММ.РРРР\n"
    "  Приклади:\n"
    "    /add завтра 18:00 зустріч\n"
    "    /add 2026-03-01 18:00 зустріч 60\n\n"
    "/today — події на сьогодні\n"
    "/week  — події на 7 днів\n"
    "/done <id>   — відмітити виконаною\n"
    "/cancel <id> — скасувати (видалити) подію\n"
    "/help  — ця довідка"
)


def _fmt_event(event) -> str:
    date_str = event.event_date.strftime("%d.%m %H:%M") if event.event_date else "—"
    return f"• [{event.id}] {date_str} — {event.title}"


def _fmt_list(events, empty_msg: str) -> str:
    if not events:
        return empty_msg
    return "\n".join(_fmt_event(e) for e in events)


def _allowed(message) -> bool:
    allowed_id = os.getenv("TELEGRAM_CHAT_ID")
    return allowed_id is None or str(message.chat.id) == allowed_id


def register_handlers(bot) -> None:
    """Register all podija command handlers on *bot* (telebot.TeleBot instance)."""

    @bot.message_handler(commands=["help"])
    def cmd_help(message):
        if not _allowed(message):
            return
        bot.reply_to(message, _HELP_TEXT, parse_mode="Markdown")

    @bot.message_handler(commands=["add"])
    def cmd_add(message):
        if not _allowed(message):
            return
        args = message.text.partition(" ")[2].strip()
        if not args:
            bot.reply_to(
                message,
                "Вкажіть аргументи. Приклад:\n/add завтра 18:00 зустріч 60",
            )
            return

        parsed = parse_add_args(args)
        if parsed["error"]:
            bot.reply_to(message, f"❌ {parsed['error']}")
            return

        db = SessionLocal()
        try:
            event_data = PodijaEventCreate(
                title=parsed["title"],
                event_date=parsed["event_date"],
                event_type="planned",
                source_trace="telegram",
            )
            event = _service.create_event(db, event_data)
            date_str = event.event_date.strftime("%d.%m.%Y %H:%M") if event.event_date else "—"
            duration_note = (
                f"\n⏱ Тривалість: {parsed['duration_minutes']} хв"
                if parsed["duration_minutes"]
                else ""
            )
            bot.reply_to(
                message,
                f"✅ Подію додано!\n📌 [{event.id}] {event.title}\n📅 {date_str}{duration_note}",
            )
        except Exception as exc:
            logger.error("cmd_add error: %s", exc, exc_info=True)
            bot.reply_to(message, f"❌ Помилка збереження: {exc}")
        finally:
            db.close()

    @bot.message_handler(commands=["today"])
    def cmd_today(message):
        if not _allowed(message):
            return
        db = SessionLocal()
        try:
            events = _service.get_today_events(db)
            bot.reply_to(
                message,
                "📅 *Події на сьогодні:*\n" + _fmt_list(events, "Подій немає 🎉"),
                parse_mode="Markdown",
            )
        except Exception as exc:
            logger.error("cmd_today error: %s", exc, exc_info=True)
            bot.reply_to(message, f"❌ Помилка: {exc}")
        finally:
            db.close()

    @bot.message_handler(commands=["week"])
    def cmd_week(message):
        if not _allowed(message):
            return
        db = SessionLocal()
        try:
            events = _service.get_week_events(db)
            bot.reply_to(
                message,
                "📆 *Події на тиждень:*\n" + _fmt_list(events, "Подій немає 🎉"),
                parse_mode="Markdown",
            )
        except Exception as exc:
            logger.error("cmd_week error: %s", exc, exc_info=True)
            bot.reply_to(message, f"❌ Помилка: {exc}")
        finally:
            db.close()

    @bot.message_handler(commands=["done"])
    def cmd_done(message):
        if not _allowed(message):
            return
        args = message.text.partition(" ")[2].strip()
        if not args.isdigit():
            bot.reply_to(message, "Вкажіть ID події. Приклад: /done 3")
            return
        event_id = int(args)
        db = SessionLocal()
        try:
            event = _service.mark_done(db, event_id)
            if not event:
                bot.reply_to(message, f"❌ Подію #{event_id} не знайдено.")
            else:
                bot.reply_to(message, f"✅ Подію [{event.id}] «{event.title}» позначено виконаною!")
        except Exception as exc:
            logger.error("cmd_done error: %s", exc, exc_info=True)
            bot.reply_to(message, f"❌ Помилка: {exc}")
        finally:
            db.close()

    @bot.message_handler(commands=["cancel"])
    def cmd_cancel(message):
        if not _allowed(message):
            return
        args = message.text.partition(" ")[2].strip()
        if not args.isdigit():
            bot.reply_to(message, "Вкажіть ID події. Приклад: /cancel 3")
            return
        event_id = int(args)
        db = SessionLocal()
        try:
            success = _service.delete_event(db, event_id)
            if not success:
                bot.reply_to(message, f"❌ Подію #{event_id} не знайдено.")
            else:
                bot.reply_to(message, f"🗑 Подію #{event_id} видалено.")
        except Exception as exc:
            logger.error("cmd_cancel error: %s", exc, exc_info=True)
            bot.reply_to(message, f"❌ Помилка: {exc}")
        finally:
            db.close()


def create_bot() -> "telebot.TeleBot":
    """Create and return a configured TeleBot instance with all handlers registered."""
    if not _TELEBOT_AVAILABLE:
        raise RuntimeError(
            "pyTelegramBotAPI is not installed. "
            "Add 'pyTelegramBotAPI' to requirements.txt and install it."
        )
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set.")
    bot = telebot.TeleBot(token)
    register_handlers(bot)
    return bot


def run_bot() -> None:
    """Entry point: create bot and start polling."""
    bot = create_bot()
    logger.info("Podija Telegram bot started (polling)...")
    bot.infinity_polling()
