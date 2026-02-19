from fastapi import FastAPI
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth.authentication import router as auth_router
from .config import settings



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello Iron Vault"}

