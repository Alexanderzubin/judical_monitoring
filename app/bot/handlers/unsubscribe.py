import logging

from telebot.types import CallbackQuery, Message

from app.bot import bot
from app.bot.constants import SUBSCRIPTIONS_PER_PAGE
from app.bot.keyboards import generate_paginated_case_buttons, cases_menu
from app.database.session import Session
from app.services.subscriptions import SubscriptionService
from app.services.users import UserService

logger = logging.getLogger(__name__)


# Словарь для хранения состояния пагинации по каждому пользователю
_pagination_state = {}


@bot.message_handler(func=lambda message: message.text == '🗑️ Отписаться от дела')
def unsubscribe_from_cases(message: Message):
    """
    Обрабатывает запрос на отписку от дела.
    Показывает список дел, от которых можно отписаться.
    """
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    current_page = 0

    with Session() as session:
        try:
            user_service = UserService.get_service(session)
            user = user_service.find_user_by_telegram_id(message.chat.id)

            subscription_service = SubscriptionService.get_service(session)
            total_subscriptions_count = subscription_service.get_user_subscriptions_count(user)
            if not total_subscriptions_count:
                bot.send_message(message.chat.id, '⚠️ У вас нет подписок')
                return

            user_subscriptions = subscription_service.get_user_subscriptions(
                user,
                limit=SUBSCRIPTIONS_PER_PAGE,
                offset=current_page,
            )

            # Сохраняем состояние пагинации
            _pagination_state[message.chat.id] = {'current_page': 0}

            bot.send_message(
                message.chat.id,
                'Выберите дело, от которого хотите отписаться:',
                reply_markup=generate_paginated_case_buttons(
                    user_subscriptions,
                    prefix='unsubscribe',
                    page_number=current_page,
                    items_per_page=SUBSCRIPTIONS_PER_PAGE,
                    total_subscriptions_count=total_subscriptions_count,
                ),
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

    with Session() as session:
        try:
            user_service = UserService.get_service(session)
            user = user_service.find_user_by_telegram_id(call.message.chat.id)

            subscription_service = SubscriptionService.get_service(session)
            subscription = subscription_service.find_subscription_by_id(subscription_id)
            case = subscription.case

            subscription_service.unsubscribe_user(user, case)
            bot.send_message(
                chat_id=call.message.chat.id,
                parse_mode='HTML',
                text=f'✅ Вы успешно отписались от дела: <a href="{case.url}">{case.number}</a>',
            )
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            logger.error(f'Ошибка при отписке: {e}')
            bot.answer_callback_query(call.id, text='❌ Произошла ошибка при отписке')


@bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe_page_'))
def handle_unsubscribe_pagination(call: CallbackQuery):
    """
    Обрабатывает пагинацию для списка дел.
    """
    with Session() as session:
        try:
            current_page = int(call.data.split('_')[-1])

            user_service = UserService.get_service(session)
            user = user_service.find_user_by_telegram_id(call.message.chat.id)

            subscription_service = SubscriptionService.get_service(session)

            user_subscriptions = subscription_service.get_user_subscriptions(
                user,
                limit=SUBSCRIPTIONS_PER_PAGE,
                offset=current_page,
            )
            total_subscriptions_count = subscription_service.get_user_subscriptions_count(user)

            state = _pagination_state.get(call.message.chat.id)

            if not state:
                bot.answer_callback_query(call.id, '⚠️ Состояние не найдено.')
                return

            state['current_page'] = current_page

            markup = generate_paginated_case_buttons(
                subscriptions_page=user_subscriptions,
                prefix='unsubscribe',
                page_number=current_page,
                items_per_page=SUBSCRIPTIONS_PER_PAGE,
                total_subscriptions_count=total_subscriptions_count,
            )

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='Выберите дело, от которого хотите отписаться:',
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        except Exception as exc:
            logger.error('Ошибка при пагинации', exc_info=exc)
            bot.answer_callback_query(call.id, '❌ Не удалось обновить страницу')
