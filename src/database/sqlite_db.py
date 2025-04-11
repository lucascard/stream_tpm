import sqlite3
from datetime import datetime
import os

class SQLiteDB:
    def __init__(self):
        self.db_path = "database/test_tpm.db"
        self.ensure_db_directory()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_tables()

    def ensure_db_directory(self):
        """Garante que o diretório do banco existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        cursor = self.conn.cursor()
        
        # Tabela de Planos de Teste
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS planos_teste (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                status TEXT,
                data_criacao TIMESTAMP,
                data_atualizacao TIMESTAMP
            )
        ''')

        # Tabela de Suítes de Teste
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suites_teste (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                status TEXT,
                data_criacao TIMESTAMP,
                data_atualizacao TIMESTAMP
            )
        ''')

        # Tabela de Casos de Teste
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS casos_teste (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                suite_id INTEGER,
                pre_condicoes TEXT,
                passos_execucao TEXT,
                resultado_esperado TEXT,
                prioridade TEXT,
                status TEXT,
                data_criacao TIMESTAMP,
                data_atualizacao TIMESTAMP,
                FOREIGN KEY (suite_id) REFERENCES suites_teste (id)
            )
        ''')

        # Tabela de Testes Regressivos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS regressivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                status TEXT,
                data_criacao TIMESTAMP,
                data_atualizacao TIMESTAMP
            )
        ''')

        self.conn.commit()

    # Métodos para Planos de Teste
    def inserir_plano(self, titulo, descricao, status):
        """Insere um novo plano de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            INSERT INTO planos_teste (titulo, descricao, status, data_criacao, data_atualizacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, descricao, status, data_atual, data_atual))
        self.conn.commit()
        return cursor.lastrowid

    def listar_planos(self):
        """Lista todos os planos de teste"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM planos_teste')
        return [dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()]

    def atualizar_plano(self, id_plano, titulo, descricao, status):
        """Atualiza um plano de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            UPDATE planos_teste 
            SET titulo = ?, descricao = ?, status = ?, data_atualizacao = ?
            WHERE id = ?
        ''', (titulo, descricao, status, data_atual, id_plano))
        self.conn.commit()
        return cursor.rowcount > 0

    def excluir_plano(self, id_plano):
        """Exclui um plano de teste"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM planos_teste WHERE id = ?', (id_plano,))
        self.conn.commit()
        return cursor.rowcount > 0

    # Métodos para Suítes de Teste
    def inserir_suite(self, titulo, descricao, status):
        """Insere uma nova suíte de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            INSERT INTO suites_teste (titulo, descricao, status, data_criacao, data_atualizacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, descricao, status, data_atual, data_atual))
        self.conn.commit()
        return cursor.lastrowid

    def listar_suites(self):
        """Lista todas as suítes de teste"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM suites_teste')
        return [dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()]

    def atualizar_suite(self, id_suite, titulo, descricao, status):
        """Atualiza uma suíte de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            UPDATE suites_teste 
            SET titulo = ?, descricao = ?, status = ?, data_atualizacao = ?
            WHERE id = ?
        ''', (titulo, descricao, status, data_atual, id_suite))
        self.conn.commit()
        return cursor.rowcount > 0

    def excluir_suite(self, id_suite):
        """Exclui uma suíte de teste"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM suites_teste WHERE id = ?', (id_suite,))
        self.conn.commit()
        return cursor.rowcount > 0

    # Métodos para Casos de Teste
    def criar_caso_teste(self, caso):
        """Cria um novo caso de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            INSERT INTO casos_teste (
                titulo, descricao, suite_id, pre_condicoes, 
                passos_execucao, resultado_esperado, prioridade, 
                status, data_criacao, data_atualizacao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            caso['titulo'], caso['descricao'], caso['suite_id'],
            caso['pre_condicoes'], caso['passos_execucao'],
            caso['resultado_esperado'], caso['prioridade'],
            caso['status'], data_atual, data_atual
        ))
        self.conn.commit()
        return cursor.lastrowid

    def listar_casos_teste(self):
        """Lista todos os casos de teste"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM casos_teste')
        return [dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()]

    def buscar_caso_teste(self, caso_id):
        """Busca um caso de teste específico"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM casos_teste WHERE id = ?', (caso_id,))
        row = cursor.fetchone()
        if row:
            return dict(zip([col[0] for col in cursor.description], row))
        return None

    def atualizar_caso_teste(self, caso_id, dados):
        """Atualiza um caso de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        dados['data_atualizacao'] = data_atual
        
        # Constrói a query dinamicamente baseada nos campos fornecidos
        campos = []
        valores = []
        for campo, valor in dados.items():
            if campo != 'id':  # Ignora o ID na atualização
                campos.append(f"{campo} = ?")
                valores.append(valor)
        
        # Adiciona o ID ao final dos valores
        valores.append(caso_id)
        
        # Constrói a query
        query = f'''
            UPDATE casos_teste 
            SET {', '.join(campos)}
            WHERE id = ?
        '''
        
        # Executa a query
        try:
            cursor.execute(query, valores)
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar caso de teste: {str(e)}")
            return False

    def deletar_caso_teste(self, caso_id):
        """Deleta um caso de teste"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM casos_teste WHERE id = ?', (caso_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def atualizar_caso_teste_simples(self, caso_id, titulo, descricao, suite_id, pre_condicoes, 
                               passos_execucao, resultado_esperado, status, prioridade):
        """Método simplificado para atualizar um caso de teste"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        
        try:
            cursor.execute('''
                UPDATE casos_teste 
                SET titulo = ?, 
                    descricao = ?, 
                    suite_id = ?, 
                    pre_condicoes = ?, 
                    passos_execucao = ?, 
                    resultado_esperado = ?, 
                    status = ?, 
                    prioridade = ?,
                    data_atualizacao = ?
                WHERE id = ?
            ''', (
                titulo, 
                descricao, 
                suite_id, 
                pre_condicoes, 
                passos_execucao, 
                resultado_esperado, 
                status, 
                prioridade,
                data_atual,
                caso_id
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar caso de teste: {str(e)}")
            return False

    # Métodos para Testes Regressivos
    def inserir_regressivo(self, titulo, descricao, status):
        """Insere um novo teste regressivo"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            INSERT INTO regressivos (titulo, descricao, status, data_criacao, data_atualizacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, descricao, status, data_atual, data_atual))
        self.conn.commit()
        return cursor.lastrowid

    def listar_regressivos(self):
        """Lista todos os testes regressivos"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM regressivos')
        return [dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()]

    def atualizar_regressivo(self, id_regressivo, titulo, descricao, status):
        """Atualiza um teste regressivo"""
        cursor = self.conn.cursor()
        data_atual = datetime.now()
        cursor.execute('''
            UPDATE regressivos 
            SET titulo = ?, descricao = ?, status = ?, data_atualizacao = ?
            WHERE id = ?
        ''', (titulo, descricao, status, data_atual, id_regressivo))
        self.conn.commit()
        return cursor.rowcount > 0

    def excluir_regressivo(self, id_regressivo):
        """Exclui um teste regressivo"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM regressivos WHERE id = ?', (id_regressivo,))
        self.conn.commit()
        return cursor.rowcount > 0

    def __del__(self):
        """Fecha a conexão quando o objeto é destruído"""
        if hasattr(self, 'conn'):
            self.conn.close() 