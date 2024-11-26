from fastapi import HTTPException
from sqlmodel import Session
from models import User
from user_service import UserService

class UserController:
    def __init__(self, session: Session) -> None:
        self.user_service = UserService(session)
    
    async def add_user(self, user: User) -> dict:
        try:
            created_user = self.user_service.add_user(user)
            return {"message": "User added successfully", "user": created_user}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def delete_user(self, user_id: int) -> dict:
        try:
            self.user_service.delete_user(user_id)
            return {"message": "User deleted successfully", "user_id": user_id}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def edit_user(self, user_id: int, user_data: User) -> dict:
        try:
            updated_user = self.user_service.edit_user(user_id, user_data)
            return {"message": "User updated successfully", "user": updated_user}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    async def return_users(self) -> dict:
        try:
            users = self.user_service.get_all_users()
            user_data = [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "avatar": user.avatar
                } 
                for user in users
            ]
            return {"users": user_data}
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))