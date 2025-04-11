import streamlit as st
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    
    # Criar tabela de pastas de documentação
    c.execute('''
        CREATE TABLE IF NOT EXISTS pastas_documentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            regras TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Criar tabela de associação entre pastas e casos de teste
    c.execute('''
        CREATE TABLE IF NOT EXISTS pasta_casos_teste (
            pasta_id INTEGER,
            caso_teste_id INTEGER,
            ordem INTEGER,
            FOREIGN KEY (pasta_id) REFERENCES pastas_documentacao (id),
            FOREIGN KEY (caso_teste_id) REFERENCES casos_teste (id),
            PRIMARY KEY (pasta_id, caso_teste_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def criar_pasta(nome, regras):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('INSERT INTO pastas_documentacao (nome, regras) VALUES (?, ?)',
              (nome, regras))
    conn.commit()
    conn.close()

def listar_pastas():
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('SELECT id, nome, regras, data_criacao FROM pastas_documentacao ORDER BY data_criacao DESC')
    pastas = c.fetchall()
    conn.close()
    return pastas

def adicionar_caso_teste_pasta(pasta_id, caso_teste_id, ordem):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('INSERT INTO pasta_casos_teste (pasta_id, caso_teste_id, ordem) VALUES (?, ?, ?)',
              (pasta_id, caso_teste_id, ordem))
    conn.commit()
    conn.close()

def listar_casos_teste_pasta(pasta_id):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('''
        SELECT ct.id, ct.titulo, ct.descricao, pct.ordem 
        FROM casos_teste ct
        JOIN pasta_casos_teste pct ON ct.id = pct.caso_teste_id
        WHERE pct.pasta_id = ?
        ORDER BY pct.ordem
    ''', (pasta_id,))
    casos = c.fetchall()
    conn.close()
    return casos

def main():
    st.title("📚 Documentação")
    
    # Inicializar banco de dados
    init_db()
    
    # Criar tabs para edição e visualização
    tab1, tab2 = st.tabs(["✏️ Edição", "👀 Visualização"])
    
    with tab1:
        st.header("Edição de Documentação")
        
        # Formulário para criar nova pasta
        with st.form("nova_pasta"):
            st.subheader("Nova Pasta de Documentação")
            nome_pasta = st.text_input("Nome da Pasta")
            regras = st.text_area("Regras da Pasta")
            
            if st.form_submit_button("Criar Pasta"):
                if nome_pasta:
                    criar_pasta(nome_pasta, regras)
                    st.success("Pasta criada com sucesso!")
                else:
                    st.error("Por favor, insira um nome para a pasta.")
        
        # Lista de pastas existentes
        st.subheader("Pastas Existentes")
        pastas = listar_pastas()
        
        for pasta in pastas:
            with st.expander(f"📁 {pasta[1]}"):
                st.write(f"**Regras:** {pasta[2]}")
                st.write(f"**Data de Criação:** {pasta[3]}")
                
                # Adicionar casos de teste à pasta
                st.subheader("Adicionar Caso de Teste")
                casos_teste = listar_casos_teste_pasta(pasta[0])
                
                # TODO: Implementar seleção de casos de teste e ordem
                # TODO: Implementar visualização dos casos já adicionados
    
    with tab2:
        st.header("Visualização de Documentação")
        
        # Lista de pastas para visualização
        pastas = listar_pastas()
        
        for pasta in pastas:
            with st.expander(f"📁 {pasta[1]}"):
                st.write(f"**Regras:** {pasta[2]}")
                st.write(f"**Data de Criação:** {pasta[3]}")
                
                # Listar casos de teste da pasta
                st.subheader("Casos de Teste")
                casos = listar_casos_teste_pasta(pasta[0])
                
                for caso in casos:
                    with st.expander(f"🔍 {caso[1]}"):
                        st.write(caso[2])

if __name__ == "__main__":
    main() 