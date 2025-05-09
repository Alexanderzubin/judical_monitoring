import logging

from telebot.apihelper import ApiException
from telebot.types import Message

from app.bot import bot
from app.bot.keyboards import main_menu

logger = logging.getLogger(__name__)


@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
def back_to_main(message: Message):
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except ApiException as exc:
        logger.exception('Failed to delete message', exc_info=exc)

    bot.send_message(chat_id=message.chat.id, text='Главное меню:', reply_markup=main_menu())
