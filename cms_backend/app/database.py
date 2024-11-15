from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = f"postgresql://postgres:Worldof123@postgres:5432/Users"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
