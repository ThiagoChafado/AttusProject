from fastapi import HTTPException

from models.client import Client

from repositories.client_repository import (
    ClientRepository
)

from integrations.pipefy_client import (
    PipefyClient
)


class ClientService:

    def __init__(self, db):

        self.repository = ClientRepository(db)

        self.pipefy_client = PipefyClient()

    def create_client(self, payload):

        existing_client = self.repository.get_by_email(
            payload.cliente_email
        )

        if existing_client:

            raise HTTPException(
                status_code=409,
                detail="Cliente já cadastrado"
            )

        client = Client(
            cliente_nome=payload.cliente_nome,
            cliente_email=payload.cliente_email,
            tipo_solicitacao=payload.tipo_solicitacao,
            valor_patrimonio=payload.valor_patrimonio,
        )

        created_client = self.repository.create(client)

        graphql_payload = (
            self.pipefy_client
            .build_create_card_payload(created_client)
        )

        print("\nGRAPHQL PAYLOAD:")
        print(graphql_payload)

        return created_client