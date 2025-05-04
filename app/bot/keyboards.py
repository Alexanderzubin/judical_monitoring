from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


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
	button1 = KeyboardButton('❌ Отмена')
	keyboard.add(button1)
	return keyboard

def generate_paginated_case_buttons(subscriptions, prefix, page_number):
	items_per_page = 3
	start_index = page_number * items_per_page
	end_index = start_index + items_per_page
	paginated_subs = subscriptions[start_index:end_index]

	markup = InlineKeyboardMarkup()

	# Кнопки дел
	for sub in paginated_subs:
		case_number = sub.cases.number
		markup.add(
			InlineKeyboardButton(
				text=case_number,
				callback_data=f'{prefix}_case_{sub.id}'
			)
		)

	# Кнопки пагинации
	pagination_buttons = []

	if start_index > 0:
		pagination_buttons.append(
			InlineKeyboardButton('⬅️ Предыдущая', callback_data=f'{prefix}_page_{page_number - 1}')
		)
	if end_index < len(subscriptions):
		pagination_buttons.append(
			InlineKeyboardButton('Следующая ➡️', callback_data=f'{prefix}_page_{page_number + 1}')
		)
	if pagination_buttons:
		markup.add(*pagination_buttons)

	markup.add(InlineKeyboardButton('❌ Отмена', callback_data='cancel'))
	return markup
