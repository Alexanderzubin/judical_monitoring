from sqlalchemy.orm import Session
from app.database.models.case_category import CaseCategory
from typing import Callable, TypeAlias
from sqlalchemy.exc import SQLAlchemyError
import logging

SessionFactory: TypeAlias = Callable[[], Session]


class UserRepository:

    def __init__(self, session: SessionFactory, logger: logging.Logger):
       self.session = session()
       self.logger = logger

    def __del__(self):
        self.session.close()

    def create(self, category_id: int, case_id: int) -> CaseCategory:
        
        try:
            if self.exists(category_id, case_id):
                raise ValueError('Связь между делом и категорией уже существует')
            
            case_category = CaseCategory(category_id=category_id, case_id=case_id)
            self.session.add(case_category)
            self.session.commit()
            return case_category
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating case category: {exc}')
    
    