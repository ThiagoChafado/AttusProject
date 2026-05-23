from sqlalchemy import Column, Integer, String, Float

from database import Base

class Client(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String, nullable=False)
    cliente_email = Column(String, unique=True, nullable=False)
    tipo_solicitacao = Column(String, nullable=False)
    valor_patrimonio = Column(Float, nullable=False)
    