import logging

from app.celery import app
from app.database.session import Session
from app.services.cases import CaseService
from app.tasks.cases import async_update_case

logger = logging.getLogger(__name__)


@app.task
def async_update_all_cases() -> None:
    logger.info('Async update cases')

    with Session() as session:
        case_service = CaseService.get_service(session)

        for case in case_service.get_cases_for_sync():
            async_update_case.delay(case.id)
            logger.info(f'Enqueue async update for case {case.id}')

    logger.info('Async cases update processed')
