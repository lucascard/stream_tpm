import streamlit as st
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_caso_teste():
    """Renderiza a página de casos de teste"""
    st.title("Casos de Teste")
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Cria duas abas: uma para criar e outra para listar
    tab1, tab2 = st.tabs(["Criar Caso", "Listar Casos"])
    
    with tab1:
        st.header("Criar Novo Caso de Teste")
        
        with st.form("form_caso_teste"):
            nome = st.text_input("Nome do Caso de Teste")
            descricao = st.text_area("Descrição")
            
            # Busca suites disponíveis
            suites = db.listar_suites()
            suite_opcoes = {s["titulo"]: s["id"] for s in suites}
            suite_selecionada = st.selectbox("Suite de Teste", options=list(suite_opcoes.keys()))
            
            pre_condicoes = st.text_area("Pré-condições")
            passos_execucao = st.text_area("Passos para Execução")
            resultado_esperado = st.text_area("Resultado Esperado")
            
            col1, col2 = st.columns(2)
            with col1:
                prioridade = st.selectbox(
                    "Prioridade",
                    options=["Baixa", "Média", "Alta", "Crítica"]
                )
            with col2:
                status = st.selectbox(
                    "Status",
                    options=["Não Executado", "Em Execução", "Passou", "Falhou", "Bloqueado"]
                )
            
            submitted = st.form_submit_button("Criar Caso de Teste")
            
            if submitted:
                if not nome:
                    st.error("O nome do caso de teste é obrigatório!")
                else:
                    novo_caso = {
                        "titulo": nome,
                        "descricao": descricao,
                        "suite_id": suite_opcoes[suite_selecionada],
                        "pre_condicoes": pre_condicoes,
                        "passos_execucao": passos_execucao,
                        "resultado_esperado": resultado_esperado,
                        "prioridade": prioridade,
                        "status": status
                    }
                    
                    if db.criar_caso_teste(novo_caso):
                        st.success("Caso de teste criado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar caso de teste!")
    
    with tab2:
        st.header("Casos de Teste Existentes")
        
        casos = db.listar_casos_teste()
        if casos:
            for caso in casos:
                with st.expander(f"{caso['titulo']} - {caso['status']}"):
                    st.write(f"**Descrição:** {caso['descricao']}")
                    st.write(f"**Suite:** {suite_opcoes.get(caso['suite_id'], 'N/A')}")
                    st.write(f"**Pré-condições:** {caso['pre_condicoes']}")
                    st.write(f"**Passos para Execução:** {caso['passos_execucao']}")
                    st.write(f"**Resultado Esperado:** {caso['resultado_esperado']}")
                    st.write(f"**Prioridade:** {caso['prioridade']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_{caso['id']}"):
                            st.session_state['caso_edicao'] = caso
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"del_{caso['id']}"):
                            if db.deletar_caso_teste(caso['id']):
                                st.success("Caso de teste excluído com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir caso de teste!")
        else:
            st.info("Nenhum caso de teste encontrado.") 