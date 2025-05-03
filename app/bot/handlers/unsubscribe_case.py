from app.bot.keyboards import generate_unsubscribe_buttons, main_menu


def unsubscribe(bot, repos, logger):
	@bot.message_handler(func=lambda message: message.text == '🗑️ Отписаться от дела')

	def unsubscribe_case(message):
		user = repos['user'].get_by_tg_id(message.chat.id)
		user_subscription = repos['subscription'].get_user_subscriptions(user.id)
		try:
			if not user_subscription:
				bot.send_message(message.chat.id, '❌ У вас нет подписок')
				return

			bot.send_message(message.chat.id,
							 'Выберите дело, от которого хотите отписаться:',
							 reply_markup=generate_unsubscribe_buttons(user_subscription)
							 )

		except Exception as e:
			bot.send_message(message.chat.id, 'Ошибка при просмотре дел')

	@bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe_'))
	def unsubscribe_callback(call):
		subscription_id = int(call.data.split('_')[1])

		try:
			repos['subscription'].delete(subscription_id)
			bot.answer_callback_query(call.id, text='Вы успешно отписались от дела')
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
								  text='Подписка удалена')

		except Exception as e:
			logger.error(f'Произошла ошибка при отписке {e}')
			bot.answer_callback_query(call.id, text='Произошла ошибка при отписке')

	@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
	def back_to_main(message):
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
