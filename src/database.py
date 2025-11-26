import psycopg2
from psycopg2 import Error
from typing import List, Tuple, Any

class Database:
    def __init__(self, 
                 host: str = "localhost",
                 database: str = "barbearia",
                 user: str = "postgres",
                 password: str = "admin",
                 port: str = "5432"):
        """
        Inicializa a conexão com o banco de dados PostgreSQL
        
        Args:
            host: Endereço do servidor (padrão: localhost)
            database: Nome do banco de dados (padrão: barbearia)
            user: Usuário do PostgreSQL (padrão: postgres)
            password: Senha do usuário (ALTERAR CONFORME SUA INSTALAÇÃO)
            port: Porta do PostgreSQL (padrão: 5432)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.cursor = None
    
    def conectar(self):
        """Estabelece conexão com o banco PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.conn.cursor()
            print("Conectado ao banco de dados PostgreSQL")
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            print("\nDICA: Verifique se:")
            print("   - O PostgreSQL está rodando")
            print("   - O banco 'barbearia' foi criado")
            print("   - A senha está correta no arquivo database.py")
    
    def desconectar(self):
        """Fecha a conexão com o banco"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Desconectado do banco de dados")
    
    def executar_query(self, query: str, params: Tuple = None) -> List[Any]:
        """
        Executa uma query SELECT e retorna os resultados
        
        Args:
            query: SQL query a ser executada
            params: Tupla com os parâmetros da query
            
        Returns:
            Lista com os resultados da query
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Erro na consulta: {e}")
            return []
    
    def executar_comando(self, comando: str, params: Tuple = None) -> bool:
        """
        Executa um comando INSERT, UPDATE ou DELETE
        
        Args:
            comando: SQL comando a ser executado
            params: Tupla com os parâmetros do comando
            
        Returns:
            True se sucesso, False se erro
        """
        try:
            if params:
                self.cursor.execute(comando, params)
            else:
                self.cursor.execute(comando)
            self.conn.commit()
            print("Operação realizada com sucesso")
            return True
        except Error as e:
            print(f"Erro na operação: {e}")
            self.conn.rollback()
            return False
    
    def criar_tabelas(self, schema_sql: str):
        """
        Cria as tabelas do banco (executar apenas uma vez)
        
        Args:
            schema_sql: String contendo os comandos SQL de criação
        """
        try:
            comandos = schema_sql.split(';')
            for comando in comandos:
                comando = comando.strip()
                if comando:
                    self.cursor.execute(comando)
            self.conn.commit()
            print("Tabelas criadas com sucesso")
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
            self.conn.rollback()
    
    def executar_arquivo_sql(self, caminho_arquivo: str):
        """
        Executa um arquivo SQL completo
        
        Args:
            caminho_arquivo: Caminho para o arquivo .sql
        """
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                sql = f.read()
            
            comandos = sql.split(';')
            for comando in comandos:
                comando = comando.strip()
                if comando:
                    self.cursor.execute(comando)
            
            self.conn.commit()
            print(f"Arquivo {caminho_arquivo} executado com sucesso")
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {caminho_arquivo}")
        except Error as e:
            print(f"Erro ao executar arquivo SQL: {e}")
            self.conn.rollback()