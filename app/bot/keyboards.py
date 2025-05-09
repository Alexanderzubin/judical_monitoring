from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from app.database.models import Subscription


def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = KeyboardButton('📋 Мои дела')
    button2 = KeyboardButton('❓ Помощь')
    button3 = KeyboardButton('ℹ️ О боте')
    keyboard.add(button1)
    keyboard.add(button2, button3)
    return keyboard


def cases_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = KeyboardButton('📝 Подписаться на дело')
    button2 = KeyboardButton('📑 Список моих дел')
    button3 = KeyboardButton('🗑️ Отписаться от дела')
    button4 = KeyboardButton('⬅️ Назад')
    keyboard.add(button1, button2)
    keyboard.add(button3, button4)
    return keyboard


def cancel_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = KeyboardButton('⬅️ Назад')
    keyboard.add(button1)
    return keyboard


def generate_paginated_case_buttons(
    subscriptions_page: list[Subscription],
    total_subscriptions_count: int,
    prefix: str,
    page_number: int,
    items_per_page: int,
):
    start_index = page_number * items_per_page
    end_index = start_index + items_per_page

    markup = InlineKeyboardMarkup()

    # Кнопки дел
    for sub in subscriptions_page:
        case_number = sub.case.number
        markup.add(InlineKeyboardButton(text=case_number, callback_data=f'{prefix}_case_{sub.id}'))

    # Кнопки пагинации
    pagination_buttons = []

    if start_index > 0:
        pagination_buttons.append(
            InlineKeyboardButton('⬅️ Предыдущая', callback_data=f'{prefix}_page_{page_number - 1}')
        )
    if end_index < total_subscriptions_count:
        pagination_buttons.append(
            InlineKeyboardButton('Следующая ➡️', callback_data=f'{prefix}_page_{page_number + 1}')
        )
    if pagination_buttons:
        markup.add(*pagination_buttons)

    return markup
