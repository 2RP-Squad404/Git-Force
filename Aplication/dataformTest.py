from google.cloud import dataform_v1beta1 as dataform

# Faz upload de um arquivo SQLX para o repositório Dataform em uma workspace específica.
def upload_sqlx_file(project_id, repository_id, workspace, file_path_local, file_path_repo):
    try:
        client = dataform.DataformClient() # Inicializa o cliente do Dataform

        repository_name = client.repository_path(project_id, "us-central1", repository_id) # Definindo o caminho correto do repositório

        # Lendo o conteúdo do arquivo local
        with open(file_path_local, "r") as file:
            file_content = file.read()

        file_name = f"definitions/{file_path_repo}" # Definindo o caminho do arquivo no repositório

        workspace_name = f"{repository_name}/workspaces/{workspace}" # Preparando o nome do workspace

        # Montando o request para escrever o arquivo no workspace
        request = dataform.WriteFileRequest(
            workspace=workspace_name,
            path=file_name,
            contents=file_content.encode("utf-8")  # Certifique-se de codificar o conteúdo do arquivo
        )

        client.write_file(request=request) # Enviando o arquivo para o workspace

        print(f"Arquivo {file_name} enviado com sucesso para o workspace {workspace}.")

    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")


def sample_create_compilation_result(project_id, repository_id, workspace):
    client = dataform.DataformClient() # Cria um cliente para o Dataform

    compilation_result = dataform.CompilationResult() # Inicialize os argumentos da solicitação
    
    compilation_result.workspace = f"projects/{project_id}/locations/us-central1/repositories/{repository_id}/workspaces/{workspace}" # Substitua por seu branch, tag ou commit 

    # Defina o parent corretamente com o caminho para o repositório
    request = dataform.CreateCompilationResultRequest(
        parent=f"projects/{project_id}/locations/us-central1/repositories/{repository_id}",
        compilation_result=compilation_result,
    )

    response = client.create_compilation_result(request=request) # Faz a solicitação para criar o resultado de compilação
    
    return response

def create_workflow_invocation(compilation_result, project_id, repository_id, dataset_id, file_name):
    client = dataform.DataformClient() # Cria um cliente para o Dataform

    workflow_invocation = dataform.WorkflowInvocation() # Inicialize os argumentos da invocação do workflow

    workflow_invocation.compilation_result = compilation_result # Define o compilation result a partir do valor obtido

    workflow_invocation.invocation_config.included_targets.extend([
        dataform.Target(
            database=project_id,   
            schema=dataset_id,   
            name=file_name
        )
    ])

    # Crie o request de invocação
    request = dataform.CreateWorkflowInvocationRequest(
        parent=f"projects/{project_id}/locations/us-central1/repositories/{repository_id}",
        workflow_invocation=workflow_invocation,
    )

    response = client.create_workflow_invocation(request=request) # Faz a solicitação para criar o workflow invocation

    return response

# Função para executar o processo
def execute_job(project_id, repository_id, workspace, dataset_id, file_name):

    compilation_result = sample_create_compilation_result(project_id=project_id, repository_id=repository_id, workspace=workspace)

    workflow_invocation = create_workflow_invocation(compilation_result=compilation_result.name, project_id=project_id, repository_id=repository_id, dataset_id=dataset_id, file_name=file_name)

    return workflow_invocation