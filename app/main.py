from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.routes import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['GET','POST','DELETE'],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="", tags=[""])