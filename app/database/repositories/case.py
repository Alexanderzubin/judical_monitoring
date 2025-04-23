from sqlalchemy.orm import Session
from app.database.models.case import Case
from typing import Callable, TypeAlias
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import date

SessionFactory: TypeAlias = Callable[[], Session]


class CaseRepository:

    def __init__(self, session: SessionFactory, logger: logging.Logger):
       self.session = session()
       self.logger = logger

    def __del__(self):
        self.session.close()

    def create(
            self,
            number: str,
            unique_identifier: str,
            judge_id: int,
            name_of_the_court: str,
            date_of_receipt: date,
            url: str,
            court_id: int
        ) -> Case | None:

        try:
            new_case = Case(
                number=number,
                unique_identifier=unique_identifier,
                judge_id=judge_id,
                name_of_the_court=name_of_the_court,
                date_of_receipt=date_of_receipt,
                url=url,
                court_id=court_id
            )

            self.session.add(new_case)
            self.session.commit()
            return new_case
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating case: {exc}')

    def update(self, case: Case) -> Case | None:
        
        try:
           self.session.query(Case).filter(Case.id == case.id).update(case.as_dict())
           self.session.commit()
           return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while updating case: {exc}')

    def get_by_id(self, case_id: int) -> Case | None:
        
        try:
            case = self.session.query(Case).filter(Case.id == case_id).first()
            return case
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get case by id: {exc}')

    def get_by_url(self, url: str) -> Case | None:
        
        try:
            case = self.session.query(Case).filter(Case.url == url).first()
            return case
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get case by url: {exc}')

    
    