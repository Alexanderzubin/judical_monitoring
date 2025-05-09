from app.bot.handlers.unsubscribe_case import register_unsubscribe
from app.bot.handlers.cases import register_cases_handler
from app.bot.handlers.about import register_about_handler
from app.bot.handlers.help import register_help_handler
from app.bot.handlers.start import register_start_handler
from app.bot.handlers.list_cases import register_list_cases
from app.bot.handlers.cancel import register_cancel_button


def setup_handlers(bot, repos, logger):
    register_start_handler(bot, repos, logger)
    register_help_handler(bot)
    register_about_handler(bot)
    register_cases_handler(bot, repos, logger)
    register_unsubscribe(bot, repos, logger)
    register_list_cases(bot, repos, logger)
    register_cancel_button(bot)
