from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.webhook_schema import WebhookPayload
from services.webhook_service import WebhookService

router = APIRouter()


@router.post("/webhooks/pipefy/card-updated", status_code=200)
def card_updated(
    payload: WebhookPayload,
    db: Session = Depends(get_db)
):
    service = WebhookService(db)
    return service.process_card_updated(payload)