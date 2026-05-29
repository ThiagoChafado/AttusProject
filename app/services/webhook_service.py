from fastapi import HTTPException

from models.webhook_event import WebhookEvent
from repositories.client_repository import ClientRepository
from repositories.webhook_repository import WebhookRepository
from integrations.pipefy_client import PipefyClient

PRIORITY_THRESHOLD = 200_000


def _calculate_priority(valor_patrimonio: float) -> str:
    if valor_patrimonio >= PRIORITY_THRESHOLD:
        return "prioridade_alta"
    return "prioridade_normal"


class WebhookService:

    def __init__(self, db):
        self.client_repo = ClientRepository(db)
        self.webhook_repo = WebhookRepository(db)
        self.pipefy_client = PipefyClient()
        self.db = db

    def process_card_updated(self, payload):
        # rejeita se ja foi processado anteriormente
        existing_event = self.webhook_repo.get_by_event_id(payload.event_id)
        if existing_event:
            raise HTTPException(
                status_code=409,
                detail=f"Evento '{payload.event_id}' já foi processado."
            )

        # pega por email
        client = self.client_repo.get_by_email(payload.cliente_email)
        if not client:
            raise HTTPException(
                status_code=404,
                detail=f"Cliente com e-mail '{payload.cliente_email}' não encontrado."
            )

        # calculo de status
        prioridade = _calculate_priority(client.valor_patrimonio)

        # faz as chamadas (SIMULACAO)
        status_payload = self.pipefy_client.build_update_status_payload(
            card_id=payload.card_id,
            status="Processado"
        )
        priority_payload = self.pipefy_client.build_update_priority_payload(
            card_id=payload.card_id,
            prioridade=prioridade
        )

        print("\nGRAPHQL PAYLOAD — status update:")
        print(status_payload)
        print("\nGRAPHQL PAYLOAD — priority update:")
        print(priority_payload)

        # atualiza no db
        client.status = "Processado"
        client.prioridade = prioridade
        self.db.commit()
        self.db.refresh(client)

        # registra evento para idempotencia
        event = WebhookEvent(
            event_id=payload.event_id,
            card_id=payload.card_id,
            cliente_email=payload.cliente_email,
            timestamp=payload.timestamp,
        )
        self.webhook_repo.create(event)

        return {
            "event_id": payload.event_id,
            "cliente_email": client.cliente_email,
            "status": client.status,
            "prioridade": client.prioridade,
        }