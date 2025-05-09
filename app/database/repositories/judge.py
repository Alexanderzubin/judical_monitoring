import logging

from sqlalchemy.orm import Session
from app.database.models.judge import Judge
from sqlalchemy.exc import SQLAlchemyError
from app.database.repositories.exceptions import JudgeError

logger = logging.getLogger(__name__)


class JudgeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, name: str) -> Judge:
        try:
            new_judge = Judge(name=name)
            self.session.add(new_judge)
            self.session.commit()
            return new_judge

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while creating judge: {exc}')
            raise JudgeError('Ошибка создания судьи')

    def get_by_name(self, judge_name: str) -> Judge | None:
        try:
            judge = self.session.query(Judge).filter(Judge.name == judge_name).first()
            return judge

        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get judge by name: {exc}')
            raise JudgeError('Ошибка получения судьи по ФИО')

    def get_or_create(self, judge_name: str) -> Judge:
        try:
            judge = self.session.query(Judge).filter(Judge.name == judge_name).first()
            if not judge:
                judge = self.create(judge_name)

            return judge
        except SQLAlchemyError as exc:
            self.session.rollback()
            logger.error(f'Database error while get_or_create judge by name: {exc}')
            raise JudgeError('Ошибка создания или получения судьи по ФИО')
