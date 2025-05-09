from telebot.types import Message

from app.bot import bot
from app.bot.keyboards import main_menu

ABOUT_TEXT = """\
<b>О боте:</b>\n\n
Я — бот, который поможет вам отслеживать судебные дела. \
Просто добавьте ссылку, и я буду сообщать об изменениях по каждому делу."

<b>Текущая версия:</b> 1.0\
"""


@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
def about_command(message: Message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(
        chat_id=message.chat.id, text=ABOUT_TEXT, parse_mode='HTML', reply_markup=main_menu()
    )
