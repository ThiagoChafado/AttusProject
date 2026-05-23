from fastapi import FastAPI

from database import Base, engine
from routes.client_routes import router as clients_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(clients_router)