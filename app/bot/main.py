import telebot
from app.settings import settings
from app.bot.handlers import setup_handlers

bot = telebot.TeleBot(settings.telegram_bot.bot_token)

setup_handlers(bot)


if __name__=='__main__':
	bot.polling(non_stop=True)
