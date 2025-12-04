import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from pymongo import MongoClient, ASCENDING, DESCENDING

def criar_estrutura_mongodb():
    """Cria coleções e índices no MongoDB"""
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client['barbearia_db']
    
    print("🚀 Criando estrutura do MongoDB...\n")
    
    # Criar coleções (se não existirem)
    colecoes = ['clientes', 'barbeiros', 'servicos', 'produtos', 'atendimentos']
    
    for colecao in colecoes:
        if colecao not in db.list_collection_names():
            db.create_collection(colecao)
            print(f"✓ Coleção '{colecao}' criada")
    
    # Criar índices
    print("\n🔍 Criando índices...")
    
    # Clientes
    db.clientes.create_index("cpf", unique=True)
    db.clientes.create_index("nome")
    print("✓ Índices de clientes criados")
    
    # Barbeiros
    db.barbeiros.create_index("cpf", unique=True)
    db.barbeiros.create_index("ativo")
    print("✓ Índices de barbeiros criados")
    
    # Atendimentos
    db.atendimentos.create_index("cliente_id")
    db.atendimentos.create_index("barbeiro_id")
    db.atendimentos.create_index("data_atendimento")
    db.atendimentos.create_index("data_agendada")
    db.atendimentos.create_index("status")
    db.atendimentos.create_index([("data_atendimento", DESCENDING), ("status", ASCENDING)])
    print("✓ Índices de atendimentos criados")
    
    print("\n✅ Estrutura criada com sucesso!")
    
    client.close()

if __name__ == "__main__":
    criar_estrutura_mongodb()