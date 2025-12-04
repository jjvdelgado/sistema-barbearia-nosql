import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from crud_clientes import menu_clientes
from crud_barbeiros import menu_barbeiros
from crud_servicos import menu_servicos
from relatorios import menu_relatorios
from processos import menu_processos
from crud_produtos import menu_produtos
import os

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_estrutura_mongo(db):
    """Verifica se as coleções existem no MongoDB"""
    print("\nVerificando estrutura do MongoDB...")
    
    colecoes_necessarias = ['clientes', 'barbeiros', 'servicos', 'produtos', 'atendimentos']
    colecoes_existentes = db.db.list_collection_names()
    
    faltando = [col for col in colecoes_necessarias if col not in colecoes_existentes]
    
    if faltando:
        print(f"ATENCAO: Colecoes faltando: {', '.join(faltando)}")
        print("\nExecute primeiro: python create_mongodb_structure.py")
        return False
    
    print("Todas as colecoes estao criadas!")
    return True

def inicializar_sistema(db):
    """Inicializa e verifica o sistema MongoDB"""
    print("\n" + "="*60)
    print("   VERIFICACAO INICIAL DO SISTEMA")
    print("="*60)
    
    # Verificar estrutura
    if not verificar_estrutura_mongo(db):
        print("\nATENCAO: Sistema nao pode iniciar sem a estrutura correta!")
        print("Execute: python create_mongodb_structure.py")
        return False
    
    # Verificar se já tem dados
    total_docs = sum([
        db.clientes.count_documents({}),
        db.barbeiros.count_documents({}),
        db.servicos.count_documents({}),
        db.produtos.count_documents({})
    ])
    
    if total_docs == 0:
        print("\nBanco de dados esta vazio!")
        print("Execute: python populate_mongodb.py")
        resposta = input("\nDeseja continuar mesmo assim? (S/N): ").strip().upper()
        if resposta != 'S':
            return False
    
    return True

def menu_principal(db):
    """Menu principal do sistema"""
    while True:
        print("\n" + "="*60)
        print("   SISTEMA DE GERENCIAMENTO - BARBEARIA (MongoDB)")
        print("="*60)
        print("\n[1] Gerenciar Clientes")
        print("[2] Gerenciar Barbeiros")
        print("[3] Gerenciar Servicos")
        print("[4] Gerenciar Produtos")
        print("[5] Processos de Negocio (Agendamentos/Atendimentos)")
        print("[6] Relatorios")
        print("[0] Sair")
        print("-"*60)
        
        opcao = input("\nEscolha uma opcao: ").strip()
        
        if opcao == "1":
            menu_clientes(db)
        elif opcao == "2":
            menu_barbeiros(db)
        elif opcao == "3":
            menu_servicos(db)
        elif opcao == "4":
            menu_produtos(db)
        elif opcao == "5":
            menu_processos(db)
        elif opcao == "6":
            menu_relatorios(db)
        elif opcao == "0":
            print("\nEncerrando sistema... Ate logo!")
            break
        else:
            print("\nOpcao invalida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   INICIANDO SISTEMA DA BARBEARIA - MONGODB")
    print("="*60)
    
    try:
        # Conectar ao MongoDB
        db = DatabaseMongo()
        
        # Verificar e inicializar sistema
        if not inicializar_sistema(db):
            print("\nERRO: Sistema nao pode iniciar!")
            exit(1)
        
        # Executar menu principal
        menu_principal(db)
        
    except KeyboardInterrupt:
        print("\n\nATENCAO: Sistema interrompido pelo usuario.")
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.fechar()
        print("\nObrigado por usar o sistema!")