import streamlit as st
from src.database.sqlite_db import SQLiteDB

def render_criar_caso_teste():
    st.subheader("Criar Novo Caso de Teste")
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    with st.form("form_caso_teste"):
        titulo = st.text_input("Título do Caso de Teste")
        descricao = st.text_area("Descrição")
        
        # Busca suites disponíveis
        suites = db.listar_suites()
        suite_opcoes = {s["titulo"]: s["id"] for s in suites}
        suite_selecionada = st.selectbox("Suite de Teste", options=list(suite_opcoes.keys()))
        
        pre_condicoes = st.text_area("Pré-condições")
        passos = st.text_area("Passos")
        resultado_esperado = st.text_area("Resultado Esperado")
        
        status = st.selectbox(
            "Status",
            options=["Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
        )
        
        submitted = st.form_submit_button("Criar Caso de Teste")
        
        if submitted:
            if not titulo:
                st.error("O título do caso de teste é obrigatório!")
            else:
                novo_caso = {
                    "titulo": titulo,
                    "descricao": descricao,
                    "suite_id": suite_opcoes[suite_selecionada],
                    "pre_condicoes": pre_condicoes,
                    "passos_execucao": passos,
                    "resultado_esperado": resultado_esperado,
                    "prioridade": "Média",  # Valor padrão
                    "status": status
                }
                
                if db.criar_caso_teste(novo_caso):
                    st.success("Caso de teste criado com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao criar caso de teste!") 