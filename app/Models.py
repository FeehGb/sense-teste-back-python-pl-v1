from .Database import Base
from sqlalchemy import TIMESTAMP, Column, String, text
from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

class Localidades(Base):
    
    __tablename__ = 'localidades'
    
    id              = Column(GUID, primary_key=True, server_default=GUID_SERVER_DEFAULT_POSTGRESQL )
    cep             = Column(String, unique=True, nullable=False)
    uf              = Column(String, nullable=False)
    localidade      = Column(String, nullable=False)
    logradouro      = Column(String, nullable=True) 
    data_consulta   = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()")) 
   