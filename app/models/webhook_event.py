from sqlalchemy import Column, Integer, String

from database import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, unique=True, nullable=False, index=True)
    card_id = Column(String, nullable=False)
    cliente_email = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)