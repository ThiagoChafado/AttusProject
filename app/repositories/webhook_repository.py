from sqlalchemy.orm import Session

from models.webhook_event import WebhookEvent


class WebhookRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_event_id(self, event_id: str):
        return (
            self.db.query(WebhookEvent)
            .filter(WebhookEvent.event_id == event_id)
            .first()
        )

    def create(self, event: WebhookEvent):
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event