from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlmodel import create_engine
from backend.models import User

app = Flask(__name__)
app.secret_key = "supersecret"
engine = create_engine("postgresql://postgres:Worldof123@localhost:5432/Users")
SessionLocal = scoped_session(sessionmaker(bind=engine))

admin = Admin(app, name="Administrator", template_mode="bootstrap3")

class UserAdminView(ModelView):
    can_create = True
    can_delete = True
    can_edit = True
    can_view_details = True

    column_list = ('id', 'name', 'email', 'avatar')
    form_columns = ('name', 'email', 'avatar')
    



admin.add_view(UserAdminView(User, SessionLocal))

if __name__ == "__main__":
    app.run(port=5000)