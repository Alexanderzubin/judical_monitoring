import logging

from telebot.types import Message, CallbackQuery

from app.bot import bot
from app.bot.constants import SUBSCRIPTIONS_PER_PAGE
from app.bot.keyboards import cases_menu, cancel_menu, generate_paginated_case_buttons
from app.bot.utils import is_valid_url
from app.database.session import Session
from app.services.cases import CaseService
from app.services.subscriptions import SubscriptionService
from app.services.users import UserService

logger = logging.getLogger(__name__)

# Состояние пагинации для каждого пользователя
_pagination_state = {}


@bot.message_handler(func=lambda msg: msg.text == '📋 Мои дела')
def my_cases(message: Message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=cases_menu())


def wait_for_case_link(message: Message) -> None:
    if message.text == '⬅️ Назад':
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(
            chat_id=message.chat.id, text='Выберите действие:', reply_markup=cases_menu()
        )
        return

    url = message.text.strip()
    if not is_valid_url(url):
        bot.reply_to(
            message,
            '⚠️ Это не похоже на корректную ссылку. Пожалуйста, проверьте и отправьте повторно.',
        )
        bot.register_next_step_handler(message, wait_for_case_link)
        return

    with Session() as session:
        try:
            user_service = UserService.get_service(session)
            case_service = CaseService.get_service(session)
            subscription_service = SubscriptionService.get_service(session)

            user = user_service.find_user_by_telegram_id(message.chat.id)
            case = case_service.get_case_by_url(url)
            is_new_case = case is None

            if is_new_case:
                bot.send_message(
                    message.chat.id, '🔍 Обрабатываем ссылку, пожалуйста, подождите...'
                )
                case, created = case_service.get_or_create_case(url)
                is_new_case = created

            if not is_new_case:
                if subscription_service.is_user_subscribed_to_case(user, case):
                    bot.send_message(
                        message.chat.id,
                        '🔔 Вы уже подписаны на это дело. Мы продолжим уведомлять Вас об изменениях.',
                        reply_markup=cases_menu(),
                    )
                    return

            subscription_service.subscribe_user(user, case)
            bot.send_message(
                message.chat.id,
                '✅ Подписка успешно оформлена. Мы будем уведомлять Вас о всех изменениях по делу.',
                reply_markup=cases_menu(),
            )
        except Exception as exc:
            logger.exception('Error during subscription', exc_info=exc)
            bot.send_message(
                message.chat.id,
                '⚠️ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.',
                reply_markup=cases_menu(),
            )


@bot.message_handler(func=lambda msg: msg.text == '📝 Подписаться на дело')
def subscribe_to_case(message: Message) -> None:
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    bot.send_message(
        message.chat.id,
        (
            '📝 <b>Подписка на судебное дело</b>\n\n'
            'Пожалуйста, отправьте ссылку на интересующее Вас дело.\n\n'
            '🔗 Ссылка должна начинаться с <code>http://</code> или <code>https://</code> и вести на сайт суда\n'
            'Например: <i>https://sudrf.ru/...</i>'
        ),
        parse_mode='HTML',
        reply_markup=cancel_menu(),
    )
    bot.register_next_step_handler(message, wait_for_case_link)


@bot.message_handler(func=lambda message: message.text == '📑 Список моих дел')
def my_list_cases(message: Message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    current_page = 0

    with Session() as session:
        try:
            user_service = UserService.get_service(session)
            user = user_service.find_user_by_telegram_id(message.chat.id)

            subscription_service = SubscriptionService.get_service(session)
            total_subscriptions_count = subscription_service.get_user_subscriptions_count(user)

            if not total_subscriptions_count:
                bot.send_message(message.chat.id, '⚠️ У вас нет подписок', reply_markup=cases_menu())
                return

            user_subscriptions = subscription_service.get_user_subscriptions(
                user,
                limit=SUBSCRIPTIONS_PER_PAGE,
                offset=current_page,
            )

            # Сохраняем состояние пагинации
            _pagination_state[message.chat.id] = {'current_page': current_page}

            # Отправляем сообщение с кнопками пагинации
            bot.send_message(
                message.chat.id,
                'Выберите дело, которое хотите просмотреть',
                reply_markup=generate_paginated_case_buttons(
                    subscriptions_page=user_subscriptions,
                    prefix='list',
                    page_number=current_page,
                    items_per_page=SUBSCRIPTIONS_PER_PAGE,
                    total_subscriptions_count=total_subscriptions_count,
                ),
            )

        except Exception as exc:
            logger.exception('Error during list cases', exc_info=exc)
            bot.send_message(
                message.chat.id,
                '⚠️ Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.',
                reply_markup=cases_menu(),
            )


@bot.callback_query_handler(func=lambda call: call.data.startswith('list_page_'))
def handle_pagination(call: CallbackQuery):
    with Session() as session:
        try:
            current_page = int(call.data.split('_')[-1])

            user_service = UserService.get_service(session)
            subscription_service = SubscriptionService.get_service(session)

            user = user_service.find_user_by_telegram_id(call.message.chat.id)
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
                prefix='list',
                page_number=current_page,
                items_per_page=SUBSCRIPTIONS_PER_PAGE,
                total_subscriptions_count=total_subscriptions_count,
            )

            # Обновляем кнопки пагинации
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup,
            )
            bot.answer_callback_query(call.id)

        except Exception as exc:
            logger.error('Ошибка при пагинации', exc_info=exc)
            bot.answer_callback_query(call.id, '❌ Не удалось обновить страницу')


@bot.callback_query_handler(func=lambda call: call.data.startswith('list_case_'))
def open_case_details(call: CallbackQuery):
    with Session() as session:
        try:
            UserService.get_service(session)
            subscription_service = SubscriptionService.get_service(session)

            subscription_id = int(call.data.split('_')[-1])
            subscription = subscription_service.find_subscription_by_id(subscription_id)
            case = subscription.case

            case_text = (
                f'<b>📄 Номер дела:</b> <code>{case.number}</code>\n'
                f'<b>🏛 Суд:</b> {case.court.name if case.court else "<i>Не указан</i>"}\n'
                f'<b>👨‍⚖ Судья:</b> {case.judge.name if case.judge else "<i>Не указан</i>"}\n'
                f'<b>📅 Дата поступления:</b> <code>{case.date_of_receipt.strftime("%d.%m.%Y")}</code>\n\n'
                f"<a href='{case.url}'>🔗 Ссылка на дело</a>"
            )

            # Редактируем сообщение с деталями дела
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=case_text,
                parse_mode='HTML',
            )
            bot.answer_callback_query(call.id)

        except Exception as exc:
            logger.error('Ошибка при открытии дела', exc_info=exc)
            bot.answer_callback_query(call.id, '❌ Не удалось получить данные дела')
