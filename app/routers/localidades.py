from datetime import datetime

from .. import Models, Schemas
from sqlalchemy.orm import Session
from fastapi import Depends, status, APIRouter, Response, HTTPException
from ..Database import get_db
from ..CepService import CepService

cepService = CepService()
router = APIRouter()

@router.get('/', response_model=Schemas.ListLocalidadesResponse)
def get_localidades(uf:str = '', db: Session = Depends(get_db)):
    
    localidades = db.query(Models.Localidades).group_by(Models.Localidades.id).filter(
        Models.Localidades.uf.contains(uf)).all()
    
    return { 'localidades': localidades }


@router.post('/{cep}', status_code=status.HTTP_201_CREATED, response_model=Schemas.LocalidadesResponse)
def create_localidade(cep: str, db: Session = Depends(get_db)):
    
    localidades = cepService.get_address_by_cep(cep)
    
    nova_localidade = Models.Localidades(**{
            "cep"       :localidades.get("cep")
        ,   "uf"        :localidades.get("uf",'')
        ,   "logradouro":localidades.get("logradouro",'')
        ,   "localidade":localidades.get("localidade",'')
    })
    db.add(nova_localidade)
    db.commit()
    db.refresh(nova_localidade)
    return nova_localidade

@router.delete('/{cep}')
def delete_localidade(cep: str, db: Session = Depends(get_db)):
    
    if '-' not in cep:
        cep = "{}-{}".format(cep[:5], cep[5:8])
    
    localidade_query = db.query(Models.Localidades).filter(Models.Localidades.cep == cep)
    localidade = localidade_query.first()
    if not localidade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Nenhuma localidade encontrada com o ID: {cep}')

    localidade_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)