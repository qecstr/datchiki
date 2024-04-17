import asyncio
import datetime
import json
from typing import Annotated

from fastapi import  WebSocket
from starlette.websockets import WebSocketDisconnect

from app.models import Data
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, event

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

                await connection.send_json(DTOtoJson(data))

manager = ConnectionManager()
@router.websocket("/getData")
async def websocket_endpoint(websocket: WebSocket,db:db_dependency):
    await manager.connect(websocket)
    listOfSensors = db.query(Data).all()
    try:
        for sensor in listOfSensors:

            await manager.broadcast(DTO(sensor))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@event.listens_for(Data, "after_insert")
async def after_data_insert(mapper, connection, target):
    new_data = target
    print(DTOtoJson(DTO(new_data)))

    await asyncio.sleep(1)
    await manager.broadcast(DTO(new_data))
def DTO(data:Data):
    temp = SensorData(
                    temperature=data.temperature,
                    humidity=data.humidity,
                    CO2=data.CO2,
                    time=data.time
                )
    return temp
def DTOtoJson(data: SensorData):
    temp = json.dumps({
        "temperature": data.temperature,
        "humidity": data.humidity,
        "CO2": data.CO2,
        "time": data.time
    }
    )
    return temp

@router.post("/postData")
async def postData(sensor_data: SensorData,db:db_dependency):
    print("Received sensor value:", sensor_data)
    temp = insertData(sensor_data,db)
    await after_data_insert(None, None, temp)
