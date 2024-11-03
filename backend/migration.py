from sqlalchemy import create_engine
from sqlmodel import Session, select
from models import User

sqlite_engine = create_engine("sqlite:///users.db")
postgres_engine = create_engine(f"postgresql://postgres:Worldof123@postgres:5432/Users")

def migrate_data():
    with Session(sqlite_engine) as sqlite_session:
        users = sqlite_session.exec(select(User)).all()

    with Session(postgres_engine) as pg_session:
        for user in users:
            new_user = User(
                name=user.name,
                email=user.email,
                avatar=user.avatar
            )
            pg_session.add(new_user)
        pg_session.commit()

def check_migrated_data():
    with Session(postgres_engine) as pg_session:
        users = pg_session.exec(select(User)).all()
        print("Users in PostgreSQL database:")
        for user in users:
            print(user)

if __name__ == "__main__":
    migrate_data()