from sqlalchemy.orm import Session
from app.database.models.judge import Judge
from typing import Callable, TypeAlias
from sqlalchemy.exc import SQLAlchemyError
import logging

SessionFactory: TypeAlias = Callable[[], Session]


class JudgeRepository:

    def __init__(self, session: SessionFactory, logger: logging.Logger):
       self.session = session()
       self.logger = logger

    def __del__(self):
        self.session.close()

    def create(self, name: str) -> Judge | None:
 
        try:
            new_judge = Judge(name=name)
            self.session.add(new_judge)
            self.session.commit()
            return new_judge
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating judge: {exc}')
        
    def get_by_name(self, judge_name: str) -> Judge | None:

        try:
            judge = self.session.query(Judge).filter(Judge.name == judge_name).first()
            return judge
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get judge by name: {exc}')

