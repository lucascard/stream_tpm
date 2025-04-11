import streamlit as st
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    
    # Verificar se a tabela existe
    c.execute('''
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='pastas_documentacao'
    ''')
    tabela_existe = c.fetchone() is not None
    
    if not tabela_existe:
        # Criar tabela de pastas de documentação
        c.execute('''
            CREATE TABLE pastas_documentacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                regras TEXT,
                pasta_pai_id INTEGER,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (pasta_pai_id) REFERENCES pastas_documentacao (id)
            )
        ''')
    else:
        # Verificar se a coluna pasta_pai_id existe
        c.execute('PRAGMA table_info(pastas_documentacao)')
        colunas = [coluna[1] for coluna in c.fetchall()]
        
        if 'pasta_pai_id' not in colunas:
            # Adicionar a coluna pasta_pai_id
            c.execute('ALTER TABLE pastas_documentacao ADD COLUMN pasta_pai_id INTEGER')
            # Adicionar a chave estrangeira
            c.execute('''
                CREATE TABLE temp_pastas_documentacao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    regras TEXT,
                    pasta_pai_id INTEGER,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (pasta_pai_id) REFERENCES pastas_documentacao (id)
                )
            ''')
            c.execute('INSERT INTO temp_pastas_documentacao (id, nome, regras, data_criacao) SELECT id, nome, regras, data_criacao FROM pastas_documentacao')
            c.execute('DROP TABLE pastas_documentacao')
            c.execute('ALTER TABLE temp_pastas_documentacao RENAME TO pastas_documentacao')
    
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

def criar_pasta(nome, regras, pasta_pai_id=None):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('INSERT INTO pastas_documentacao (nome, regras, pasta_pai_id) VALUES (?, ?, ?)',
              (nome, regras, pasta_pai_id))
    conn.commit()
    conn.close()

def listar_pastas(pasta_pai_id=None):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, nome, regras, pasta_pai_id, data_criacao 
        FROM pastas_documentacao 
        WHERE pasta_pai_id IS NULL AND ? IS NULL
           OR pasta_pai_id = ?
        ORDER BY data_criacao DESC
    ''', (pasta_pai_id, pasta_pai_id))
    pastas = c.fetchall()
    conn.close()
    return pastas

def listar_todas_pastas():
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('SELECT id, nome, regras, pasta_pai_id, data_criacao FROM pastas_documentacao ORDER BY data_criacao DESC')
    pastas = c.fetchall()
    conn.close()
    return pastas

def obter_pasta(pasta_id):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('SELECT id, nome, regras, pasta_pai_id, data_criacao FROM pastas_documentacao WHERE id = ?', (pasta_id,))
    pasta = c.fetchone()
    conn.close()
    return pasta

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

def obter_caminho_pasta(pasta_id):
    caminho = []
    pasta_atual = obter_pasta(pasta_id)
    
    while pasta_atual:
        caminho.insert(0, pasta_atual)
        if pasta_atual[3]:  # pasta_pai_id
            pasta_atual = obter_pasta(pasta_atual[3])
        else:
            break
            
    return caminho

def render_pasta(pasta, nivel=0):
    pasta_id, nome, regras, pasta_pai_id, data_criacao = pasta
    
    # Obter subpastas
    subpastas = listar_pastas(pasta_id)
    
    # Obter casos de teste
    casos = listar_casos_teste_pasta(pasta_id)
    
    # Renderizar pasta atual
    with st.expander(f"{'  ' * nivel}📁 {nome}"):
        st.write(f"**Regras:** {regras}")
        st.write(f"**Data de Criação:** {data_criacao}")
        
        # Renderizar subpastas
        if subpastas:
            st.subheader("Subpastas")
            for subpasta in subpastas:
                render_pasta(subpasta, nivel + 1)
        
        # Renderizar casos de teste
        if casos:
            st.subheader("Casos de Teste")
            for caso in casos:
                with st.expander(f"{'  ' * (nivel + 1)}🔍 {caso[1]}"):
                    st.write(caso[2])

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
            
            # Seleção de pasta pai (opcional)
            todas_pastas = listar_todas_pastas()
            opcoes_pastas = ["Nenhuma (Pasta Raiz)"] + [f"{p[1]} (ID: {p[0]})" for p in todas_pastas]
            pasta_pai_idx = st.selectbox("Pasta Pai (opcional)", range(len(opcoes_pastas)), format_func=lambda x: opcoes_pastas[x])
            
            if st.form_submit_button("Criar Pasta"):
                if nome_pasta:
                    pasta_pai_id = None if pasta_pai_idx == 0 else todas_pastas[pasta_pai_idx-1][0]
                    criar_pasta(nome_pasta, regras, pasta_pai_id)
                    st.success("Pasta criada com sucesso!")
                else:
                    st.error("Por favor, insira um nome para a pasta.")
        
        # Lista de pastas existentes
        st.subheader("Pastas Existentes")
        pastas_raiz = listar_pastas()  # Apenas pastas raiz
        
        for pasta in pastas_raiz:
            render_pasta(pasta)
    
    with tab2:
        st.header("Visualização de Documentação")
        
        # Lista de pastas para visualização
        pastas_raiz = listar_pastas()  # Apenas pastas raiz
        
        for pasta in pastas_raiz:
            render_pasta(pasta)

if __name__ == "__main__":
    main() 