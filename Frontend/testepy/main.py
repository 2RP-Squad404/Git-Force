import streamlit as st
import os
import json
from datetime import datetime

# Função para gerar uma resposta com base na entrada do usuário
def gerar_resposta(mensagem):
    return f"{mensagem[::-1]}"

# Função para carregar históricos de conversas salvas
def carregar_historicos():
    arquivos = [f for f in os.listdir() if f.startswith("historico_") and f.endswith(".json")]
    conversas = {}
    for arquivo in arquivos:
        with open(arquivo, "r") as f:
            nome_conversa = arquivo.replace("historico_", "").replace(".json", "")
            conversas[nome_conversa] = json.load(f)
    return conversas

# Função para exibir mensagens com estilo diferenciado (usuário e bot)
def exibir_mensagem(tipo, mensagem):
    if tipo == "Você":
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 10px; text-align: right; margin-bottom: 10px;'>
                <strong style='color: #FFF;'>Você:</strong> {mensagem}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='padding: 10px; border-radius: 10px; text-align: left; margin-bottom: 10px;'>
                <strong style='color: #FFF;'>G-Chat:</strong> {mensagem}
            </div>
        """, unsafe_allow_html=True)

# Inicializar session_state
if "historico" not in st.session_state:
    st.session_state.historico = []
if "conversas" not in st.session_state:
    st.session_state.conversas = carregar_historicos()
if "conversa_atual" not in st.session_state:
    st.session_state.conversa_atual = "Conversa Atual"  # Nome padrão da conversa atual
if "mensagem_usuario" not in st.session_state:
    st.session_state.mensagem_usuario = ""

# Função para processar a mensagem
def enviar_mensagem():
    mensagem_usuario = st.session_state.mensagem_usuario
    if mensagem_usuario:
        st.session_state.historico.append(f"Você: {mensagem_usuario}")
        resposta = gerar_resposta(mensagem_usuario)
        st.session_state.historico.append(f"GenAI: {resposta}")
        st.session_state.mensagem_usuario = ""  # Resetar o campo de texto após o envio

# Função para salvar o histórico em um arquivo (atualiza se já existir)
def salvar_historico():
    if st.session_state.historico:  # Verifica se a conversa tem mensagens
        nome_arquivo = f"historico_{st.session_state.conversa_atual}.json"
        with open(nome_arquivo, 'w') as f:
            json.dump(st.session_state.historico, f)
        st.success(f"Histórico da conversa '{st.session_state.conversa_atual}' salvo com sucesso!")
    else:
        st.warning("A conversa está vazia. Não é possível salvar uma conversa sem mensagens.")

# Função para excluir a conversa e o arquivo associado
def excluir_conversa():
    nome_conversa = st.session_state.conversa_atual
    nome_arquivo = f"historico_{nome_conversa}.json"
    
    # Excluir o arquivo da conversa
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        st.success(f"Conversa '{nome_conversa}' e arquivo '{nome_arquivo}' excluídos com sucesso!")
    else:
        st.warning(f"O arquivo '{nome_arquivo}' não foi encontrado.")

    # Remover conversa da session_state e limpar histórico
    if nome_conversa in st.session_state.conversas:
        del st.session_state.conversas[nome_conversa]
    st.session_state.historico = []
    st.session_state.conversa_atual = "Conversa Atual"  # Definir uma conversa padrão

# Função para criar uma nova conversa
def criar_nova_conversa(novo_nome):
    if novo_nome and novo_nome not in st.session_state.conversas:
        st.session_state.conversas[novo_nome] = []
        st.session_state.conversa_atual = novo_nome
        st.session_state.historico = []
        st.success(f"Nova conversa '{novo_nome}' criada!")
    else:
        st.warning("O nome da conversa já existe ou está vazio.")

# Função para selecionar uma conversa
def selecionar_conversa(nome):
    st.session_state.conversa_atual = nome
    st.session_state.historico = st.session_state.conversas.get(nome, [])

# Função para renomear a conversa
def renomear_conversa(novo_nome):
    conversa_atual = st.session_state.conversa_atual
    if novo_nome and novo_nome not in st.session_state.conversas:
        # Renomear o arquivo do histórico da conversa, se existir
        nome_arquivo_antigo = f"historico_{conversa_atual}.json"
        nome_arquivo_novo = f"historico_{novo_nome}.json"
        if os.path.exists(nome_arquivo_antigo):
            os.rename(nome_arquivo_antigo, nome_arquivo_novo)

        # Atualizar o dicionário de conversas
        st.session_state.conversas[novo_nome] = st.session_state.conversas.pop(conversa_atual)

        # Atualizar a conversa atual e o histórico
        st.session_state.conversa_atual = novo_nome
        st.success(f"Conversa '{conversa_atual}' renomeada para '{novo_nome}'!")
    else:
        st.warning("O nome da conversa já existe ou está vazio.")

# Interface principal
st.title("G-Chat")

# Exibir a conversa acima da caixa de texto
st.header(f"Conversa: {st.session_state.conversa_atual}")
for msg in st.session_state.historico:
    tipo, texto = msg.split(": ", 1)
    exibir_mensagem(tipo.strip(), texto.strip())

# Caixa de entrada para o usuário
st.text_input(
    "Digite sua mensagem:",
    value=st.session_state.mensagem_usuario,
    on_change=enviar_mensagem,
    key="mensagem_usuario"
)

# Sidebar
st.sidebar.title("Gerenciar Conversas")

# Campo para criar nova conversa
novo_nome = st.sidebar.text_input("Nome da nova conversa:")
if st.sidebar.button("Criar Nova Conversa"):
    criar_nova_conversa(novo_nome)

# Exibir conversas salvas na sidebar
st.sidebar.markdown("### Suas Conversas")
for conversa in st.session_state.conversas.keys():
    if st.sidebar.button(f"Selecionar '{conversa}'"):
        selecionar_conversa(conversa)

# Campo para renomear a conversa atual
novo_nome_renomear = st.sidebar.text_input("Novo nome para a conversa:")
if st.sidebar.button("Renomear Conversa"):
    renomear_conversa(novo_nome_renomear)

# Opções para a conversa atual
if st.session_state.conversa_atual:
    if st.sidebar.button("Salvar Histórico"):
        salvar_historico()
    if st.sidebar.button("Excluir Histórico"):
        excluir_conversa()