import streamlit as st
from src.pages.dashboard import render_dashboard
from src.pages.plano_teste import render_plano_teste
from src.pages.suite_teste import render_suite_teste
from src.pages.caso_teste import render_caso_teste
from src.pages.regressivo import render_regressivo
from src.pages.editar_caso_teste import render_editar_caso_teste
from src.pages.documentacao import main as render_documentacao

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
    /* Estilo da Sidebar */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    .sidebar-title {
        color: #262730;
        font-size: 24px;
        font-weight: bold;
        padding: 20px 0;
        text-align: center;
    }
    .sidebar-subtitle {
        color: #666666;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
    }
    .menu-item {
        padding: 10px 15px;
        margin: 5px 0;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .menu-item:hover {
        background-color: #e6e9ef;
    }
    .menu-item.selected {
        background-color: #e6e9ef;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Menu lateral
st.sidebar.markdown('<p class="sidebar-title">Test TPM</p>', unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-subtitle">Sistema de Gerenciamento de Testes</p>', unsafe_allow_html=True)
st.sidebar.markdown("---")

# Opções do menu com ícones
menu = st.sidebar.radio(
    "Navegação",
    ["📊 Dashboard", "📋 Planos de Teste", "🧪 Suítes de Teste", "✅ Casos de Teste", "🔄 Testes Regressivos", "📚 Documentação"],
    label_visibility="collapsed"
)

# Renderiza a página selecionada
if menu == "📊 Dashboard":
    render_dashboard()
elif menu == "📋 Planos de Teste":
    render_plano_teste()
elif menu == "🧪 Suítes de Teste":
    render_suite_teste()
elif menu == "✅ Casos de Teste":
    render_caso_teste()
elif menu == "🔄 Testes Regressivos":
    render_regressivo()
elif menu == "📚 Documentação":
    render_documentacao()

# Verifica se há um caso de teste para edição
if 'caso_edicao' in st.session_state:
    render_editar_caso_teste() 