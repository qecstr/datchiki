from sqlalchemy.orm import Session
from app.models import Users as DB_Users
from app.models import Data as DB_Data
from app.schemas import Users
from app.schemas import SensorData
import datetime



def regiter(users:Users,db:Session):
    temp = DB_Users(
        login = users.login,
        password = users.password
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)

    return auth(users,db)

def auth(users:Users,db:Session):
    temp = db.query(DB_Users).filter(DB_Users.login == users.login,DB_Users.password == users.password).first()
    if temp is None:
        return False
    else:
        return True

def insertData(data:SensorData,db:Session):
    temp = DB_Data(
        time = datetime.datetime.now(),
        temperature = data.temperature,
        humidity = data.humidity
    )
    db.add(temp)
    db.commit()
    db.refresh(temp)