import streamlit as st
from prompt import processar_prompt  # Importar função do prompt.py

# Título
st.title("G-Chat")

# Função para exibir mensagens com estilo diferenciado (usuário e bot)
def exibir_mensagem(tipo, mensagem):
    if tipo == "Você":
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 10px; background-color: #007bff; color: white;'>
                <strong>Você:</strong> {mensagem}
            </div>
        """, unsafe_allow_html=True)
    else:
        mensagem_formatada = mensagem.replace("\n", "<br>")
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 10px; text-align: left; margin-bottom: 10px; background-color: #343a40; color: white;'>
                <strong>GenAI:</strong> {mensagem_formatada}
            </div>
        """, unsafe_allow_html=True)

# Inicializar session_state
if "historico" not in st.session_state:  # Para aparecer as mensagens
    st.session_state.historico = []
if "fase_inicial" not in st.session_state:  # Onde aparecem os prompts das perguntas
    st.session_state.fase_inicial = True
if "respostas_iniciais" not in st.session_state:  # Onde vai ser armazenado as respostas da fase_inicial
    st.session_state.respostas_iniciais = [""] * 4
if "mensagem_input" not in st.session_state:  # Onde vai ser armazenado a mensagem do usuário
    st.session_state.mensagem_input = ""

# Perguntas iniciais do bot
perguntas_iniciais = [
    "Em qual dataset está sua tabela?",
    "Em qual tabela você quer consultar?",
    "Em qual dataset será salvo a view?",
    "Qual o nome terá a view?"
]

# Função para processar a mensagem
def enviar_mensagem():
    mensagem_usuario = st.session_state.mensagem_input
    if mensagem_usuario.strip() == "":
        st.error("Por favor, digite uma mensagem.")
        return
    
    # Salvar no histórico a mensagem do usuário
    st.session_state.historico.append(f"Você: {mensagem_usuario}")

    # Processar a resposta do bot
    resposta = processar_prompt(
        mensagem_usuario, 
        st.session_state.dataset, 
        st.session_state.table, 
        st.session_state.target_dataset, 
        st.session_state.name_view
    )

    # Salvar resposta no histórico como "GenAI"
    if resposta:
        st.session_state.historico.append(f"GenAI: {resposta}")
    else:
        st.session_state.historico.append("GenAI: Não foi possível gerar uma resposta.")

    # Limpar o campo de input após o envio da mensagem
    st.session_state.mensagem_input = ""  # Definido após o processamento da mensagem

# Verificação das respostas iniciais e transição para o chat normal
def enviar_respostas_iniciais():
    if all(resposta != "" for resposta in st.session_state.respostas_iniciais):
        # Salvar as respostas nas variáveis do session_state
        st.session_state.dataset = st.session_state.respostas_iniciais[0]
        st.session_state.table = st.session_state.respostas_iniciais[1]
        st.session_state.target_dataset = st.session_state.respostas_iniciais[2]
        st.session_state.name_view = st.session_state.respostas_iniciais[3]

        # Marcar que as perguntas iniciais foram respondidas
        st.session_state.fase_inicial = False
        st.session_state.historico = []
    else:
        st.warning("Por favor, preencha todos os campos antes de enviar.")

# Fase das perguntas iniciais
if st.session_state.fase_inicial:
    st.header("Responda as perguntas abaixo:")
    
    for i, pergunta in enumerate(perguntas_iniciais):
        st.session_state.respostas_iniciais[i] = st.text_input(
            pergunta,
            value=st.session_state.respostas_iniciais[i],
            key=f"resposta_inicial_{i}"
        )

    if st.button("Enviar Respostas"):
        st.session_state.respostas_iniciais = [
            st.session_state[f"resposta_inicial_{i}"] for i in range(4)
        ]
        enviar_respostas_iniciais()

# Fase da conversa normal
else:
    # Exibir o histórico de mensagens
    for msg in st.session_state.historico:
        tipo, texto = msg.split(": ", 1)
        exibir_mensagem(tipo.strip(), texto.strip())

    # Função a ser chamada quando o usuário envia uma mensagem
    def reset():
        enviar_mensagem()

    # Campo para o usuário digitar a mensagem
    mensagem_usuario = st.text_input(
        "Digite sua mensagem:",
        key="mensagem_input",
        on_change=reset  # Chama função reset
    )

    # Botão para enviar a mensagem
    if st.button("Enviar Mensagem"):
        reset()  # Chama a função para enviar a mensagem ao clicar no botão
