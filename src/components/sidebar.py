import streamlit as st

def render_sidebar():
    """Renderiza a barra lateral da aplicação"""
    st.sidebar.title("Test TPM")
    st.sidebar.markdown("---")
    
    # Filtros
    status_filter = st.sidebar.selectbox(
        "Filtrar por Status",
        ["Todos", "Não Iniciado", "Em Andamento", "Concluído", "Cancelado"]
    )
    
    # Estatísticas
    st.sidebar.subheader("Estatísticas")
    st.sidebar.metric("Total de Planos", "0")
    st.sidebar.metric("Planos Ativos", "0")
    
    # Informações
    st.sidebar.subheader("Informações")
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        ### Sobre o Sistema
        
        Test TPM é um sistema de gerenciamento 
        de testes que permite criar e acompanhar:
        
        - Planos de Teste
        - Suítes de Teste
        - Casos de Teste
        - Testes Regressivos
        
        Desenvolvido com Streamlit e SQLite.
    """)
    
    return status_filter 