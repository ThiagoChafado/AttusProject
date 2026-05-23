from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database import get_db

from schemas.client_schema import ClientCreate

from services.client_service import (
    ClientService
)

router = APIRouter()


@router.post("/clientes", status_code=201)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db)
):

    service = ClientService(db)

    client = service.create_client(payload)

    return {
        "id": client.id,
        "cliente_nome": client.cliente_nome,
        "cliente_email": client.cliente_email,
        "tipo_solicitacao": client.tipo_solicitacao,
        "valor_patrimonio": client.valor_patrimonio
    }