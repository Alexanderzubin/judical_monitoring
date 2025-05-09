from sqlalchemy.orm import Session
from app.database.models.court import Court
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import CourtError


logger = logging.getLogger(__name__)


class CourtRepository:
    def __init__(self, session: Session):
        self.session = session
        self.logger = logger

    def create(self, name: str) -> Court:
        try:
            new_court = Court(name=name)
            self.session.add(new_court)
            self.session.commit()
            return new_court

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while creating court: {exc}')
            raise CourtError('Ошибка создания суда')

    def get_by_name(self, court_name: str) -> Court | None:
        try:
            court = self.session.query(Court).filter(Court.name == court_name).first()
            return court

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get court by name: {exc}')
            raise CourtError('Ошибка получения суда по наименованию')

    def get_or_create(self, court_name: str) -> Court:
        try:
            court = self.session.query(Court).filter(Court.name == court_name).first()
            if not court:
                court = self.create(court_name)

            return court
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get_or_create court by name: {exc}')
            raise CourtError('Ошибка создания или получения суда по наименованию')
