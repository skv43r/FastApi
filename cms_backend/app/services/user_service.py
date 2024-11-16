from sqlmodel import Session
from models import User

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def import_user(self, user_data: dict):
        user_id = user_data["id"]
        existing_user = self.session.get(User, user_id)

        if existing_user is None:
            user = User(
                id=user_id,
                name=user_data["name"],
                email=user_data["email"],
                avatar=user_data["avatar"],
            )
            self.session.add(user)
        else:
            existing_user.name = user_data["name"]
            existing_user.email = user_data["email"]
            existing_user.avatar = user_data["avatar"]