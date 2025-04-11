import streamlit as st

def render_plano_form(plano=None):
    """Renderiza o formulário de cadastro/edição de planos"""
    with st.form("plano_form"):
        st.subheader("Cadastrar/Editar Plano de Teste")
        
        # Campos do formulário
        titulo = st.text_input("Título *", value=plano["titulo"] if plano else "", key="titulo")
        descricao = st.text_area("Descrição", value=plano.get("descricao", "") if plano else "", key="descricao")
        status = st.selectbox(
            "Status",
            ["Rascunho", "Ativo", "Concluído", "Arquivado"],
            index=["Rascunho", "Ativo", "Concluído", "Arquivado"].index(plano["status"]) if plano else 0,
            key="status"
        )
        
        # Botão de submit
        submitted = st.form_submit_button("Salvar")
        
        if submitted:
            if not titulo.strip():
                st.error("O título é obrigatório!")
                return None
            return {
                "titulo": titulo,
                "descricao": descricao,
                "status": status
            }
        return None 