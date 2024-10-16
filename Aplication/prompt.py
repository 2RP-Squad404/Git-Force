from gemini import generate
from bigquery import create_view, get_data, get_schema, create_sqlx, string_cleaned, name_view_sqlx
from dataformTest import upload_sqlx_file, execute_job

def processar_prompt(prompt, dataset, table, target_dataset, name_view):
    # Obter o schema da tabela
    schema = get_schema(dataset, table)
    print(f"Schema obtido: {schema}")

    # Instrução para o modelo gerar a consulta SQL e insights
    instruction = """Você é um analista de dados especializado na tabela ({}.{}). Essa tabela contém informações como SCHEMA: {}. Ao criar consultas SQL para visualizar os dados, certifique-se de nomear as colunas utilizando 'AS' seguido de um nome descritivo e apropriado que reflita o conteúdo ou a operação realizada (exemplo: total_vendas, media_idade, soma_valores). Sempre priorize a clareza e legibilidade ao montar suas consultas.""".format(dataset, table, schema) # Instrução para gerar a consulta
    
    # Geração da consulta com base no prompt
    response = generate(prompt, instruction)
    print(f"Resposta gerada: {response}")

    # Processamento do dado e criação da view
    data = get_data(response)
    print(data)
    response_view = string_cleaned(response)
    print(f"View a ser criada: {response_view}")

    # Tente criar a view e capture qualquer erro
    try:
        view = create_view(response_view, target_dataset, name_view)
        print(f"View criada: {view}")
    except Exception as e:
        print(f"Erro ao criar view: {e}")

    # Criação e upload do arquivo SQLX no Dataform
    create_sqlx(view, "teste")
    project_id = "tarefa-squad"
    repository_id = "teste"
    workspace = "testeDataform"
    file_path_local = "teste.sqlx"
    file_path_repo = name_view_sqlx(name_view)
    
    # Tente fazer o upload e capture qualquer erro
    try:
        upload_sqlx_file(project_id, repository_id, workspace, file_path_local, file_path_repo)
        print(f"Arquivo SQLX enviado: {file_path_repo}")
    except Exception as e:
        print(f"Erro ao fazer upload do SQLX: {e}")

    # Executa o job no Dataform
    try:
        execute_job(project_id, repository_id, workspace, "dataform", name_view)
        print("Job executado com sucesso.")
    except Exception as e:
        print(f"Erro ao executar o job: {e}")

    # Instrução para gerar insights sobre os dados
    instruction_insight = """Você é um analista de dados especializado. Forneça insights com base nos dados apresentados, focando nos principais indicadores e observações relevantes. Organize o resultado de forma clara e objetiva:
    1. *Dado principal*: Resuma o ponto mais importante.
    2. *Métricas chave*: Apresente os números relevantes.
    3. *Observações/Ações*: Destaque possíveis padrões ou tendências."""
    insight = generate(data, instruction_insight)
    
    print(f"Insight gerado: {insight}")
    return insight
