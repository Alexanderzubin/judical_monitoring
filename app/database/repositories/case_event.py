import datetime

from sqlalchemy.orm import Session
from app.database.models.case_event import CaseEvent
from app.database.models.case import Case
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import CaseEventError
from app.parser.types import ParsedCaseEventData

logger = logging.getLogger(__name__)


class CaseEventRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        case: Case,
        parsed_event: ParsedCaseEventData,
    ) -> CaseEvent:
        try:
            new_event = CaseEvent(
                name=parsed_event['event_name'],
                date=parsed_event['date'],
                time=parsed_event['time'],
                result=parsed_event['result'],
                the_basic_for_the_selected_result=parsed_event['reason'],
                date_of_placement=parsed_event['placement_date'],
                case=case,
            )
            self.session.add(new_event)
            self.session.commit()
            return new_event

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while creating case event: {exc}')
            raise CaseEventError('Ошибка создания события')

    def update(self, case_event: CaseEvent) -> bool:
        try:
            self.session.query(CaseEvent).filter(CaseEvent.id == case_event.id).update(
                case_event.as_dict()
            )
            self.session.commit()
            return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while updating case event: {exc}')
            raise CaseEventError('Ошибка обновления события')

    def get_by_id(self, event_id):
        try:
            event = self.session.query(CaseEvent).filter(CaseEvent.id == event_id).first()
            return event

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get event by id: {exc}')
            raise CaseEventError('Ошибка получения события по id')
