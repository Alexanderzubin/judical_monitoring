from sqlalchemy.orm import Session
from app.database.models.user import User
from typing import Callable, TypeAlias

SessionFactory: TypeAlias = Callable[[], Session]

class UserRepository:

    def __init__(self, session: SessionFactory):
       self.session = session()

    def __del__(self):
        self.session.close()


    def create_user(self, tg_id: int, first_name: str, last_name: str,
        user_name: str, chat_id: int) -> User:
        
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

    
    def delete_user(self, user_id: int) -> bool:
       
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    
    
    def get_user(self, user_id: int) -> User | None:

        user = self.session.query(User).filter(User.id == user_id).first()
        return user
        
        
    
    


    


    


    


        












    def get_user(self, user_id: int) -> User | None:
        """Получить пользователя по ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    

    
repa=UserRepository()
get=repa.get_user(1)
print(get)
