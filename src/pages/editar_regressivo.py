import streamlit as st
import sqlite3
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_editar_regressivo():
    if 'regressivo_edicao' not in st.session_state:
        st.error("Nenhum teste regressivo selecionado para edição!")
        st.stop()
    
    st.title("Editar Teste Regressivo")
    
    # Recupera o teste regressivo da sessão
    regressivo = st.session_state['regressivo_edicao']
    regressivo_id = regressivo['id']
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Entradas para edição (fora do formulário)
    st.subheader("Informações do Teste Regressivo")
    
    # Campos básicos
    titulo = st.text_input("Título", value=regressivo['titulo'])
    descricao = st.text_area("Descrição", value=regressivo['descricao'])
    
    # Status
    status_opcoes = ["Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
    
    # Verifica se o status atual está na lista
    status_atual = regressivo['status']
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
    
    # Seleção de casos de teste
    casos_disponiveis = db.listar_casos_teste()
    casos_ids_regressivo = regressivo.get('casos_teste_ids', [])
    
    # Verifica se caso_teste_ids está disponível, caso contrário, cria uma lista vazia
    if not isinstance(casos_ids_regressivo, list):
        casos_ids_regressivo = []
    
    # Pré-seleciona os casos de teste que já estavam associados ao regressivo
    casos_selecionados = st.multiselect(
        "Casos de Teste",
        options=casos_disponiveis,
        default=[c for c in casos_disponiveis if c['id'] in casos_ids_regressivo],
        format_func=lambda x: x['titulo']
    )
    
    # Extrai os IDs dos casos selecionados
    casos_ids = [c['id'] for c in casos_selecionados]
    
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
                        UPDATE regressivos
                        SET titulo = ?,
                            descricao = ?,
                            status = ?,
                            data_atualizacao = ?
                        WHERE id = ?
                    """, (
                        titulo,
                        descricao,
                        status,
                        datetime.now(),
                        regressivo_id
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Teste regressivo atualizado com sucesso!")
                    
                    # Remover da sessão e retornar à lista
                    del st.session_state['regressivo_edicao']
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar: {str(e)}")
    
    with col2:
        if st.button("Cancelar"):
            del st.session_state['regressivo_edicao']
            st.rerun() 