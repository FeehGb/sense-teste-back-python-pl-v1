# Teste técnico backend Python pleno

Instalação e Execução
---
1. **INSTALAR DEPENDENCIAS**

        pip install -r .\requirements.txt --user
2. **Rodar arquivo docker-compose.yml**
       
        docker-compose up -d  
2. **Crie seu arquivo .env com as seguintes configurações**

        DATABASE_PORT=6500
        POSTGRES_PASSWORD=1234
        POSTGRES_USER=postgres
        POSTGRES_DB=fastapi
        POSTGRES_HOST=postgres
        POSTGRES_HOSTNAME=127.0.0.1
        CLIENT_ORIGIN=http://localhost:3000
        
        
3. **Executar projeto**

      uvicorn app.main:app --host localhost --port 8000 --reload    
        
5. acessar http://localhost:8000
  - http://localhost:8000/api/localidades/ - Lista todas as localidades cadastradas
  - http://localhost:8000/api/localidades/?uf=PR - Lista todas as localidades daquela UF
6. Consumir via postman utlizando metodo **"POST"** a rota: http://localhost:8000/api/localidades/82700370
    - Ira Cadastrar no banco de dados a localidade selecionada


Documentação
---

Acessar - http://localhost:8000/docs


