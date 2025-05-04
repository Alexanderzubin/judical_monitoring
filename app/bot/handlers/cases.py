from telebot.types import Message
from app.bot.keyboards import cases_menu, cancel_menu
from app.bot.utils import is_valid_url
from app.parser.parser import CasePageParse


def register_cases_handler(bot, repos, logger):
	@bot.message_handler(func=lambda msg: msg.text == '📋 Мои дела')

	def my_cases(message: Message):
		bot.reply_to(message, 'Выберите действие:', reply_markup=cases_menu())

	@bot.message_handler(func=lambda msg: msg.text == '📝 Подписаться на дело')
	def subscribe_to_case(message: Message):
		bot.reply_to(
			message,
			(
				"📝 <b>Подписка на судебное дело</b>\n\n"
				"Пожалуйста, отправьте ссылку на интересующее Вас дело.\n\n"
				"🔗 Ссылка должна начинаться с <code>http://</code> или <code>https://</code> и вести на сайт суда\n"
				"Например: <i>https://sudrf.ru/...</i>\n\n"
				"❌ Чтобы отменить подписку, нажмите кнопку <b>Отмена</b> ниже."
			),
			parse_mode='HTML',
			reply_markup=cancel_menu()
		)
		bot.register_next_step_handler(message, wait_for_case_link)

	def wait_for_case_link(message: Message):
		if message.text == '❌ Отмена':
			bot.send_message(
				message.chat.id,
				"Вы отменили подписку на дело. Возвращаюсь в меню.",
				reply_markup=cases_menu()
			)
			return

		url = message.text.strip()
		if not is_valid_url(url):
			bot.reply_to(message, "⚠️ Это не похоже на корректную ссылку. Пожалуйста, проверьте и отправьте повторно.")
			bot.register_next_step_handler(message, wait_for_case_link)
			return

		try:
			user = repos['user'].get_by_tg_id(message.chat.id)
			case = repos['case'].get_by_url(url)

			if case:
				if repos['subscription'].get_by_user_and_case(user.id, case.id):
					bot.send_message(
						message.chat.id,
						"🔔 Вы уже подписаны на это дело. Мы продолжим уведомлять Вас об изменениях.",
						reply_markup=cases_menu()
					)
					return
			else:
				bot.send_message(message.chat.id, '🔍 Обрабатываем ссылку, пожалуйста, подождите...')
				parser = CasePageParse(url=url, logger=logger)
				data = parser.get_case_data()

				judge = repos['judge'].get_by_name(data['judge']) or repos['judge'].create(data['judge'])
				court = repos['court'].get_by_name(data['court']) or repos['court'].create(data['court'])

				categories = []
				for name in map(str.strip, data['categories'].split('→')):
					category = repos['category'].get_category_by_name(name) or repos['category'].create(name)
					categories.append(category)

				case = repos['case'].create(
					number=data['number'],
					unique_identifier=data['unique_identifier'],
					judge=judge,
					date_of_receipt=data['date_of_receipt'],
					url=url,
					court=court,
					categories=categories
				)

			if not repos['subscription'].get_by_user_and_case(user.id, case.id):
				repos['subscription'].create(user.id, case.id)

			bot.send_message(message.chat.id,
							 "✅ Подписка успешно оформлена. Мы будем уведомлять Вас о всех изменениях по делу.",
							 reply_markup=cases_menu()
							 )

		except Exception as e:
			logger.error(f'Ошибка при подписке: {e}')
			bot.send_message(
				message.chat.id,
				'⚠️ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.',
				reply_markup=cases_menu()
			)
