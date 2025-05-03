from app.bot.keyboards import main_menu

def register_help_handler(bot):
	@bot.message_handler(func=lambda message: message.text == '❓ Помощь')

	def help_command(message):
		help_text = (
			"<b>📖 Инструкция по использованию бота:</b>\n\n"
			"1. <b>Мои дела</b> — работа с судебными делами:\n"
			"   - <i>Подписаться на дело</i>: Введи ссылку на дело.\n"
			"   - <i>Список моих дел</i>: Посмотри все дела, на которые ты подписан.\n"
			"   - <i>Отписаться от дела</i>: Удали дело из подписок.\n\n"
			"2. <b>О боте</b> — информация о боте и контакты поддержки.\n\n"
			"Если что-то не работает, напиши в <a href='https://t.me/YourSupport'>поддержку</a>"
		)
		bot.reply_to(message, help_text, parse_mode='HTML', reply_markup=main_menu())
