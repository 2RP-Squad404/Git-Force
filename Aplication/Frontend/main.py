import streamlit as st
from Backend.prompt import processar_prompt

# Função para exibir mensagens com estilo diferenciado (usuário e bot)
def exibir_mensagem(tipo, mensagem):
    if tipo == "Você":
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 10px; background-color: #007bff; color: white;'>
                <strong>Você:</strong> {mensagem}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 10px; text-align: left; margin-bottom: 10px; background-color: #343a40; color: white;'>
                <strong>GenAI:</strong> {mensagem}
            </div>
        """, unsafe_allow_html=True)

# Inicializar session_state
if "historico" not in st.session_state:
    st.session_state.historico = []
if "fase_inicial" not in st.session_state:
    st.session_state.fase_inicial = True
if "respostas_iniciais" not in st.session_state:
    st.session_state.respostas_iniciais = [""] * 4
if "mensagem_usuario" not in st.session_state:
    st.session_state.mensagem_usuario = ""

# Perguntas iniciais do bot
perguntas_iniciais = [
    "Em qual dataset está sua tabela?",
    "Em qual tabela você quer consultar?",
    "Em qual dataset será salvo a view?",
    "Qual o nome terá a view?"
]

# Função para processar a mensagem
def enviar_mensagem():
    mensagem_usuario = st.session_state.mensagem_usuario

    # Salvar as repostas do session_state nas variáveis 
    dataset = st.session_state.dataset
    table = st.session_state.table
    target_dataset = st.session_state.target_dataset
    name_view = st.session_state.name_view

    # Verificação para garantir que dataset e table não estão vazios
    if not dataset or not table:
        st.error("Por favor, preencha o dataset e a tabela antes de enviar a mensagem.")
        return  # Para a execução da função se as variáveis estiverem vazias

    # Se tudo estiver correto ele vai processar o prompt (função do prompt.py)
    resposta = processar_prompt(mensagem_usuario, dataset, table, target_dataset, name_view)
    st.session_state.historico.append(f"GenAI:\n{resposta}")

    # Reseta o input
    st.session_state.mensagem_usuario

# Verificação das respostas iniciais e transição para o chat normal
def enviar_respostas_iniciais():
    if all(resposta != "" for resposta in st.session_state.respostas_iniciais):
        # Salvar as respostas nas variáveis do session_state
        st.session_state.dataset = st.session_state.respostas_iniciais[0]
        st.session_state.table = st.session_state.respostas_iniciais[1]
        st.session_state.target_dataset = st.session_state.respostas_iniciais[2]
        st.session_state.name_view = st.session_state.respostas_iniciais[3]

        st.session_state.fase_inicial = False
        st.session_state.historico = []
    else:
        st.warning("Por favor, preencha todos os campos antes de enviar.")

# Interface principal
st.title("G-Chat")

# Fase das perguntas iniciais
if st.session_state.fase_inicial:
    st.header("Responda as perguntas abaixo:")
    
    #Percorre a lista das perguntas
    for i, pergunta in enumerate(perguntas_iniciais):
        st.session_state.respostas_iniciais[i] = st.text_input(
            pergunta,
            value=st.session_state.respostas_iniciais[i],
            key=f"resposta_inicial_{i}"
        )

    #Salva as respostas
    if st.button("Enviar Respostas"):
        st.session_state.respostas_iniciais = [
            st.session_state[f"resposta_inicial_{i}"] for i in range(4)
        ]
        enviar_respostas_iniciais()

# Conversa normal onde é enviado o prompt e retornado a resposta
else:
    for msg in st.session_state.historico:
        tipo, texto = msg.split(": ", 1)
        exibir_mensagem(tipo.strip(), texto.strip())

    st.text_input(
        "Digite sua mensagem:",
        value=st.session_state.mensagem_usuario,
        on_change=enviar_mensagem,
        key="mensagem_usuario"
    )

    if st.button("Enviar Mensagem"):
        enviar_mensagem()
