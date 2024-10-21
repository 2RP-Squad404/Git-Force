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
        st.markdown(f"{mensagem}")

# Inicializar session_state
if "historico" not in st.session_state:
    st.session_state.historico = []
if "fase" not in st.session_state:
    st.session_state.fase = "perguntas_iniciais"  # Fase inicial como padrão
if "respostas_iniciais" not in st.session_state:
    st.session_state.respostas_iniciais = [""] * 4
if "mensagem_input" not in st.session_state:
    st.session_state.mensagem_input = ""

# Perguntas iniciais
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
    st.session_state.historico.append(f"Você: {mensagem_usuario}")  # Salvar no histórico a mensagem do usuário

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

    # Limpar o campo de input sem modificar diretamente o session_state
    st.session_state.mensagem_input = ""

# Verificação das respostas iniciais e transição para o chat normal
def enviar_respostas_iniciais():
    # Atualizar diretamente o session_state
    for i in range(4):
        st.session_state.respostas_iniciais[i] = st.session_state[f"resposta_inicial_{i}"]

    # Verificar se todas as respostas foram preenchidas
    if all(resposta != "" for resposta in st.session_state.respostas_iniciais):
        # Salvar as respostas nas variáveis do session_state
        st.session_state.dataset = st.session_state.respostas_iniciais[0]
        st.session_state.table = st.session_state.respostas_iniciais[1]
        st.session_state.target_dataset = st.session_state.respostas_iniciais[2]
        st.session_state.name_view = st.session_state.respostas_iniciais[3]
        
        # Mudar para a fase de conversa
        st.session_state.fase = "conversa"
        st.session_state.historico = []
    else:
        st.warning("Por favor, preencha todos os campos antes de enviar.")

# Fase das perguntas iniciais
if st.session_state.fase == "perguntas_iniciais":
    st.header("Responda as perguntas abaixo:")
    for i, pergunta in enumerate(perguntas_iniciais):
        st.text_input(
            pergunta,
            value=st.session_state.respostas_iniciais[i],
            key=f"resposta_inicial_{i}"
        )
    
    if st.button("Enviar Respostas", on_click=enviar_respostas_iniciais):
        enviar_respostas_iniciais()

# Fase da conversa com IA
elif st.session_state.fase == "conversa":
    # Exibir o histórico de mensagens
    for msg in st.session_state.historico:
        tipo, texto = msg.split(": ", 1)
        exibir_mensagem(tipo.strip(), texto.strip())

    # Campo para o usuário digitar a mensagem com on_change
    st.text_input(
        "Digite sua mensagem:",
        value=st.session_state.mensagem_input,
        key="mensagem_input",
        on_change=enviar_mensagem  # Processa a mensagem ao apertar "Enter"
    )