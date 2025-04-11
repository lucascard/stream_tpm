import streamlit as st
import sqlite3
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_editar_caso_teste():
    if 'caso_teste_edicao' not in st.session_state:
        st.error("Nenhum caso de teste selecionado para edição!")
        st.stop()
    
    st.title("Editar Caso de Teste")
    
    # Recupera o caso de teste da sessão
    caso_teste = st.session_state['caso_teste_edicao']
    caso_id = caso_teste['id']
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Busca suites disponíveis
    suites = db.listar_suites()
    
    # Preparar lista de suítes para o selectbox
    suite_nomes = []
    suite_ids = []
    suite_index = 0
    
    for i, suite in enumerate(suites):
        suite_nomes.append(suite["titulo"])
        suite_ids.append(suite["id"])
        if suite["id"] == caso_teste['suite_id']:
            suite_index = i
    
    # Entradas para edição (fora do formulário)
    st.subheader("Informações do Caso de Teste")
    
    # Campos básicos
    titulo = st.text_input("Título", value=caso_teste['titulo'])
    descricao = st.text_area("Descrição", value=caso_teste['descricao'])
    
    # Seleção da suíte
    suite_selecionada = st.selectbox(
        "Suite de Teste",
        options=suite_nomes,
        index=suite_index
    )
    
    # ID da suíte selecionada
    suite_id = suite_ids[suite_nomes.index(suite_selecionada)]
    
    # Outros campos
    pre_condicoes = st.text_area("Pré-condições", value=caso_teste['pre_condicoes'])
    passos_execucao = st.text_area("Passos", value=caso_teste['passos_execucao'])
    resultado_esperado = st.text_area("Resultado Esperado", value=caso_teste['resultado_esperado'])
    
    # Status e prioridade
    col1, col2 = st.columns(2)
    with col1:
        # Lista de status com opção adicional "Não Executado"
        status_opcoes = ["Não Iniciado", "Em Andamento", "Concluído", "Cancelado", "Não Executado"]
        
        # Verifica se o status atual está na lista, se não estiver usa o primeiro
        status_atual = caso_teste['status']
        status_index = 0
        
        try:
            status_index = status_opcoes.index(status_atual)
        except ValueError:
            # Se o status não estiver na lista, usa o primeiro da lista
            pass
        
        status = st.selectbox(
            "Status",
            options=status_opcoes,
            index=status_index
        )
    with col2:
        # Lista de prioridades
        prioridade_opcoes = ["Baixa", "Média", "Alta", "Crítica"]
        
        # Verifica se a prioridade atual está na lista
        prioridade_atual = caso_teste.get('prioridade', 'Média')
        prioridade_index = 1  # Padrão Média
        
        try:
            prioridade_index = prioridade_opcoes.index(prioridade_atual)
        except ValueError:
            # Se a prioridade não estiver na lista, usa Média
            pass
        
        prioridade = st.selectbox(
            "Prioridade",
            options=prioridade_opcoes,
            index=prioridade_index
        )
    
    # Botões de ação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Salvar Alterações"):
            if not titulo:
                st.error("O título é obrigatório!")
            else:
                try:
                    # Conexão direta com o banco
                    conn = sqlite3.connect("database/test_tpm.db")
                    cursor = conn.cursor()
                    
                    # Executar a atualização direta
                    cursor.execute("""
                        UPDATE casos_teste
                        SET titulo = ?,
                            descricao = ?,
                            suite_id = ?,
                            pre_condicoes = ?,
                            passos_execucao = ?,
                            resultado_esperado = ?,
                            status = ?,
                            prioridade = ?,
                            data_atualizacao = ?
                        WHERE id = ?
                    """, (
                        titulo,
                        descricao,
                        suite_id,
                        pre_condicoes,
                        passos_execucao,
                        resultado_esperado,
                        status,
                        prioridade,
                        datetime.now(),
                        caso_id
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Caso de teste atualizado com sucesso!")
                    
                    # Remover da sessão e retornar à lista
                    del st.session_state['caso_teste_edicao']
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar: {str(e)}")
    
    with col2:
        if st.button("Cancelar"):
            del st.session_state['caso_teste_edicao']
            st.rerun() 