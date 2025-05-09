import logging

from app.celery import app
from app.database.session import Session
from app.services.cases import CaseService
from app.tasks import async_notify_on_case_event
from app.settings import settings

logger = logging.getLogger(__name__)


@app.task
def async_update_case(case_id: int) -> None:
    logger.info(f'Update case {case_id}')

    with Session() as session:
        case_service = CaseService.get_service(session)
        case = case_service.find_case_by_id(case_id)

        new_events = case_service.check_case_for_updates(case)
        if new_events:
            logger.info(f'Process new events for case {case.id}')

            for event in new_events:
                if event.days_since_event < settings.max_days_since_event_for_notification:
                    async_notify_on_case_event.delay(event.id)

        logger.info(f'Case {case.id} updated')
