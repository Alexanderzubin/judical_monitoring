from sqlalchemy import Column, Integer, String
# from app.database.models.case import Case
from sqlalchemy.orm import relationship, Mapped
from app.database.base import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'user'
    
    id = Column(Integer, autoincrement=True, primary_key=True, comment='идентификтор пользователя')
    tg_id = Column(Integer, unique=True, comment='индентификтор пользователя в telegram')
    first_name = Column(String(255), comment='имя пользователя')
    last_name = Column(String(255), comment='фамилия пользователя')
    username = Column(String(255), comment='логин пользователя в telegram')
    chat_id = Column(Integer, comment='идентификтор чата с пользователем')
    
  

    # relationship
    case_subscriptions = relationship('Case', secondary ='subscription')
    notifications = relationship('Notification', back_populates='user')
    events = relationship(
		'CaseEvent',
		secondary='notification',
	)

    def __repr__(self):
	    return f'{self.id}, {self.first_name}, {self.last_name}'
