import streamlit as st
from src.database.sqlite_db import SQLiteDB

def render_dashboard():
    """Renderiza o dashboard principal"""
    st.title("Dashboard")
    
    # Inicializa conexão com o banco de dados
    db = SQLiteDB()
    
    # Obtém dados para o dashboard
    planos = db.listar_planos()
    suites = db.listar_suites()
    casos = db.listar_casos_teste()
    regressivos = db.listar_regressivos()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Planos", len(planos))
    with col2:
        st.metric("Total de Suítes", len(suites))
    with col3:
        st.metric("Total de Casos", len(casos))
    with col4:
        st.metric("Total de Regressivos", len(regressivos))
    
    # Tabela dos últimos planos de teste
    st.subheader("Últimos Planos de Teste")
    if planos:
        for plano in planos[:5]:  # Mostra apenas os 5 últimos planos
            st.write(f"**{plano['titulo']}** - {plano['status']}")
            st.write(f"Data de criação: {plano['data_criacao']}")
            st.write("---")
    else:
        st.info("Nenhum plano de teste encontrado.") 