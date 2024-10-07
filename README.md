# Automatização de Views com Inteligência Artificial Baseada em Regras de Negócio Utilizando Dataform

## Objetivo

Implementar uma solução automatizada, utilizando o modelo de IA Gemini integrado ao Google Cloud Platform (GCP), para gerar views a partir de regras de negócio definidas. O sistema deve interpretar essas regras e criar automaticamente as views no dataform, otimizando processos, aumentando a precisão e a escalabilidade, e proporcionando flexibilidade para a equipe de desenvolvimento e análise de dados.

## Funcionalidades

1. **Geração automática de consultas SQL**: Utiliza um modelo generativo no Vertex AI para criar consultas SQL com base nas informações da tabela do BigQuery e em prompts fornecidos.

2. **Criação de views no BigQuery**: Gera e implementa views no BigQuery a partir das consultas SQL geradas, automatizando a criação de views.

3. **Criação e upload de arquivos SQLX**: Converte as consultas SQL geradas em arquivos SQLX e realiza o upload para o Dataform, permitindo a automação e versionamento das views.

4. **Execução de jobs no Dataform**: Automatiza a execução de jobs no Dataform, incluindo a compilação e invocação de workflows, para processar e implementar as views.

5. **Geração de insights baseados em dados**: Utiliza IA para gerar insights sobre os dados retornados pelas consultas SQL, agregando valor ao processo de análise de dados.

## Tecnologias

- Python 3.12
- VertexAI API - (gemini-1.5-flash-001)
- Google Cloud BigQuery
- DataForm

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu_usuario/seu_projeto.git
cd seu_projeto
```

2. Crie um ambiente virtual e ative-o:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Autentique-se no Google Cloud:

```bash
gcloud auth application-default login
```
ou
```bash
$env:GOOGLE_APPLICATION_CREDENTIALS="credenciais_de_sua_conta_de_serviço"
```

5. Certifique-se de ter o **BigQuery**, **Vertex AI** e **Dataform** habilitados no seu projeto Google Cloud.

## Como Usar
Para usar o código, siga estes passos:

1. **Preparar o ambiente**:
   - Certifique-se de ter as bibliotecas necessárias instaladas, como `vertexai`, `google-cloud-bigquery`, e `google-cloud-dataform`.

2. **Configuração do modelo generativo no Vertex AI**:
   - Inicialize o projeto Vertex AI, definindo o `project_id` e `location` corretos:
     ```python
     vertexai.init(project="tarefa-squad", location="us-central1")
     ```

3. **Gerar consulta SQL**:
   - Especifique o dataset, a tabela e o prompt desejado. A IA vai gerar uma consulta SQL com base nas informações da tabela:
     ```python
     dataset = input('Em qual dataset está sua tabela?\n')
     table = input('Em qual tabela quer consultar?\n')
     prompt = input("Digite um prompt: \n")
     schema = get_schema(dataset, table) # Obtenha o esquema da tabela
     instruction = f"Você é um analista de dados especializado na tabela ({dataset}.{table}). SCHEMA: {schema}"
     response = generate(prompt, instruction) # Geração da consulta SQL
     ```

4. **Criar uma view no BigQuery**:
   - Após gerar a consulta SQL, você pode criar uma view no BigQuery usando:
     ```python
     target_dataset = input('Em qual dataset será salva a view?\n')
     name_view = input('Qual o nome terá a view?\n')
     view = create_view(response, target_dataset, name_view) # Cria o script SQLX
     ```

5. **Criar e subir o arquivo SQLX para o Dataform**:
   - Crie o arquivo SQLX localmente e faça o upload para o Dataform:
     ```python
     create_sqlx(view, "cartao_teste") # Cria o arquivo SQLX localmente
     upload_sqlx_file(project_id, repository_id, workspace, "cartao_teste.sqlx", "eventos_view.sqlx") # Upload do arquivo
     ```

6. **Executar o job no Dataform**:
   - Execute um job no Dataform para compilar e aplicar as mudanças:
     ```python
     execute_job(project_id, repository_id, workspace, "dataform", "eventos_view")
     ```

7. **Gerar insights baseados nos dados**:
   - Após obter os dados do BigQuery, você pode gerar insights com IA:
     ```python
     data = get_data(response) # Obtém os dados
     instruction_insight = "Forneça insights com base nesses dados"
     last_response = generate(data, instruction_insight) # Gera os insights
     print(last_response)
     ```

Esses passos permitem automatizar a criação de views e gerar insights usando IA e Dataform, facilitando o trabalho com grandes volumes de dados no BigQuery.