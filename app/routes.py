import asyncio
import datetime
from typing import Annotated

from fastapi import  WebSocket
from app.models import Data
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

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



class ConnectionManager:
        def __init__(self):
            self.active_connections: list[WebSocket] = []

        async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)

        def disconnect(self, websocket: WebSocket):
            self.active_connections.remove(websocket)


        async def broadcast(self,data:SensorData):
            for connection in self.active_connections:
                await connection.send_json(data)

manager = ConnectionManager()
@router.websocket("/getData")
async def websocket_endpoint(websocket: WebSocket,db:db_dependency):
    await manager.connect(websocket)

    while True:
        query = db.query(Data).all().pop(0)
        data = SensorData(
            temperature = query.temperature,
            humidity = query.humidity,
            CO2 = query.CO2,
            time = query.time
        )
        await manager.broadcast(data)
        while query is None:
            async with db as session:
                result = await session.execute(select(Data))
                items = result.scalars().all()
                data = SensorData(
                    temperature=items.temperature,
                    humidity=items.humidity,
                    CO2=items.CO2,
                    time=items.time
                )
                await manager.broadcast(data)


        await asyncio.sleep(1)


@router.post("/postData")
async def postData(sensor_data: SensorData,db:db_dependency):
    print("Received sensor value:", sensor_data)
    insertData(sensor_data,db)
