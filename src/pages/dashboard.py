import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from src.database.sqlite_db import SQLiteDB

def render_dashboard():
    """Renderiza o dashboard principal"""
    st.title("📊 Dashboard")
    
    # Inicializa conexão com o banco de dados
    db = SQLiteDB()
    
    # Obtém dados para o dashboard
    planos = db.listar_planos()
    suites = db.listar_suites()
    casos = db.listar_casos_teste()
    regressivos = db.listar_regressivos()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Planos",
            len(planos),
            delta=f"+{len([p for p in planos if (datetime.now() - datetime.strptime(p['data_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days < 7])} esta semana"
        )
    with col2:
        st.metric(
            "Total de Suítes",
            len(suites),
            delta=f"+{len([s for s in suites if (datetime.now() - datetime.strptime(s['data_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days < 7])} esta semana"
        )
    with col3:
        st.metric(
            "Total de Casos",
            len(casos),
            delta=f"+{len([c for c in casos if (datetime.now() - datetime.strptime(c['data_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days < 7])} esta semana"
        )
    with col4:
        st.metric(
            "Total de Regressivos",
            len(regressivos),
            delta=f"+{len([r for r in regressivos if (datetime.now() - datetime.strptime(r['data_criacao'], '%Y-%m-%d %H:%M:%S.%f')).days < 7])} esta semana"
        )
    
    # Gráficos e análises
    col1, col2 = st.columns(2)
    
    with col1:
        # Status dos casos de teste
        if casos:
            status_counts = pd.DataFrame(casos)['status'].value_counts()
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Status dos Casos de Teste",
                hole=0.4
            )
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.info("Nenhum caso de teste encontrado para análise.")
    
    with col2:
        # Prioridade dos casos de teste
        if casos:
            prioridade_counts = pd.DataFrame(casos)['prioridade'].value_counts()
            fig_prioridade = px.bar(
                x=prioridade_counts.index,
                y=prioridade_counts.values,
                title="Casos por Prioridade",
                labels={'x': 'Prioridade', 'y': 'Quantidade'}
            )
            st.plotly_chart(fig_prioridade, use_container_width=True)
        else:
            st.info("Nenhum caso de teste encontrado para análise.")
    
    # Últimos planos de teste
    st.subheader("📋 Últimos Planos de Teste")
    if planos:
        # Converte para DataFrame para melhor manipulação
        df_planos = pd.DataFrame(planos)
        df_planos['data_criacao'] = pd.to_datetime(df_planos['data_criacao'])
        df_planos = df_planos.sort_values('data_criacao', ascending=False).head(5)
        
        for _, plano in df_planos.iterrows():
            with st.expander(f"**{plano['titulo']}** - {plano['status']}"):
                st.write(f"**Descrição:** {plano['descricao']}")
                st.write(f"**Data de criação:** {plano['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
                st.write(f"**Última atualização:** {plano['data_atualizacao']}")
    else:
        st.info("Nenhum plano de teste encontrado.")
    
    # Casos de teste recentes
    st.subheader("✅ Casos de Teste Recentes")
    if casos:
        # Converte para DataFrame para melhor manipulação
        df_casos = pd.DataFrame(casos)
        df_casos['data_criacao'] = pd.to_datetime(df_casos['data_criacao'])
        df_casos = df_casos.sort_values('data_criacao', ascending=False).head(5)
        
        for _, caso in df_casos.iterrows():
            with st.expander(f"**{caso['titulo']}** - {caso['status']}"):
                st.write(f"**Suite:** {caso['suite_id']}")
                st.write(f"**Prioridade:** {caso['prioridade']}")
                st.write(f"**Data de criação:** {caso['data_criacao'].strftime('%d/%m/%Y %H:%M')}")
    else:
        st.info("Nenhum caso de teste encontrado.") 