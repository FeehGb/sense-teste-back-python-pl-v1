import requests
#from .. import Models, Schemas
class CepService:
    def __init__(self):
        self.base_url = "https://viacep.com.br"
        
    def get_address_by_cep(self, cep: str):
        url = f'{self.base_url}/ws/{cep}/json/'
        response = requests.get(url)
        return response.json()