from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session, select
from database import db
from models import User
from services.data_service import DataService
from services.user_service import UserService

SessionDep = Annotated[Session, Depends(db.get_session)]
API_URL = "https://api.npoint.io/88fcfcbf4fde970ba6f2"
router = APIRouter()


@router.get("/api/cms/external-data")
async def get_external_data():
    data_service = DataService(API_URL)
    try:
        data = await data_service.fetch_data()
        await data_service.save_json(data)

        for user in data["users"]:
            file_name = f"user_{user['id']}.jpg"
            await data_service.download_image(user["avatar"], file_name)

        return {"message": "Data fetched and images saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            

@router.get("/api/cms/import-users")
async def import_users(session: SessionDep):
    data_service = DataService(API_URL)
    user_service = UserService(session)
    try:
        data = await data_service.fetch_data()

        for user_data in data["users"]:
            user_service.import_user(user_data)
            file_name = f"user_{user_data['id']}.jpg"
            await data_service.download_image(user_data["avatar"], file_name)
        session.commit()

        return {"message": "Users imported successfully"}
    except Exception as e:
            return {"error": str(e)}

@router.get("/api/cms/users/")
async def read_users(session: SessionDep):
    users = session.exec(select(User)).all()
    return users

    
