# Automatização de Views com Inteligência Artificial Baseada em Regras de Negócio Utilizando Dataform

## Objetivo
Implementar uma solução automatizada, utilizando o modelo de IA Gemini integrado ao Google Cloud Platform (GCP), para gerar views a partir de regras de negócio definidas. O sistema deve interpretar essas regras e criar automaticamente as views no Dataform, otimizando processos, aumentando a precisão e a escalabilidade, e proporcionando flexibilidade para a equipe de desenvolvimento e análise de dados.

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
- Dataform
- Streamlit

## Instalação
1. Clone o repositório:
    ```bash
    git clone https://github.com/2RP-Squad404/Git-Force.git
    cd Git-Force
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

### 1. Preparar o ambiente
Certifique-se de ter as bibliotecas necessárias instaladas, como `vertexai`, `google-cloud-bigquery`, e `google-cloud-dataform`.

### 2. Interação com o Frontend
O frontend foi desenvolvido usando Streamlit, permitindo que o usuário interaja com o sistema diretamente na interface web. O frontend coleta as entradas do usuário, como o nome do dataset, da tabela e o prompt para gerar a consulta SQL. Essas informações são enviadas ao backend via API.

### 3. Geração de consultas SQL via frontend
No frontend, o usuário deve fornecer as seguintes informações:
- Dataset
- Tabela
- Prompt (instrução sobre o que a consulta SQL deve retornar)

O backend, então, processa essas informações e gera a consulta SQL utilizando o modelo generativo do Vertex AI.

Exemplo de input no frontend:
```plaintext
Dataset: nome_do_dataset
Tabela: nome_da_tabela
Prompt: Gere uma consulta SQL que retorne as vendas totais por mês.
```
Processo do backend:
```python
dataset = st.text_input('Em qual dataset está sua tabela?')
table = st.text_input('Em qual tabela quer consultar?')
prompt = st.text_area("Digite um prompt: ")
schema = get_schema(dataset, table)  # Obtenha o esquema da tabela
instruction = f"Você é um analista de dados especializado na tabela ({dataset}.{table}). SCHEMA: {schema}"
response = generate(prompt, instruction)  # Geração da consulta SQL
```

### 4. Criação de Views no BigQuery via frontend
Após a consulta SQL ser gerada, o frontend permite que o usuário selecione o dataset de destino e o nome da view que será criada no BigQuery.

Exemplo no frontend:
```plaintext
Dataset de destino: dataset_destino
Nome da view: nome_da_view
```
O backend cria a view da seguinte forma:
```python
target_dataset = st.text_input('Em qual dataset será salva a view?')
name_view = st.text_input('Qual o nome terá a view?')
view = create_view(response, target_dataset, name_view)  # Cria o script SQLX
```

### 5. Upload do arquivo SQLX para o Dataform
O backend cria o arquivo SQLX localmente e faz o upload para o Dataform.
```python
create_sqlx(view, teste)  # Cria o arquivo SQLX localmente
upload_sqlx_file(project_id, repository_id, workspace, teste.sqlx, "nome_view.sqlx")  # Upload do arquivo
```

### 6. Execução de jobs no Dataform
Depois que o arquivo SQLX for enviado, o backend permite executar um job no Dataform para aplicar a nova view.
```python
execute_job(project_id, repository_id, workspace, "dataform", "nome_view")
```

### 7. Geração de insights baseados nos dados
Após a consulta ser executada, o backend pode gerar insights com IA a partir dos dados retornados.
```python
data = get_data(response)  # Obtém os dados
instruction_insight = "Forneça insights com base nesses dados"
last_response = generate(data, instruction_insight)  # Gera os insights
st.write(last_response)
```

Com essa solução, o frontend facilita a interação do usuário para criar consultas SQL, gerar views automaticamente no BigQuery e realizar o upload dessas views para o Dataform. Tudo isso integrado com IA para geração automática de código e insights baseados nos dados.