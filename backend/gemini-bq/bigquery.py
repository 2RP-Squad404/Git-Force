from google.cloud import bigquery

def get_data (query: str):
    # Create a BQ client
    client = bigquery.Client()

    # Cleaning string
    query_cleaned = string_cleaned(query)
    try:
        # Running query
        query_job = client.query(query_cleaned)
    except Exception as e:
        # Exception
        print("Erro de consulta")

    # Getting Result
    results = query_job.result()
    # Closing client
    client.close()
    # Become to dictionary
    data = [dict(row) for row in results] 
    return data

def get_schema (dataset: str, table: str):
     # Create a BQ client
    client = bigquery.Client()
    
    # Setting Reference
    dataset_ref = client.dataset(dataset)
    table_ref = dataset_ref.table(table)

    # Getting Schema
    table = client.get_table(table_ref)
    schema = table.schema

    # Closing client
    client.close()
    return schema

def string_cleaned (content: str):
    content_cleaned = content.replace("```sql", "").replace("```", "")
    content_cleaned = content_cleaned.strip()
    return content_cleaned

def get_query_in_response(response):
    match = re.search(r'CREATE\s+OR\s+REPLACE\s+VIEW\s+`[^`]+`\s+AS[\s\S]*?FROM\s+`([^`]+)`', response)

    if match:
        sql_query = match.group(0).strip()  # Obtemos a parte capturada e removemos espaços em branco
        print(sql_query)
        return sql_query
    else:
        print("Query não encontrada.")
        return

def create_sqlx(query, file_name):
    file_name = f"{file_name}.sqlx"
    with open(file_name, "w") as file:
    # Escreve o conteúdo do SQLX no arquivo
        file.write(query)
    print(f"Arquivo {file_name} criado com sucesso.")
    
def create_view(query, dataset, table):
    view = """CREATE OR REPLACE VIEW `tarefa-squad.{}.{}` AS 
    {}""".format(dataset, table, query)
    return view