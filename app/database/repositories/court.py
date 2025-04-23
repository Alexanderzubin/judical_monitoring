from sqlalchemy.orm import Session
from app.database.models.court import Court
from typing import Callable, TypeAlias
from sqlalchemy.exc import SQLAlchemyError
import logging

SessionFactory: TypeAlias = Callable[[], Session]


class Courtepository:

    def __init__(self, session: SessionFactory, logger: logging.Logger):
       self.session = session()
       self.logger = logger

    def __del__(self):
        self.session.close()

    def create(self, name: str) -> Court | None:
 
        try:
            new_court = Court(name=name)
            self.session.add(new_court)
            self.session.commit()
            return new_court
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating court: {exc}')
        
    def get_by_name(self, court_name: str) -> Court | None:

        try:
            court = self.session.query(Court).filter(Court.name == court_name).first()
            return court
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get court by name: {exc}')

