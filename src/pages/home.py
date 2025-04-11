import streamlit as st
from src.database.sqlite_db import SQLiteDB

def render_home():
    st.title("Bem-vindo ao Test TPM")
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Obtém estatísticas
    planos = db.listar_planos()
    suites = db.listar_suites()
    casos = db.listar_casos_teste()
    regressivos = db.listar_regressivos()
    
    # Exibe estatísticas em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Planos", len(planos))
    with col2:
        st.metric("Total de Suítes", len(suites))
    with col3:
        st.metric("Total de Casos", len(casos))
    with col4:
        st.metric("Total de Regressivos", len(regressivos))
    
    # Informações sobre o sistema
    st.markdown("""
        ## Sobre o Sistema
        
        O Test TPM é uma ferramenta para gerenciamento de testes, que permite:
        
        - Criar e gerenciar planos de teste
        - Organizar suítes de teste
        - Documentar casos de teste
        - Acompanhar testes regressivos
        
        ### Como Começar
        
        1. Use o menu lateral para navegar entre as funcionalidades
        2. Comece criando um plano de teste
        3. Adicione suítes ao seu plano
        4. Crie casos de teste dentro das suítes
        5. Acompanhe a execução dos testes
        
        ### Precisa de Ajuda?
        
        - Consulte a documentação
        - Entre em contato com o suporte
        - Reporte problemas
    """)
    
    # Últimas atualizações
    st.subheader("Últimas Atualizações")
    
    if planos:
        st.write("**Últimos Planos Criados:**")
        for plano in planos[:3]:
            st.write(f"- {plano['titulo']} ({plano['status']})")
    
    if casos:
        st.write("**Últimos Casos de Teste:**")
        for caso in casos[:3]:
            st.write(f"- {caso['titulo']} ({caso['status']})") 