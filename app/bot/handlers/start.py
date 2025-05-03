from app.bot.keyboards import main_menu

def register_start_handler(bot, repos, logger):
	@bot.message_handler(commands=['start'])
	def send_welcome(message):
		try:
			tg_id = message.from_user.id
			user = repos['user'].get_by_tg_id(tg_id=tg_id)
			if user:
				welcome_text = (
					f"<b>Привет, {user.first_name}!</b>\n\n"
					"<i>Рад видеть тебя снова!</i> Я помогу отслеживать твои судебные дела. "
					"Выбери действие в меню ниже:"
				)
				bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=main_menu())
			else:
				repos['user'].create(
					tg_id=tg_id,
					first_name=message.from_user.first_name,
					last_name=message.from_user.last_name,
					username=message.from_user.username,
					chat_id=message.chat.id
				)
				welcome_text = (
					f"<b>Добро пожаловать, {message.from_user.first_name}!</b>\n\n"
					"<i>Я твой помощник по отслеживанию судебных дел.</i> "
					"Подписывайся на дела, следи за их статусами и управляй подписками. "
					"Начнём? Выбери действие в меню:"
				)
				bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=main_menu())
		except Exception as e:
			logger.error(f'Ошибка в send_welcome: {e}')
			bot.send_message(
				message.chat.id, 'Произошла ошибка при обработке запроса.\nПопробуйте позже',
				parse_mode='HTML'
			)