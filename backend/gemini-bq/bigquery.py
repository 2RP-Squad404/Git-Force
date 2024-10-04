from google.cloud import bigquery

# Função para pegar apenas o dado
def get_data (query: str):
    client = bigquery.Client() # Criando um cliente bigquery

    query_cleaned = string_cleaned(query) # Limpando string
    try:
        query_job = client.query(query_cleaned) # Rodando a query
    except Exception as e:
        print("Erro de consulta")

    results = query_job.result() # Armazendo o resultado
    client.close()
    data = [dict(row) for row in results] # Transformando em um dicionário
    return data

def get_schema (dataset: str, table: str):
    client = bigquery.Client() # Criando um cliente bigquery
    
    # Configurando referência do dataset e da tabela
    dataset_ref = client.dataset(dataset)
    table_ref = dataset_ref.table(table)

    # Obter o esquema da tabela
    table = client.get_table(table_ref)
    schema = table.schema

    client.close()
    return schema

# Função para tirar o que não faz parte da consulta
def string_cleaned (content: str):
    content_cleaned = content.replace("```sql", "").replace("```", "")
    content_cleaned = content_cleaned.strip()
    return content_cleaned

# Criando o arquivo SQLX
def create_sqlx(query, file_name):
    file_name = f"{file_name}.sqlx"
    with open(file_name, "w") as file:
        file.write(query) # Escreve o conteúdo do SQLX no arquivo
    print(f"Arquivo {file_name} criado com sucesso.")

# Criando o script SQLX
def create_view(query, dataset, table):
    view = """CREATE OR REPLACE VIEW `tarefa-squad.{}.{}` AS 
    {}""".format(dataset, table, query)
    return view