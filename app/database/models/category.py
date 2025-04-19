from sqlalchemy import Column, Integer, String
from  sqlalchemy.orm import relationship

from app.database.base import Base


class Category(Base):
    __tablename__ = 'category'
    
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True, comment='идентификтор категории дела')
    name = Column(String(1024), unique=True, comment='наименование категории дела')

    case_categories = relationship('CaseCategory', back_populates='category')

    cases = relationship(
        'Case',
        secondary='case_category',
        back_populates='categories'
    )
    


    
