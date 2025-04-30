from sqlalchemy.orm import Session
from app.database.models.category import Category
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import CategoryError

class CategoryRepository:

    def __init__(self, session: Session, logger: logging.Logger):
       self.session = session
       self.logger = logger

    def create(self, name: str) -> Category:
 
        try:
            new_category = Category(name=name)
            self.session.add(new_category)
            self.session.commit()
            return new_category
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating judge: {exc}')
            raise CategoryError('Ошибка создания категории')
   
    def update(self, category: Category) -> bool:
        
        try:
           self.session.query(Category).filter(Category.id == category.id).update(category.as_dict())
           self.session.commit()
           return True

        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while updating category: {exc}')
            raise CategoryError('Ошибка обновления категории')

    def get_category_by_name(self, category_name: str) -> Category | None:

        try:
            category = self.session.query(Category).filter(Category.name == category_name).first()
            return category

        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get category by name category: {exc}')
            raise CategoryError('Ошибка получения категории по наименованию')