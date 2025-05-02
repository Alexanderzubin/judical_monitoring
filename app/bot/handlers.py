from telebot import TeleBot
from app.database.repositories.user import UserRepository
from app.database.repositories.subscription import SubscriptionRepository
from app.database.repositories.case import CaseRepository
from app.database.session import Session

from app.bot.keyboards import main_menu, cases_menu, cancel_menu
from app.bot.utils import is_valid_url

import logging

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

session = Session()

repo_user = UserRepository(session=session, logger=logger)
repo_case = CaseRepository(session=session, logger=logger)
repo_subscription = SubscriptionRepository(session=session, logger=logger)


def setup_handlers(bot: TeleBot):
	@bot.message_handler(commands=['start'])

	def send_welcome(message):
		try:
			tg_id = message.from_user.id
			user = repo_user.get_by_tg_id(tg_id=tg_id)
			if user:
				welcome_text = (
					f"<b>Привет, {user.first_name}!</b>\n\n"
					"<i>Рад видеть тебя снова!</i> Я помогу отслеживать твои судебные дела. "
					"Выбери действие в меню ниже:"
				)
				bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=main_menu())
			else:
				repo_user.create(
					tg_id=tg_id,
					first_name=message.from_user.first_name,
					last_name=message.from_user.last_name,
					username=message.from_user.username,
					chat_id=message.chat.id
				)
				welcome_text = (
					f"<b>Добро пожаловать, {message.from_user.first_name}!</b>\n\n"
					"<i>Я твой помощник по отслеживанию судебных дел.</i> "
					"Подписывайся на дела, следи за их статусами и управляй подписками. "
					"Начнём? Выбери действие в меню:"
				)
				bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=main_menu())
		except Exception as e:
			logger.error(f'Ошибка в send_welcome: {e}')
			bot.send_message(
				message.chat.id, 'Произошла ошибка при обработке запроса.\nПопробуйте позже',
				parse_mode='HTML'
			)

	@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
	def help_command(message):
		help_text = (
			"<b>📖 Инструкция по использованию бота:</b>\n\n"
			"1. <b>Мои дела</b> — работа с судебными делами:\n"
			"   - <i>Подписаться на дело</i>: Введи ссылку на дело.\n"
			"   - <i>Список моих дел</i>: Посмотри все дела, на которые ты подписан.\n"
			"   - <i>Отписаться от дела</i>: Удали дело из подписок.\n\n"
			"2. <b>О боте</b> — информация о боте и контакты поддержки.\n\n"
			"Если что-то не работает, напиши в <a href='https://t.me/YourSupport'>поддержку</a>"
		)
		bot.reply_to(message, help_text, parse_mode='HTML', reply_markup=main_menu())

	@bot.message_handler(func=lambda message: message.text == 'ℹ️ О боте')
	def about_command(message):
		about_text = (
			"<b>О боте:</b>\n\n"
			"Я бот для отслеживания судебных дел. Помогу следить за статусами дел по вашим ссылкам.\n\n"
			"<b>Версия:</b> 1.0"
		)
		bot.reply_to(message, about_text, parse_mode='HTML', reply_markup=main_menu())

	@bot.message_handler(func=lambda message: message.text == '📋 Мои дела')
	def my_cases(message):
		bot.reply_to(message, 'Выберите действие:', reply_markup=cases_menu())

	@bot.message_handler(func=lambda message: message.text == '📝 Подписаться на дело')
	def subscribe_to_case(message):
		bot.reply_to(
			message, "📝 Пожалуйста, пришли ссылку на дело, на которое хочешь подписаться.\n\n"
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

			case = repo_case.get_by_url(url)
			if case:
				user_id = repo_user.get_by_tg_id(message.chat.id)
				existing_subscription = repo_subscription.get_by_user_and_case(user_id.id, case.id)
				if existing_subscription:
					bot.send_message(
						message.chat.id,
						"🔔 Вы уже подписаны на это дело.",
						reply_markup=cases_menu()
					)
					return
			else:
				bot.send_message(message.chat.id, 'дело еще не добавлено в бд', reply_markup=cases_menu())
		except Exception as e:
			logger.error('Дело еще не создано проверьте бд {e}')
			bot.send_message(
				message.chat.id, 'Произошла ошибка при обработке запроса.\nПопробуйте позже',
				parse_mode='HTML'
			)

	# Логика запуска парсера и добавление дела в бд

	@bot.message_handler(func=lambda message: message.text == '⬅️ Назад')
	def back_to_main(message):
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
