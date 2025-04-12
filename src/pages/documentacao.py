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

def editar_pasta(pasta_id, nome, regras, pasta_pai_id=None):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    c.execute('UPDATE pastas_documentacao SET nome = ?, regras = ?, pasta_pai_id = ? WHERE id = ?',
              (nome, regras, pasta_pai_id, pasta_id))
    conn.commit()
    conn.close()

def excluir_pasta(pasta_id):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    
    # Primeiro, excluir todas as associações com casos de teste
    c.execute('DELETE FROM pasta_casos_teste WHERE pasta_id = ?', (pasta_id,))
    
    # Depois, excluir todas as subpastas recursivamente
    subpastas = listar_pastas(pasta_id)
    for subpasta in subpastas:
        excluir_pasta(subpasta[0])
    
    # Por fim, excluir a pasta em si
    c.execute('DELETE FROM pastas_documentacao WHERE id = ?', (pasta_id,))
    
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

def listar_todas_pastas(excluir_id=None):
    conn = sqlite3.connect('database/test_tpm.db')
    c = conn.cursor()
    
    if excluir_id:
        c.execute('SELECT id, nome, regras, pasta_pai_id, data_criacao FROM pastas_documentacao WHERE id != ? ORDER BY data_criacao DESC', (excluir_id,))
    else:
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

def render_pasta(pasta, nivel=0, modo_edicao=False):
    pasta_id, nome, regras, pasta_pai_id, data_criacao = pasta
    
    # Obter subpastas
    subpastas = listar_pastas(pasta_id)
    
    # Obter casos de teste
    casos = listar_casos_teste_pasta(pasta_id)
    
    # Criar indentação visual
    indent = "    " * nivel
    
    # Renderizar pasta atual
    st.markdown(f"{indent}📁 **{nome}**")
    
    # Container para conteúdo da pasta
    with st.container():
        # Adicionar margem esquerda para criar hierarquia visual
        if nivel > 0:
            st.markdown(f"<style>div.element-container {{margin-left: {nivel * 40}px;}}</style>", unsafe_allow_html=True)
        
        # Informações e botões
        with st.expander("Detalhes", expanded=False):
            st.write(f"**Regras:** {regras}")
            st.write(f"**Data de Criação:** {data_criacao}")
            
            # Botões de edição e exclusão (apenas no modo de edição)
            if modo_edicao:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{pasta_id}"):
                        st.session_state['pasta_edicao'] = pasta_id
                
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_{pasta_id}"):
                        st.session_state['pasta_exclusao'] = pasta_id
                        st.session_state['pasta_exclusao_nome'] = nome
                        # Adicionar script para rolar até o topo
                        st.markdown("""
                            <script>
                                window.scrollTo(0, 0);
                            </script>
                        """, unsafe_allow_html=True)
        
        # Renderizar casos de teste
        if casos:
            for caso in casos:
                st.markdown(f"{indent}    📄 {caso[1]}")
                with st.expander("Ver detalhes do caso de teste", expanded=False):
                    st.write(caso[2])
        
        # Renderizar subpastas
        if subpastas:
            for subpasta in subpastas:
                render_pasta(subpasta, nivel + 1, modo_edicao)

def main():
    st.title("📚 Documentação")
    
    # Inicializar banco de dados
    init_db()
    
    # Criar tabs para visualização e edição (ordem invertida)
    tab1, tab2 = st.tabs(["👀 Visualização", "✏️ Edição"])
    
    with tab1:
        st.header("Visualização de Documentação")
        
        # Adicionar CSS para melhorar a visualização hierárquica
        st.markdown("""
            <style>
            .folder-structure {
                margin-left: 20px;
            }
            .folder-item {
                margin: 5px 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Lista de pastas para visualização
        pastas_raiz = listar_pastas()  # Apenas pastas raiz
        
        if not pastas_raiz:
            st.info("Nenhuma pasta criada ainda.")
        else:
            for pasta in pastas_raiz:
                render_pasta(pasta, modo_edicao=False)
    
    with tab2:
        st.header("Edição de Documentação")
        
        # 1. Formulário para criar nova pasta
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
        
        # 2. Verificar se há uma pasta para edição
        if 'pasta_edicao' in st.session_state:
            pasta_id = st.session_state['pasta_edicao']
            pasta = obter_pasta(pasta_id)
            
            if pasta:
                st.subheader(f"Editar Pasta: {pasta[1]}")
                
                with st.form(f"editar_pasta_{pasta_id}"):
                    nome_pasta = st.text_input("Nome da Pasta", value=pasta[1])
                    regras = st.text_area("Regras da Pasta", value=pasta[2])
                    
                    # Seleção de pasta pai (opcional)
                    todas_pastas = listar_todas_pastas(excluir_id=pasta_id)  # Excluir a pasta atual
                    opcoes_pastas = ["Nenhuma (Pasta Raiz)"] + [f"{p[1]} (ID: {p[0]})" for p in todas_pastas]
                    
                    # Encontrar o índice da pasta pai atual
                    pasta_pai_atual = pasta[3]
                    pasta_pai_idx = 0  # Padrão: nenhuma pasta pai
                    
                    if pasta_pai_atual:
                        for i, p in enumerate(todas_pastas):
                            if p[0] == pasta_pai_atual:
                                pasta_pai_idx = i + 1  # +1 porque a primeira opção é "Nenhuma"
                                break
                    
                    pasta_pai_idx = st.selectbox("Pasta Pai (opcional)", range(len(opcoes_pastas)), 
                                                index=pasta_pai_idx, 
                                                format_func=lambda x: opcoes_pastas[x])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Salvar Alterações"):
                            pasta_pai_id = None if pasta_pai_idx == 0 else todas_pastas[pasta_pai_idx-1][0]
                            editar_pasta(pasta_id, nome_pasta, regras, pasta_pai_id)
                            st.success("Pasta atualizada com sucesso!")
                            del st.session_state['pasta_edicao']
                            st.experimental_rerun()
                    
                    with col2:
                        if st.form_submit_button("Cancelar"):
                            del st.session_state['pasta_edicao']
                            st.experimental_rerun()
        
        # 3. Lista de pastas existentes
        st.subheader("Pastas Existentes")
        pastas_raiz = listar_pastas()  # Apenas pastas raiz
        
        if not pastas_raiz:
            st.info("Nenhuma pasta criada ainda.")
        else:
            for pasta in pastas_raiz:
                render_pasta(pasta, modo_edicao=True)
        
        # Verificar se há uma pasta para exclusão (mantido no final para não interferir na ordem visual)
        if 'pasta_exclusao' in st.session_state:
            pasta_id = st.session_state['pasta_exclusao']
            pasta_nome = st.session_state['pasta_exclusao_nome']
            
            # Adicionar script para rolar até o topo
            st.markdown("""
                <script>
                    window.scrollTo(0, 0);
                </script>
            """, unsafe_allow_html=True)
            
            st.warning(f"Você está prestes a excluir a pasta '{pasta_nome}' e todas as suas subpastas. Esta ação não pode ser desfeita.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirmar Exclusão", key="confirmar_exclusao"):
                    excluir_pasta(pasta_id)
                    st.success(f"Pasta '{pasta_nome}' excluída com sucesso!")
                    del st.session_state['pasta_exclusao']
                    del st.session_state['pasta_exclusao_nome']
                    st.experimental_rerun()
            
            with col2:
                if st.button("Cancelar", key="cancelar_exclusao"):
                    del st.session_state['pasta_exclusao']
                    del st.session_state['pasta_exclusao_nome']
                    st.experimental_rerun()

if __name__ == "__main__":
    main() 