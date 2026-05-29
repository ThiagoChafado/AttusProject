from fastapi import FastAPI

from database import Base, engine
from routes.client_routes import router as clients_router
from routes.webhook_routes import router as webhooks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundo Invest — Client Management API")

app.include_router(clients_router)
app.include_router(webhooks_router)