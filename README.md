# Teste técnico backend Python pleno

Instalação
---
1. **Executar comando para criar um docker com PostgreSQL**

        docker run -p 5432:5432 -e POSTGRES_PASSWORD=1234 postgres
2. **Acessar o banco de dados**
       
        docker exec -it <nome_do_banco_gerado> psql -U postgres
        
3. **Executar o SQL de Criação de tabela**

      ```sql
      CREATE TABLE localidades (
        id SERIAL PRIMARY KEY,
        cep VARCHAR(8)  NOT NULL,
        uf VARCHAR(2)  NOT NULL,
        localidade  VARCHAR(255) ,
        logradouro  VARCHAR(255) ,
        data_consulta  TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE(cep)
      );
      ```
4. Crie um arquivo .env com os seguintes dados

        ``` 
          HOST="localhost"
          USER="postgres"
          PASSWORD="1234"
          DATABASE="postgres"
        ```
4. Rodar o comando uvicorn
  
        main:app --reload
        
        
5. acessar http://localhost:8000
  - http://localhost:8000/api/localidades/ - Lista todas as localidades cadastradas
  - http://localhost:8000/api/localidades/?uf=PR - Lista todas as localidades daquela UF
6. Consumir via postman utlizando metodo **"POST"** a rota: http://localhost:8000/api/localidades/82700370
    - Ira Cadastrar no banco de dados a localidade selecionada


Documentação
---

Acessar - http://localhost:8000/docs

Dependências
---

- fastapi
  - FastAPI é um moderno e rápido (alta performance) framework web para construção de APIs com Python 3.6 ou superior, baseado nos type hints padrões do Python.

- requests
  - Biblioteca HTTP para a linguagem de programação Python.

- dotenv
  - O Dotenv é um pacote para gerenciar as variáveis de ambiente
  
- uvicorn
  -  O Uvicorn faz o trabalho de subir o servidor para acessarmos as rotas. 

