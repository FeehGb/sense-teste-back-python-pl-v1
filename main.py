import os

from fastapi        import FastAPI, HTTPException
from dotenv         import load_dotenv
from app.Request    import Request, Path, Json
from app.Database   import Database


# Conexao com o banco
load_dotenv()
db  = Database(
            host      = os.getenv('HOST')
        ,   user      = os.getenv('USER')
        ,   password  = os.getenv('PASSWORD')
        ,   database  = os.getenv('DATABASE')                              
)

api = Request
api.default_params = { "base_url": "https://viacep.com.br/ws" }
# Rotas da API 
@Json()
@Request("/{cep}/json")
def recuperar_localidades(cep:Path):
    #"Recupera a localidade baseado no CEP, retorna os dados em JSON"
    ...




app = FastAPI()
# Rotas do app
@app.get("/")
def read_root():
    return {"server":"ok"}


@app.get("/api/localidades/")
def consultar_localidade(uf:str = None):
    #"Retorna todas as localidades cadastradas no banco de dados"
    error = {
                "status_code" : 404
            ,   "detail"      : ""
    }
    params = {      
                "fields":[
                     "cep"
                    , "uf"
                    , "localidade"
                    , "logradouro"
                    , "data_consulta"
                ]
                ,   "table":"localidades"
            }
    
    if uf:
        params = {**params, **{"where": {"uf":uf}}}
        
    try:
        records = db.select(**params)
        if records:
            return {"localidades":records}
        else:
            error["detail"] = "Nenhum dado foi encontrado em nossa base"
        
        
    except Exception as Exception_error:
        error["detail"] = "Erro de execução"
        error["status_code"] = 500
        
    
    if error:
        raise HTTPException(**error)

    

# Mudar para POST
@app.post("/api/localidades/{cep}")
def cadastrar_cep_selecionado(cep: int):
    error = {
        "status_code" : 400
    ,   "detail"      : "CPF inválido ou não fornecido "
    }
    
    dados_localidade = recuperar_localidades(cep=cep)
    if dados_localidade :
        cep = dados_localidade.get("cep",'')
        try:
            db.insert(
                    table="localidades"
                ,   data={
                            "cep"       : cep
                        ,   "uf"        : dados_localidade.get("uf",'')
                        ,   "localidade": dados_localidade.get("logradouro",'')
                        ,   "logradouro": dados_localidade.get("localidade",'')
                    }
            )
            return {"success":f"CEP({cep}) inserido com sucesso!"}
        except Exception as Exception_error:
            error["detail"] = "Houve erro ao tentar inserir dados, ou os dados"\
            " já constam em nossa base de dados "
            
    raise HTTPException(**error)
        
@app.delete("/api/localidades/{cep}")
def remover_localidade(cep:str):
    error = {
        "status_code" : 400
    ,   "detail"      : "Não foi possível deletar ou item nao encontrado"
    }
    if '-' not in cep:
        cep = "{}-{}".format(cep[:5], cep[5:8])
    
    try :
        deleted = db.delete(table='localidades',  where={"cep":cep})
        if  deleted:
            return {"success": f"CEP({cep}) foi removido com sucesso"}
    except Exception as error:
        print(str(error))
        error = {
            "status_code" : 500
        ,   "detail"      : "Não foi possivel deletar devido a erros"
        }
        
    raise HTTPException(**error)
    




