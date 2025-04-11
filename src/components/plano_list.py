import streamlit as st
from datetime import datetime

def format_date(date):
    """Formata a data para exibição"""
    if isinstance(date, datetime):
        return date.strftime("%d/%m/%Y %H:%M")
    return ""

def render_plano_list(planos, status_filter=None):
    """Renderiza a listagem de planos de teste"""
    st.subheader("Planos de Teste")
    
    if not planos:
        st.info("Nenhum plano de teste cadastrado.")
        return None, None
    
    # Filtra os planos pelo status selecionado
    if status_filter:
        planos = [p for p in planos if p["status"] in status_filter]
    
    for plano in planos:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 4, 2, 1, 1])
            
            with col1:
                st.write(f"**{plano['titulo']}**")
            with col2:
                st.write(plano.get('descricao', ''))
            with col3:
                st.write(f"Status: {plano['status']}")
                st.caption(f"Criado em: {format_date(plano.get('data_criacao'))}")
            with col4:
                if st.button("✏️", key=f"edit_{plano['_id']}"):
                    return "edit", plano
            with col5:
                if st.button("🗑️", key=f"delete_{plano['_id']}"):
                    return "delete", plano
            
            st.divider()
    
    return None, None 