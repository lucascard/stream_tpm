import streamlit as st
import sqlite3
from datetime import datetime
from src.database.sqlite_db import SQLiteDB

def render_editar_plano_teste():
    if 'plano_edicao' not in st.session_state:
        st.error("Nenhum plano de teste selecionado para edição!")
        st.stop()
    
    st.title("Editar Plano de Teste")
    
    # Recupera o plano da sessão
    plano = st.session_state['plano_edicao']
    plano_id = plano['id']
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Entradas para edição (fora do formulário)
    st.subheader("Informações do Plano de Teste")
    
    # Campos básicos
    titulo = st.text_input("Título", value=plano['titulo'])
    descricao = st.text_area("Descrição", value=plano['descricao'])
    
    # Status
    status_opcoes = ["Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
    
    # Verifica se o status atual está na lista
    status_atual = plano['status']
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
                        UPDATE planos_teste
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
                        plano_id
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Plano de teste atualizado com sucesso!")
                    
                    # Remover da sessão e retornar à lista
                    del st.session_state['plano_edicao']
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao atualizar: {str(e)}")
    
    with col2:
        if st.button("Cancelar"):
            del st.session_state['plano_edicao']
            st.rerun() 