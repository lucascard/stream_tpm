import streamlit as st
from datetime import datetime
from src.database.sqlite_db import SQLiteDB
from src.pages.criar_caso_teste import render_criar_caso_teste
from src.pages.editar_caso_teste import render_editar_caso_teste

def render_caso_teste():
    """Renderiza a página de casos de teste"""
    st.title("Casos de Teste")
    
    # Verificar se estamos em modo de edição
    if 'caso_teste_edicao' in st.session_state:
        render_editar_caso_teste()
        return
    
    # Inicializa conexão com o banco
    db = SQLiteDB()
    
    # Busca suites disponíveis
    suites = db.listar_suites()
    suite_opcoes = {s["id"]: s["titulo"] for s in suites}
    
    # Tabs para diferentes ações
    tab1, tab2 = st.tabs(["Listar Casos", "Criar Caso"])
    
    with tab1:
        st.subheader("Casos de Teste Existentes")
        
        # Busca todos os casos de teste
        casos = db.listar_casos_teste()
        
        if not casos:
            st.info("Nenhum caso de teste cadastrado.")
        else:
            for caso in casos:
                with st.expander(f"{caso['titulo']} - {caso['status']}"):
                    st.write(f"**Descrição:** {caso['descricao']}")
                    st.write(f"**Suite:** {suite_opcoes.get(caso['suite_id'], 'N/A')}")
                    st.write(f"**Pré-condições:** {caso['pre_condicoes']}")
                    st.write(f"**Passos:** {caso['passos_execucao']}")
                    st.write(f"**Resultado Esperado:** {caso['resultado_esperado']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Editar", key=f"edit_{caso['id']}"):
                            st.session_state['caso_teste_edicao'] = caso
                            st.rerun()
                    with col2:
                        if st.button("Excluir", key=f"del_{caso['id']}"):
                            if db.deletar_caso_teste(caso['id']):
                                st.success("Caso de teste excluído com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir caso de teste!")
    
    with tab2:
        render_criar_caso_teste() 