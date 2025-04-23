from sqlalchemy.orm import Session
from app.database.models.category import Category
from typing import Callable, TypeAlias
from sqlalchemy.exc import SQLAlchemyError
import logging

SessionFactory: TypeAlias = Callable[[], Session]


class CategoryRepository:

    def __init__(self, session: SessionFactory, logger: logging.Logger):
       self.session = session()
       self.logger = logger

    def __del__(self):
        self.session.close()

    def create(self, name: str) -> Category | None:
 
        try:
            new_category = Category(name=name)
            self.session.add(new_category)
            self.session.commit()
            return new_category
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating judge: {exc}')
        
    def update(self, category: Category) -> Category | None:
        
        try:
           self.session.query(Category).filter(Category.id == category.id).update(category.as_dict())
           self.session.commit()
           return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while updating category: {exc}')

