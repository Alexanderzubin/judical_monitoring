from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Category(Base):
    """Модель категорий судебных дел"""
    __tablename__ = 'category'
    str_columns = ('name',)
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификатор категории дела')
    name = Column(String(1024), unique=True, nullable=False, comment='наименование категории дела')

    # relationship
    cases = relationship(
        'Case',
        secondary='case_category',
        back_populates='categories'
    )
    