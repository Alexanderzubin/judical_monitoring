from sqlalchemy.orm import Session
from app.database.models.case import Case
from app.database.models.judge import Judge
from app.database.models.court import Court
from app.database.models.category import Category
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import date
from app.database.repositories.exceptions import CaseError


class CaseRepository:

    def __init__(self, session: Session, logger: logging.Logger):
       self.session = session
       self.logger = logger

    def create(
            self,
            number: str,
            unique_identifier: str,
            judge: Judge,
            date_of_receipt: date,
            url: str,
            court: Court,
            categories: list[Category]
        ) -> Case:

        try:
            new_case = Case(
                number=number,
                unique_identifier=unique_identifier,
                judge=judge,
                date_of_receipt=date_of_receipt,
                url=url,
                court=court,
                categories=categories
            )

            self.session.add(new_case)
            self.session.commit()
            return new_case
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating case: {exc}')
            raise CaseError('Ошибка создания дела')

    def update(self, case: Case) -> bool:
        
        try:
           self.session.query(Case).filter(Case.id == case.id).update(case.as_dict())
           self.session.commit()
           return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while updating case: {exc}')
            raise CaseError('Ошибка обновления дела')

    def get_by_id(self, case_id: int) -> Case | None:
        
        try:
            case = self.session.query(Case).filter(Case.id == case_id).first()
            return case
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get case by id: {exc}')
            raise CaseError('Ошибка получения дела по id')

    def get_by_url(self, url: str) -> Case | None:
        
        try:
            case = self.session.query(Case).filter(Case.url == url).first()
            return case
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get case by url: {exc}')
            raise CaseError('Ошибка получения дела по url')

    
    