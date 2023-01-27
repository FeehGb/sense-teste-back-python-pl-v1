from datetime import datetime
from typing import List
from pydantic import BaseModel


class LocalidadesBaseSchema(BaseModel):
    cep             : str
    uf              : str
    localidade      : str
    logradouro      : str
    data_consulta   : datetime | None = None

    class Config:
        orm_mode = True

class CreateLocalidadesSchema(LocalidadesBaseSchema):
    cep             : str
    uf              : str
    localidade      : str
    logradouro      : str
    data_consulta   : datetime | None = None

class LocalidadesResponse(LocalidadesBaseSchema):
    cep             : str
    uf              : str
    localidade      : str
    logradouro      : str
    data_consulta   : datetime | None = None


class ListLocalidadesResponse(BaseModel):
    localidades: List[LocalidadesResponse]


