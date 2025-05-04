from app.bot.keyboards import generate_paginated_case_buttons, cases_menu
from telebot.types import CallbackQuery, Message


# Словарь для хранения состояния пагинации по каждому пользователю
pagination_state = {}

def register_unsubscribe(bot, repos, logger):
    """
    Обработчик команд, связанных с отпиской от дел.
    Содержит обработку сообщений и callback-запросов от пользователей.
    """

    @bot.message_handler(func=lambda message: message.text == '🗑️ Отписаться от дела')
    def unsubscribe_case(message: Message):
        """
        Обрабатывает запрос на отписку от дела.
        Показывает список дел, от которых можно отписаться.
        """
        user = repos['user'].get_by_tg_id(message.chat.id)
        user_subscription = repos['subscription'].get_user_subscriptions(user.id)

        try:
            if not user_subscription:
                bot.send_message(message.chat.id, '❌ У вас нет подписок')
                return

            # Сохраняем состояние пагинации
            pagination_state[message.chat.id] = {'current_page': 0, 'subscriptions': user_subscription}

            bot.send_message(
                message.chat.id,
                'Выберите дело, от которого хотите отписаться:',
                reply_markup=generate_paginated_case_buttons(user_subscription, 'unsubscribe', 0)
            )

        except Exception as e:
            logger.error(f'Ошибка при получении подписок: {e}')
            bot.send_message(message.chat.id, 'Произошла ошибка при просмотре подписок')

    @bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe_case_'))
    def unsubscribe_callback(call: CallbackQuery):
        """
        Обрабатывает запрос на отписку от конкретного дела.
        """
        subscription_id = int(call.data.split('_')[-1])

        try:
            repos['subscription'].delete(subscription_id)
            bot.answer_callback_query(call.id, text='✅ Вы успешно отписались от дела')
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Подписка удалена'
            )
        except Exception as e:
            logger.error(f'Ошибка при отписке: {e}')
            bot.answer_callback_query(call.id, text='❌ Произошла ошибка при отписке')

    @bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe_page_'))
    def paginate(call: CallbackQuery):
        """
        Обрабатывает пагинацию для списка дел.
        """
        user_id = call.message.chat.id
        page_number = int(call.data.split('_')[-1])

        user_subscription = pagination_state[user_id]['subscriptions']
        pagination_state[user_id]['current_page'] = page_number

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='Выберите дело, от которого хотите отписаться:',
            reply_markup=generate_paginated_case_buttons(user_subscription, 'unsubscribe', page_number)
        )

    @bot.callback_query_handler(func=lambda call: call.data == 'cancel')
    def cancel_callback(call: CallbackQuery):
        """
        Обрабатывает кнопку "Отмена".
        """
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text='Выберите действие:', reply_markup=cases_menu())
