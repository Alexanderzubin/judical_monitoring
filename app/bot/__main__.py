import logging

from app.bot.loader import get_bot
from app.logging_config import setup_logging

setup_logging()

logger = logging.getLogger('telegram_bot')


def main():
    logger.info('Start bot infinity polling')

    bot = get_bot()
    bot.infinity_polling()

    logger.info('Stop bot infinity polling')


if __name__ == '__main__':
    main()
