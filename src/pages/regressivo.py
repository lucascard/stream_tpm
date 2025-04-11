import streamlit as st
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_regressivo():
    st.title("Testes Regressivos")
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Cria duas abas: uma para listar e outra para criar
    tab1, tab2 = st.tabs(["Listar Regressivos", "Criar Regressivo"])
    
    with tab1:
        st.header("Testes Regressivos Existentes")
        
        regressivos = db.listar_regressivos()
        if regressivos:
            for regressivo in regressivos:
                with st.expander(f"{regressivo['titulo']} - {regressivo['status']}"):
                    st.write(f"**Descrição:** {regressivo['descricao']}")
                    st.write(f"**Data de Criação:** {regressivo['data_criacao']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_{regressivo['id']}"):
                            st.session_state['regressivo_edicao'] = regressivo
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"del_{regressivo['id']}"):
                            if db.excluir_regressivo(regressivo['id']):
                                st.success("Teste regressivo excluído com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir teste regressivo!")
        else:
            st.info("Nenhum teste regressivo encontrado.")
    
    with tab2:
        st.header("Criar Novo Teste Regressivo")
        
        with st.form("form_regressivo"):
            titulo = st.text_input("Título do Teste Regressivo")
            descricao = st.text_area("Descrição")
            status = st.selectbox(
                "Status",
                options=["Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
            )
            
            submitted = st.form_submit_button("Criar Teste Regressivo")
            
            if submitted:
                if not titulo:
                    st.error("O título do teste regressivo é obrigatório!")
                else:
                    if db.inserir_regressivo(titulo, descricao, status):
                        st.success("Teste regressivo criado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar teste regressivo!") 