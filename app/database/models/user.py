from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from app.database.base import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = 'user'
    str_columns=('first_name','last_name','username')
    
    id = Column(Integer, autoincrement=True, primary_key=True, comment='идентификтор пользователя')
    tg_id = Column(BigInteger, unique=True, nullable=False, comment='индентификтор пользователя в telegram')
    first_name = Column(String(255), comment='имя пользователя')
    last_name = Column(String(255), comment='фамилия пользователя')
    username = Column(String(255), comment='логин пользователя в telegram')
    chat_id = Column(BigInteger, nullable=False, comment='идентификтор чата с пользователем')
    
  

    # relationship
    case_subscriptions = relationship('Case', secondary ='subscription')
    notifications = relationship('Notification', back_populates='user')
    events = relationship(
		'CaseEvent',
		secondary='notification',
	)
    