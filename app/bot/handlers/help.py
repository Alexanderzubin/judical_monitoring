from telebot.types import Message
from app.bot.keyboards import main_menu


def register_help_handler(bot):
	@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
	def help_command(message: Message):
		help_text = (
			"<b>📖 Инструкция по использованию бота:</b>\n\n"
			"1. <b>Мои дела</b> — управление вашими подписками:\n"
			"   • <i>Подписаться на дело</i> — отправьте ссылку на интересующее дело.\n"
			"   • <i>Список моих дел</i> — просмотрите все дела, на которые вы подписаны.\n"
			"   • <i>Отписаться от дела</i> — удалите дело из списка подписок.\n\n"
			"2. <b>О боте</b> — узнайте больше о возможностях сервиса и найдите контакты поддержки.\n\n"
			"Если возникнут вопросы или что-то пойдёт не так, напишите нам в <a href='https://t.me/YourSupport'>поддержку</a> — мы поможем!"

		)
		bot.reply_to(message, help_text, parse_mode='HTML', reply_markup=main_menu())
