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

def generate_unsubscribe_buttons(subscriptions):
    markup = InlineKeyboardMarkup()
    for sub in subscriptions:
        case_number = sub.cases.number
        button = InlineKeyboardButton(
            text=case_number,
            callback_data=f'unsubscribe_{sub.id}'
        )
        markup.add(button)
    return markup