from telebot.types import Message
from app.bot.keyboards import main_menu


def register_cancel_button(bot):
    @bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
    def back_to_main(message: Message):
        try:
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception:
            pass

        bot.send_message(
            chat_id=message.chat.id,
            text="Главное меню:",
            reply_markup=main_menu()
        )
