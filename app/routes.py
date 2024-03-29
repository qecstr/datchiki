from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from starlette import status
from app.schemas import SensorData

from app.schemas import Users, Response
from app.database import SessionLocal
from app.crud import regiter,auth,insertData
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]



@router.post("/users/reg")
async def registerUser(users:Users,db:db_dependency):
    if regiter(users,db):
        return Response(
            type = "",
            status = status.HTTP_201_CREATED,
            code = "201",
            message = "User created"
        ).dict(exclude_none = True)
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error, please contact with server"
        )


@router.post("/users/auth")
async def authUser(users:Users,db:db_dependency):
    if auth(users,db) is None:
        return   HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User Unauthorized",
    )
    else:
        return Response(
            status_code = status.HTTP_202_ACCEPTED,
            detail = "User authorized"
                        )


@router.get("/getData/")
async def getData():
    return

@router.post("/postData")
async def postData(sensor_data: SensorData,db:db_dependency):
    print("Received sensor value:", sensor_data)
    insertData(sensor_data,db)
