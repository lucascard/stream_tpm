import streamlit as st
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_editar_caso_teste():
    if 'caso_edicao' not in st.session_state:
        st.error("Nenhum caso de teste selecionado para edição!")
        st.stop()
    
    st.title("Editar Caso de Teste")
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    caso = st.session_state['caso_edicao']
    
    with st.form("form_editar_caso"):
        nome = st.text_input("Nome do Caso de Teste", value=caso['titulo'])
        descricao = st.text_area("Descrição", value=caso['descricao'])
        
        # Busca suites disponíveis
        suites = db.listar_suites()
        suite_opcoes = {s["titulo"]: s["id"] for s in suites}
        suite_atual = next((titulo for titulo, id in suite_opcoes.items() if id == caso['suite_id']), None)
        suite_selecionada = st.selectbox("Suite de Teste", options=list(suite_opcoes.keys()), index=list(suite_opcoes.keys()).index(suite_atual) if suite_atual else 0)
        
        pre_condicoes = st.text_area("Pré-condições", value=caso['pre_condicoes'])
        passos_execucao = st.text_area("Passos para Execução", value=caso['passos_execucao'])
        resultado_esperado = st.text_area("Resultado Esperado", value=caso['resultado_esperado'])
        
        col1, col2 = st.columns(2)
        with col1:
            prioridade = st.selectbox(
                "Prioridade",
                options=["Baixa", "Média", "Alta", "Crítica"],
                index=["Baixa", "Média", "Alta", "Crítica"].index(caso['prioridade'])
            )
        with col2:
            status = st.selectbox(
                "Status",
                options=["Não Executado", "Em Execução", "Passou", "Falhou", "Bloqueado"],
                index=["Não Executado", "Em Execução", "Passou", "Falhou", "Bloqueado"].index(caso['status'])
            )
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Salvar Alterações")
        with col2:
            if st.form_submit_button("Cancelar"):
                del st.session_state['caso_edicao']
                st.rerun()
        
        if submitted:
            if not nome:
                st.error("O nome do caso de teste é obrigatório!")
            else:
                dados_atualizados = {
                    "titulo": nome,
                    "descricao": descricao,
                    "suite_id": suite_opcoes[suite_selecionada],
                    "pre_condicoes": pre_condicoes,
                    "passos_execucao": passos_execucao,
                    "resultado_esperado": resultado_esperado,
                    "prioridade": prioridade,
                    "status": status
                }
                
                if db.atualizar_caso_teste(caso['id'], dados_atualizados):
                    st.success("Caso de teste atualizado com sucesso!")
                    del st.session_state['caso_edicao']
                    st.rerun()
                else:
                    st.error("Erro ao atualizar caso de teste!") 