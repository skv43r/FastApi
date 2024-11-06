from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jwt import ExpiredSignatureError, DecodeError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

DATABASE_URL = f"postgresql://postgres:Worldof123@postgres:5432/Users"
SECRET_KEY = "pass"
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL, echo=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(seconds=10)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification failed: {str(e)}")