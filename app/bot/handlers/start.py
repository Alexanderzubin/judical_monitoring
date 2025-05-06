from telebot.types import Message
from app.bot.keyboards import main_menu


def register_start_handler(bot, repos, logger):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        tg_id = message.from_user.id
        chat_id = message.chat.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username

        try:
            user = repos['user'].get_by_tg_id(tg_id=tg_id)

            if user:
                text = get_existing_user_text(user.first_name)
            else:
                repos['user'].create(
                    tg_id=tg_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    chat_id=chat_id
                )
                text = get_new_user_text(first_name)

            bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=main_menu())

        except Exception as e:
            logger.error(f'Ошибка в send_welcome: {e}', exc_info=True)
            bot.send_message(
                chat_id,
                'Произошла ошибка при обработке запроса.\nПопробуйте позже.',
                parse_mode='HTML'
            )


def get_existing_user_text(first_name: str) -> str:
    return (
        f"<b>Здравствуйте, {first_name}!</b>\n\n"
        "Рады снова видеть вас 😊\n"
        "Я помогу отслеживать ваши судебные дела и держать вас в курсе важных событий.\n\n"
        "Выберите, что хотите сделать:"
    )


def get_new_user_text(first_name: str) -> str:
    return (
        f"<b>Здравствуйте, {first_name}!</b>\n\n"
        "Я помогу вам следить за судебными делами: подписывайтесь на интересующие дела, "
        "получайте обновления и будьте в курсе всех важных событий.\n\n"
        "Готовы начать? Выберите нужный пункт в меню ниже 👇"
    )
