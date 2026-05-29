from pydantic import BaseModel, EmailStr, Field


class WebhookPayload(BaseModel):
    event_id: str = Field(..., min_length=1)  # event_id não pode ser vazio
    card_id: str
    cliente_email: EmailStr
    timestamp: str