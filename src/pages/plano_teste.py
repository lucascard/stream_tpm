import streamlit as st
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_plano_teste():
    st.title("Planos de Teste")
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Cria duas abas: uma para criar e outra para listar
    tab1, tab2 = st.tabs(["Criar Plano", "Listar Planos"])
    
    with tab1:
        st.header("Criar Novo Plano de Teste")
        
        with st.form("form_plano_teste"):
            titulo = st.text_input("Título do Plano")
            descricao = st.text_area("Descrição")
            status = st.selectbox(
                "Status",
                options=["Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
            )
            
            submitted = st.form_submit_button("Criar Plano de Teste")
            
            if submitted:
                if not titulo:
                    st.error("O título do plano é obrigatório!")
                else:
                    if db.inserir_plano(titulo, descricao, status):
                        st.success("Plano de teste criado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar plano de teste!")
    
    with tab2:
        st.header("Planos de Teste Existentes")
        
        planos = db.listar_planos()
        if planos:
            for plano in planos:
                with st.expander(f"{plano['titulo']} - {plano['status']}"):
                    st.write(f"**Descrição:** {plano['descricao']}")
                    st.write(f"**Data de Criação:** {plano['data_criacao']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_{plano['id']}"):
                            st.session_state['plano_edicao'] = plano
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"del_{plano['id']}"):
                            if db.excluir_plano(plano['id']):
                                st.success("Plano de teste excluído com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir plano de teste!")
        else:
            st.info("Nenhum plano de teste encontrado.") 