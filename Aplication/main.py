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
        # Exibir mensagem do bot usando Markdown diretamente
        st.markdown(f"**GenAI:**\n\n{mensagem}")

# Inicializar session_state
if "historico" not in st.session_state:
    st.session_state.historico = []
if "fase" not in st.session_state:
    st.session_state.fase = "perguntas_iniciais"  # Fase inicial como padrão
if "respostas_iniciais" not in st.session_state:
    st.session_state.respostas_iniciais = [""] * 4
if "mensagem_input" not in st.session_state:
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

    # Limpar o campo de input sem modificar diretamente o session_state
    st.session_state.mensagem_input = ""  # Isto já atualiza a interface automaticamente

# Verificação das respostas iniciais e transição para o chat normal
def enviar_respostas_iniciais():
    # Obter as respostas atuais
    respostas_atualizadas = [
        st.session_state[f"resposta_inicial_{i}"] for i in range(4)
    ]
    
    # Verificar se todas as respostas foram preenchidas
    if all(resposta != "" for resposta in respostas_atualizadas):
        # Salvar as respostas nas variáveis do session_state
        st.session_state.dataset = respostas_atualizadas[0]
        st.session_state.table = respostas_atualizadas[1]
        st.session_state.target_dataset = respostas_atualizadas[2]
        st.session_state.name_view = respostas_atualizadas[3]
        
        # Mudar para a fase de conversa
        st.session_state.fase = "conversa"
        st.session_state.historico = []  # Limpa o histórico para o chat normal
    else:
        st.warning("Por favor, preencha todos os campos antes de enviar.")

# Fase das perguntas iniciais
if st.session_state.fase == "perguntas_iniciais":
    st.header("Responda as perguntas abaixo:")
    
    for i, pergunta in enumerate(perguntas_iniciais):
        st.session_state.respostas_iniciais[i] = st.text_input(
            pergunta,
            value=st.session_state.respostas_iniciais[i],
            key=f"resposta_inicial_{i}"
        )

    # Botão para enviar as respostas
    if st.button("Enviar Respostas"):
        enviar_respostas_iniciais()

# Fase da conversa normal
elif st.session_state.fase == "conversa":
    st.header("Conversa com GenAI")
    
    # Exibir o histórico de mensagens
    for msg in st.session_state.historico:
        tipo, texto = msg.split(": ", 1)
        exibir_mensagem(tipo.strip(), texto.strip())

    # Campo para o usuário digitar a mensagem com on_change
    mensagem_usuario = st.text_input(
        "Digite sua mensagem:",
        value=st.session_state.mensagem_input,
        key="mensagem_input",
        on_change=enviar_mensagem  # Processa a mensagem automaticamente ao apertar "Enter"
    )
