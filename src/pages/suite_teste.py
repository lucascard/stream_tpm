import streamlit as st
from datetime import datetime
from src.database.sqlite_db import SQLiteDB
from src.pages.editar_suite_teste import render_editar_suite_teste

def render_suite_teste():
    st.title("Suítes de Teste")
    
    # Verificar se estamos em modo de edição
    if 'suite_edicao' in st.session_state:
        render_editar_suite_teste()
        return
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Cria duas abas: uma para listar e outra para criar
    tab1, tab2 = st.tabs(["Listar Suítes", "Criar Suíte"])
    
    with tab1:
        st.header("Suítes de Teste Existentes")
        
        suites = db.listar_suites()
        if suites:
            for suite in suites:
                with st.expander(f"{suite['titulo']} - {suite['status']}"):
                    st.write(f"**Descrição:** {suite['descricao']}")
                    st.write(f"**Data de Criação:** {suite['data_criacao']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_{suite['id']}"):
                            st.session_state['suite_edicao'] = suite
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"del_{suite['id']}"):
                            if db.excluir_suite(suite['id']):
                                st.success("Suíte de teste excluída com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir suíte de teste!")
        else:
            st.info("Nenhuma suíte de teste encontrada.")
    
    with tab2:
        st.header("Criar Nova Suíte de Teste")
        
        with st.form("form_suite_teste"):
            titulo = st.text_input("Título da Suíte")
            descricao = st.text_area("Descrição")
            status = st.selectbox(
                "Status",
                options=["Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
            )
            
            submitted = st.form_submit_button("Criar Suíte de Teste")
            
            if submitted:
                if not titulo:
                    st.error("O título da suíte é obrigatório!")
                else:
                    if db.inserir_suite(titulo, descricao, status):
                        st.success("Suíte de teste criada com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar suíte de teste!") 