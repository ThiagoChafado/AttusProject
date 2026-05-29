from pydantic import BaseModel, EmailStr, Field


class ClientCreate(BaseModel):

    cliente_nome: str = Field(..., min_length=1, max_length=100) # nao pode ser vazio

    cliente_email: EmailStr 

    tipo_solicitacao: str

    valor_patrimonio: float = Field(..., ge=0)  # patrimonio zero ou positivo