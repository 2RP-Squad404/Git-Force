from gemini import generate
from bigquery import create_view, get_data, get_schema, create_sqlx, string_cleaned
from dataformTest import upload_sqlx_file, execute_job

# Getting Dataset and Table name
dataset = input('Em qual dataset está sua tabela?\n')
table = input('Em qual tabela quer consultar?\n')
target_dataset = input('Em qual dataset será salvo a view?\n')
name_view = input('Qual o nome terá a view?\n')

# Get table schema
schema = get_schema(dataset, table)

prompt = input("Digite um prompt: \n")
instruction = """Você é um analista de dados especializado na tabela ({}.{}). Essa tabela contém informações como SCHEMA: {}
Use essa informação como base para montar consultas SQL e criar insights levando em consideração o que for pedido.

""".format(dataset, table, schema)

response = generate(prompt, instruction)
data = get_data(response)

response_view = string_cleaned(response)
print(response_view)
view = create_view(response_view, target_dataset, name_view)

create_sqlx(view, "cartao_teste")

instruction2 = """Você é um analista de dados especializado. Forneça insights com base nesses dados que serão apresentados. (Seja breve e objetivo)"""
last_response = generate(data, instruction2)

project_id = "tarefa-squad"
repository_id = "teste"  # Nome simples do repositório
workspace = "testeDataform"  # A branch onde você quer fazer o upload
file_path_local = "cartao_teste.sqlx"  # Caminho do arquivo local
file_path_repo = "eventos_view.sqlx"  # Nome do arquivo dentro do repositório

upload_sqlx_file(project_id, repository_id, workspace, file_path_local, file_path_repo)
execute_job(project_id, repository_id, workspace, "dataform", "eventos_view")

print(last_response)



