

from starlette import status
from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel



T = TypeVar('T')
class Response(GenericModel, Generic[T]):
    code: str
    status: int
    message: str
    result: Optional[T]

class Users(BaseModel):
    login: str
    password: str

class SensorData(BaseModel):
    temperature: float
    humidity: float
    CO2: float