from sqlalchemy.orm import Session
from app.database.models.judge import Judge
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import JudgeError

class JudgeRepository:

    def __init__(self, session: Session, logger: logging.Logger):
       self.session = session
       self.logger = logger

    def create(self, name: str) -> Judge:
 
        try:
            new_judge = Judge(name=name)
            self.session.add(new_judge)
            self.session.commit()
            return new_judge
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating judge: {exc}')
            raise JudgeError('Ошибка создания судьи')
        
    def get_by_name(self, judge_name: str) -> Judge | None:

        try:
            judge = self.session.query(Judge).filter(Judge.name == judge_name).first()
            return judge
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get judge by name: {exc}')
            raise JudgeError('Ошибка получения судьи по ФИО')

