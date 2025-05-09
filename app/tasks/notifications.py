import logging

from app.bot import bot
from app.celery import app
from app.database.models import Case
from app.database.session import Session
from app.services.events import CaseEventService
from app.services.notifications import NotificationService
from app.services.subscriptions import SubscriptionService

logger = logging.getLogger(__name__)


@app.task
def async_notify_on_case_event(case_event_id: int) -> None:
    with Session() as session:
        subscription_service = SubscriptionService.get_service(session)
        case_event_service = CaseEventService.get_service(session)
        notification_service = NotificationService.get_service(session)

        case_event = case_event_service.find_event_by_id(case_event_id)
        case: Case = case_event.case

        for user in subscription_service.get_case_subscribers(case):
            _, notification_created = notification_service.get_or_create_notification(
                user, case_event
            )

            if notification_created:
                event_details = [
                    f'<b>Наименование события</b>: {case_event.name}',
                    f'<b>Дата и время</b>: {case_event.occurred_at.strftime("%d.%m.%Y %H:%S")}',
                ]

                if case_event.result:
                    event_details.append(
                        f'<b>Результат события</b>: {case_event.result}'
                    )

                if case_event.the_basic_for_the_selected_result:
                    event_details.append(
                        f'<b>Основание для выбранного результата события</b>: '
                        f'{case_event.the_basic_for_the_selected_result}'
                    )

                notification_text = (
                    f'⚡ Новая информация по делу <a href="{case.url}">{case.number}</a>\n\n'
                )

                notification_text = notification_text + '\n'.join(event_details)

                bot.send_message(
                    chat_id=user.tg_id,
                    text=notification_text,
                    parse_mode='HTML',
                )
