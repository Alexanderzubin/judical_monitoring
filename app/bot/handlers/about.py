from telebot.types import Message
from app.bot.keyboards import main_menu


def register_about_handler(bot):
    @bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
    def about_command(message: Message):
        bot.reply_to(
            message,
            get_about_text(),
            parse_mode='HTML',
            reply_markup=main_menu()
        )


def get_about_text() -> str:
    return (
        "<b>О боте:</b>\n\n"
        "Я — бот, который поможет вам отслеживать судебные дела. "
        "Просто добавьте ссылку, и я буду сообщать об изменениях по каждому делу.\n\n"
        "<b>Текущая версия:</b> 1.0"
    )
