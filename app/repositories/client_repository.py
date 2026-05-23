from sqlalchemy.orm import Session

from models.client import Client


class ClientRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client):

        self.db.add(client)

        self.db.commit()

        self.db.refresh(client)

        return client

    def get_by_email(self, email: str):

        return (
            self.db.query(Client)
            .filter(Client.cliente_email == email)
            .first()
        )