from telebot import TeleBot

from app.settings import settings

bot = TeleBot(settings.telegram_bot.bot_token)


def get_bot() -> TeleBot:
    import app.bot.handlers  # noqa: F401, F403, E402

    return bot
