import streamlit as st

def render_topbar():
    """Renderiza a barra superior da aplicação"""
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.image("https://img.icons8.com/color/48/000000/test-tube.png", width=50)
        
        with col2:
            st.title("Sistema de Planos de Teste")
        
        with col3:
            st.write("")
            if st.button("🔄 Atualizar"):
                st.experimental_rerun() 