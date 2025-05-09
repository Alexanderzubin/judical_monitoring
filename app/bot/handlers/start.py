import logging

from telebot.types import Message
from app.bot import bot
from app.bot.keyboards import main_menu
from app.database.session import Session
from app.services.users import UserService

logger = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    tg_id = message.chat.id
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    with Session() as session:
        try:
            user_service = UserService.get_service(session)
            user = user_service.get_user_by_telegram_id(tg_id)
            if not user:
                user_service.create_user(
                    tg_id=tg_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    chat_id=chat_id,
                )
                text = get_new_user_text(first_name)
            else:
                text = get_existing_user_text(first_name)

            bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=main_menu())
        except Exception as exc:
            logger.exception('Ошибка в send_welcome', exc_info=exc)
            bot.send_message(
                chat_id,
                'Произошла ошибка при обработке запроса.\nПопробуйте позже.',
                parse_mode='HTML',
            )


def get_existing_user_text(first_name: str) -> str:
    return (
        f'<b>Здравствуйте, {first_name}!</b>\n\n'
        'Рады снова видеть вас 😊\n'
        'Я помогу отслеживать ваши судебные дела и держать вас в курсе важных событий.\n\n'
        'Выберите, что хотите сделать:'
    )


def get_new_user_text(first_name: str) -> str:
    return (
        f'<b>Здравствуйте, {first_name}!</b>\n\n'
        'Я помогу вам следить за судебными делами: подписывайтесь на интересующие дела, '
        'получайте обновления и будьте в курсе всех важных событий.\n\n'
        'Готовы начать? Выберите нужный пункт в меню ниже 👇'
    )
