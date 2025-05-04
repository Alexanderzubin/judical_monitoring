import telebot

from app.settings import settings
from app.bot.setup_hundlers import setup_handlers
from app.bot.type import Repos

from app.database.session import Session

from app.database.repositories.user import UserRepository
from app.database.repositories.case import CaseRepository
from app.database.repositories.subscription import SubscriptionRepository
from app.database.repositories.judge import JudgeRepository
from app.database.repositories.court import Courtepository
from app.database.repositories.category import CategoryRepository

import logging

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

session = Session()

bot = telebot.TeleBot(settings.telegram_bot.bot_token)

repos: Repos = {
	'user': UserRepository(session, logger),
	'case': CaseRepository(session, logger),
	'subscription': SubscriptionRepository(session, logger),
	'judge': JudgeRepository(session, logger),
	'court': Courtepository(session, logger),
	'category': CategoryRepository(session, logger)
	}

setup_handlers(bot, repos, logger)

if __name__ == '__main__':
    logger.info("Bot is starting...")
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        logger.exception("Bot crashed with exception:")
    finally:
        logger.info("Bot stopped.")
