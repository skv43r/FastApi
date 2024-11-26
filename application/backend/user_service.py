from sqlmodel import Session, select
from models import User
from fastapi import HTTPException

class UserService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_user(self, user: User) -> User:
        try:
            if not user.name or not user.email:
                raise HTTPException(status_code=400,
                                    detail="Name and email are required")
            
            existing_user = self.session.get(User, user.id) if user.id else None
            if existing_user:
                    raise HTTPException(status_code=400,
                                        detail="User with this ID already exists")
            
            existing_email = self.session.exec(
                select(User).where(User.email == user.email)
            ).first()
            if existing_email:
                raise HTTPException(status_code=400,
                                    detail="User with this email already exists")
            
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception as e:
             self.session.rollback()
             raise e
    
    def delete_user(self, user_id: int) -> None:
        try:
            user = self.session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            self.session.delete(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
    def edit_user(self, user_id: int, user_data: User) -> User:
        try:
            user = self.session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User  not found")
            
            user.name = user_data.name
            user.email = user_data.email
            user.avatar = user_data.avatar

            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise e
    def get_all_users(self) -> list[User]:
        try:
            return self.session.exec(select(User)).all()
        except Exception as e:
            raise e
