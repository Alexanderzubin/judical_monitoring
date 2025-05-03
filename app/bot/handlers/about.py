from app.bot.keyboards import main_menu


def register_about_handler(bot):
	@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')

	def about_command(message):
		about_text = (
			"<b>О боте:</b>\n\n"
			"Я бот для отслеживания судебных дел. Помогу следить за статусами дел по вашим ссылкам.\n\n"
			"<b>Версия:</b> 1.0"
		)
		bot.reply_to(message, about_text, parse_mode='HTML', reply_markup=main_menu())
