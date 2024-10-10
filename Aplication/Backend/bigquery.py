from google.cloud import bigquery

# Função para limpar a string da consulta
def string_cleaned(content: str) -> str:
    content_cleaned = content.replace("```sql", "").replace("```", "")
    content_cleaned = content_cleaned.strip()
    return content_cleaned

# Função para pegar dados
def get_data(query: str, project_id: str = "tarefa-squad"):
    if not project_id:
        raise ValueError("O ID do projeto não pode estar vazio.")

    client = bigquery.Client(project=project_id)

    try:
        query_cleaned = string_cleaned(query)  # Limpando string
        query_job = client.query(query_cleaned)  # Rodando a query
        
        # Armazenando e retornando o resultado
        return [dict(row) for row in query_job.result()]

    except Exception as e:
        print(f"Erro de consulta: {e}")
        return None

    finally:
        client.close()  # Fecha o cliente BigQuery

# Função para pegar o schema da tabela
def get_schema(dataset: str, table: str, project_id: str = "tarefa-squad"):
    if not project_id:
        raise ValueError("O ID do projeto não pode estar vazio.")
    if not dataset or not table:
        raise ValueError("Dataset e tabela não podem estar vazios.")

    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset}.{table}"

    try:
        table = client.get_table(table_ref)
        # Retorna o schema como uma lista de dicionários
        return table.schema
    
    except Exception as e:
        print(f"Erro ao obter schema: {e}")
        return None

    finally:
        client.close()

# Criando o arquivo SQLX
def create_sqlx(query: str, file_name: str):
    file_name = f"{file_name}.sqlx"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(query)  # Escreve o conteúdo do SQLX no arquivo
    print(f"Arquivo {file_name} criado com sucesso.")

# Criando o script SQLX para a view
def create_view(query: str, dataset: str, table: str, project_id: str = "tarefa-squad"):
    if not dataset or not table:
        raise ValueError("Dataset e tabela não podem estar vazios para criar a view.")
    
    view_query = f"""CREATE OR REPLACE VIEW `{project_id}.{dataset}.{table}` AS
{query}
    """
    return view_query

def name_view_sqlx(view):
    name_view = """{}.sqlx""".format(view)
    return name_view