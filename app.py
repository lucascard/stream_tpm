import streamlit as st
from src.pages.dashboard import render_dashboard
from src.pages.plano_teste import render_plano_teste
from src.pages.suite_teste import render_suite_teste
from src.pages.caso_teste import render_caso_teste
from src.pages.regressivo import render_regressivo
from src.pages.editar_caso_teste import render_editar_caso_teste

# Configuração da página
st.set_page_config(
    page_title="Test TPM",
    page_icon="🧪",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Menu lateral
st.sidebar.title("Test TPM")
st.sidebar.markdown("---")

# Opções do menu
menu = st.sidebar.radio(
    "Selecione uma opção:",
    ["Dashboard", "Planos de Teste", "Suítes de Teste", "Casos de Teste", "Testes Regressivos"]
)

# Renderiza a página selecionada
if menu == "Dashboard":
    render_dashboard()
elif menu == "Planos de Teste":
    render_plano_teste()
elif menu == "Suítes de Teste":
    render_suite_teste()
elif menu == "Casos de Teste":
    render_caso_teste()
elif menu == "Testes Regressivos":
    render_regressivo()

# Verifica se há um caso de teste para edição
if 'caso_edicao' in st.session_state:
    render_editar_caso_teste() 