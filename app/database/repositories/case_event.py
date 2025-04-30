from sqlalchemy.orm import Session
from app.database.models.case_event import CaseEvent
from app.database.models.case import Case
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import date, time
from app.database.repositories.exceptions import CaseEventError


class CaseEventRepository():

    def __init__(self, session: Session, logger: logging.Logger):
        self.session = session
        self.logger = logger

    def create(
        self,
        name: str,
        date: date,
        time: time,
        result: str,
        the_basic_for_the_selected_result: str,
        date_of_placement: date,
        case: Case
    ) -> CaseEvent:

        try:
            new_event = CaseEvent(
                name=name,
                date=date,
                time=time,
                result=result,
                the_basic_for_the_selected_result=the_basic_for_the_selected_result,
                date_of_placement=date_of_placement,
                case=case
            )
            self.session.add(new_event)
            self.session.commit()
            return new_event
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating case event: {exc}')
            raise CaseEventError('Ошибка создания события')

    def update(self, case_event: CaseEvent) -> bool:
        
        try:
           self.session.query(CaseEvent).filter(CaseEvent.id == case_event.id).update(case_event.as_dict())
           self.session.commit()
           return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while updating case event: {exc}')
            raise CaseEventError('Ошибка обновления события')



