from gemini import generate
from bigquery import create_view, get_data, get_schema, create_sqlx, string_cleaned, name_view_sqlx
from dataformTest import upload_sqlx_file, execute_job

def processar_prompt(prompt, dataset, table, target_dataset, name_view):
    # Obter o schema da tabela
    schema = get_schema(dataset, table)

    # Instrução para gerar a consulta
    instruction = """Você é um analista de dados especializado na tabela ({}.{}). Essa tabela contém informações como SCHEMA: {}. Ao criar consultas SQL para visualizar os dados, certifique-se de nomear as colunas utilizando 'AS' seguido de um nome descritivo e apropriado que reflita o conteúdo ou a operação realizada (exemplo: total_vendas, media_idade, soma_valores). Sempre priorize a clareza e legibilidade ao montar suas consultas.
    """.format(dataset, table, schema)

    # Geração da resposta da IA
    response = generate(prompt, instruction) 
    data = get_data(response)  # Obtendo o dado

    response_view = string_cleaned(response)  # Limpando a consulta

    view = create_view(response_view, target_dataset, name_view)  # Criando o script SQLX

    create_sqlx(view, "teste")  # Criando o arquivo SQLX

    # Instrução para fornecer insights
    instruction_insight = """Você é um analista de dados especializado. Forneça insights com base nos dados apresentados, focando nos principais indicadores e observações relevantes. Organize o resultado de forma clara e objetiva:
    1. *Dado principal*: Resuma o ponto mais importante.
    2. *Métricas chave*: Apresente os números relevantes.
    3. *Observações/Ações*: Destaque possíveis padrões ou tendências.
    """
    
    last_response = generate(data, instruction_insight)  # Gerando o insight com o dado

    # Executar o upload do SQLX e o job do Dataform
    project_id = "tarefa-squad"
    repository_id = "teste"
    workspace = "testeDataform"
    file_path_local = "teste.sqlx"
    upload_sqlx_file(project_id, repository_id, workspace, file_path_local, name_view_sqlx(name_view))
    execute_job(project_id, repository_id, workspace, "dataform", name_view)

    print(last_response)
    return last_response  # Retornar a resposta final
