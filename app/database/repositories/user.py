from sqlalchemy.orm import Session
from app.database.models.user import User
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.database.repositories.exceptions import UserError

class UserRepository:

    def __init__(self, session: Session, logger: logging.Logger):
       self.session = session
       self.logger = logger

    def create(
        self, tg_id: int,
        first_name: str,
        last_name: str,
        user_name: str,
        chat_id: int
    ) -> User:
 
        try:
            new_user = User(
                tg_id=tg_id,
                first_name=first_name,
                last_name=last_name,
                user_name=user_name,
                chat_id=chat_id
            )
            self.session.add(new_user)
            self.session.commit()
            return new_user
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while creating user: {exc}')
            raise UserError('Ошибка создания пользователя')
        
    def delete(self, user_id: int) -> bool:
       
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                return True
       
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while deleting user: {exc}')
            raise UserError('Ошибка удаления пользователя')
        
    def get_by_tg_id(self, tg_id: int) -> User | None:

        try:
            user = self.session.query(User).filter(User.tg_id == tg_id).first()
            return user
        
        except SQLAlchemyError as exc:
            self.session.rollback()
            self.logger.error(f'Database error while get user by tg id: {exc}')
            raise UserError('Ошибка получения пользователя по tg id')

