from .unsubscribe_case import unsubscribe
from .cases import register_cases_handler
from .about import register_about_handler
from .help import register_help_handler
from .start import register_start_handler

def setup_handlers(bot, repos, logger):
	register_start_handler(bot, repos, logger)
	register_help_handler(bot)
	register_about_handler(bot)
	register_cases_handler(bot, repos, logger)
	unsubscribe(bot, repos, logger)