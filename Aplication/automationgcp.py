import os
import json
from google.cloud import secretmanager

# Função para acessar o segredo no Secret Manager
def get_service_account_from_secret(secret_id, project_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    # Acessa a versão mais recente do segredo
    response = client.access_secret_version(request={"name": name})
    
    # Retorna o conteúdo do segredo (JSON da conta de serviço)
    service_account_key = response.payload.data.decode('UTF-8')
    return json.loads(service_account_key)

if __name__ == "__main__":
    # IDs do projeto e do segredo armazenado
    project_id = "tarefasquad"
    secret_id = "gchat" 

    # Obter a chave da conta de serviço do Secret Manager
    service_account_info = get_service_account_from_secret(secret_id, project_id)
    
    # Exibir as credenciais da conta de serviço (JSON formatado)
    print(json.dumps(service_account_info, indent=2))
