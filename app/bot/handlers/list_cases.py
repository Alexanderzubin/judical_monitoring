from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from app.bot.keyboards import cases_menu, generate_paginated_case_buttons
from app.bot.type import Repos

# Состояние пагинации для каждого пользователя
pagination_state = {}


def register_list_cases(bot: TeleBot, repos: Repos, logger):
	# Обработчик команды "Список моих дел"
	@bot.message_handler(func=lambda message: message.text == '📑 Список моих дел')
	def my_list_cases(message: Message):
		user = repos['user'].get_by_tg_id(message.chat.id)
		user_subs = repos['subscription'].get_user_subscriptions(user.id)

		if not user_subs:
			bot.send_message(message.chat.id, '❌ У вас нет подписок', reply_markup=cases_menu())
			return

		# Сохраняем состояние пагинации
		pagination_state[message.chat.id] = {
			'current_page': 0,
			'subscriptions': user_subs
		}

		# Отправляем сообщение с кнопками пагинации
		bot.send_message(
			message.chat.id,
			'Выберите дело, которое хотите просмотреть',
			reply_markup=generate_paginated_case_buttons(user_subs, 'list', 0)
		)

	# Обработчик для открытия деталей дела по callback
	@bot.callback_query_handler(func=lambda call: call.data.startswith('list_case_'))
	def open_case_details(call: CallbackQuery):
		try:
			sub_id = int(call.data.split('_')[-1])
			subscription = repos['subscription'].get_by_id(sub_id)
			case = repos['case'].get_by_id(subscription.case_id)

			case_text = (
				f"<b>📄 Номер дела:</b> <code>{case.number}</code>\n"
				f"<b>🏛 Суд:</b> {case.court.name if case.court else '<i>Не указан</i>'}\n"
				f"<b>👨‍⚖ Судья:</b> {case.judge.name if case.judge else '<i>Не указан</i>'}\n"
				f"<b>📅 Дата поступления:</b> <code>{case.date_of_receipt.strftime('%d.%m.%Y')}</code>\n\n"
				f"<a href='{case.url}'>🔗 Ссылка на дело</a>"
			)

			# Редактируем сообщение с деталями дела
			bot.edit_message_text(
				chat_id=call.message.chat.id,
				message_id=call.message.message_id,
				text=case_text,
				parse_mode='HTML'
			)
			bot.answer_callback_query(call.id)

		except Exception as e:
			logger.error(f'Ошибка при открытии дела: {e}')
			bot.answer_callback_query(call.id, '❌ Не удалось получить данные дела')

	# Обработчик пагинации
	@bot.callback_query_handler(func=lambda call: call.data.startswith('list_page_'))
	def handle_pagination(call: CallbackQuery):
		try:
			page = int(call.data.split('_')[-1])
			state = pagination_state.get(call.message.chat.id)

			if not state:
				bot.answer_callback_query(call.id, '⚠️ Состояние не найдено.')
				return

			state['current_page'] = page
			markup = generate_paginated_case_buttons(state['subscriptions'], 'list', page)

			# Обновляем кнопки пагинации
			bot.edit_message_reply_markup(
				chat_id=call.message.chat.id,
				message_id=call.message.message_id,
				reply_markup=markup
			)
			bot.answer_callback_query(call.id)

		except Exception as e:
			logger.error(f'Ошибка при пагинации: {e}')
			bot.answer_callback_query(call.id, '❌ Не удалось обновить страницу')
