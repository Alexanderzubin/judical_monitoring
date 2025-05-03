from app.bot.keyboards import cases_menu, cancel_menu
from app.bot.utils import is_valid_url
from app.parser.parser import CasePageParse


def register_cases_handler(bot, repos, logger):
	@bot.message_handler(func=lambda message: message.text == '📋 Мои дела')

	def my_cases(message):
		bot.reply_to(message, 'Выберите действие:', reply_markup=cases_menu())

	@bot.message_handler(func=lambda message: message.text == '📝 Подписаться на дело')
	def subscribe_to_case(message):
		bot.reply_to(
			message, "📝 Пожалуйста, пришлите ссылку на дело, на которое хочешь подписаться.\n\n"
					 "🔗 Ссылка должна начинаться с http или https и "
					 ""
					 "вести на сайт суда (например: https://sudrf.ru/...)\n\n"
					 "❌ Чтобы выйти из режима подписки, нажмите <b>Отмена</b>.",
			parse_mode='HTML',
			reply_markup=cancel_menu()
		)

		bot.register_next_step_handler(message, wait_for_case_link)

	def wait_for_case_link(message):
		if message.text == '❌ Отмена':
			bot.send_message(
				message.chat.id,
				"Подписка на дело отменена. Вы можете вернуться в главное меню.",
				reply_markup=cases_menu()
			)
			return
		url = message.text
		url_valid = is_valid_url(message.text)
		if not url_valid:
			bot.reply_to(message, "Это не похоже на ссылку. Попробуй ещё раз.")
			bot.register_next_step_handler(message, wait_for_case_link)
			return

		try:
			user = repos['user'].get_by_tg_id(message.chat.id)
			case = repos['case'].get_by_url(url)

			if case:
				existing_subscription = repos['subscription'].get_by_user_and_case(user.id, case.id)
				if existing_subscription:
					bot.send_message(
						message.chat.id,
						"🔔 Вы уже подписаны на это дело.",
						reply_markup=cases_menu()
					)
					return
			else:
				bot.send_message(message.chat.id, '🔍 Парсим данные...')
				parser_url = CasePageParse(url=url, logger=logger)
				parser_data = parser_url.get_case_data()

				# Проверка судьи в бд и создание
				judge = repos['judge'].get_by_name(parser_data['judge'])
				if not judge:
					judge = repos['judge'].create(parser_data['judge'])

				# Проверка суда в бд и создание
				court = repos['court'].get_by_name(parser_data['court'])
				if not court:
					court = repos['court'].create(parser_data['court'])

				# Проверка категорий дела в бд и создание
				categories = []
				for name in parser_data['categories'].split('→'):
					name = name.strip()
					category = repos['category'].get_category_by_name(name)
					if not category:
						category = repos['category'].create(name)
					categories.append(category)

				# Создание дела
				case = repos['case'].create(
					number=parser_data['number'],
					unique_identifier=parser_data['unique_identifier'],
					judge=judge,
					date_of_receipt=parser_data['date_of_receipt'],
					url=url,
					court=court,
					categories=categories
				)
			# Подписка на дело
			subscription = repos['subscription'].get_by_user_and_case(user.id, case.id)
			if not subscription:
				subscription = repos['subscription'].create(user.id, case.id)

			bot.send_message(message.chat.id, "✅ Подписка на дело успешно оформлена!", reply_markup=cases_menu())


		except Exception as e:
			logger.error('Ошибка при подписке: {e}')
			bot.send_message(
				message.chat.id, 'Произошла ошибка при обработке запроса. Попробуйте позже',
				parse_mode='HTML',
				reply_markup=cases_menu()
			)
