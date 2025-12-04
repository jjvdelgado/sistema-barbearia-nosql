from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from datetime import datetime

class DatabaseMongo:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="barbearia_db"):
        """Inicializa conexão com MongoDB"""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        
        # Coleções
        self.clientes = self.db.clientes
        self.barbeiros = self.db.barbeiros
        self.servicos = self.db.servicos
        self.produtos = self.db.produtos
        self.atendimentos = self.db.atendimentos
        
        print(f"✅ Conectado ao MongoDB: {db_name}")
    
    def inserir(self, colecao, documento):
        """Insere um documento"""
        try:
            result = self.db[colecao].insert_one(documento)
            return result.inserted_id
        except Exception as e:
            print(f"Erro ao inserir: {e}")
            return None
    
    def buscar_um(self, colecao, filtro):
        """Busca um documento"""
        return self.db[colecao].find_one(filtro)
    
    def buscar_todos(self, colecao, filtro={}, ordenacao=None, limite=None):
        """Busca múltiplos documentos"""
        cursor = self.db[colecao].find(filtro)
        
        if ordenacao:
            cursor = cursor.sort(ordenacao)
        
        if limite:
            cursor = cursor.limit(limite)
        
        return list(cursor)
    
    def atualizar(self, colecao, filtro, atualizacao):
        """Atualiza documento(s)"""
        try:
            result = self.db[colecao].update_one(filtro, {"$set": atualizacao})
            return result.modified_count > 0
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return False
    
    def deletar(self, colecao, filtro):
        """Deleta documento(s)"""
        try:
            result = self.db[colecao].delete_one(filtro)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Erro ao deletar: {e}")
            return False
    
    def agregacao(self, colecao, pipeline):
        """Executa pipeline de agregação"""
        return list(self.db[colecao].aggregate(pipeline))
    
    def fechar(self):
        """Fecha conexão"""
        self.client.close()
        print("Conexão com MongoDB fechada")