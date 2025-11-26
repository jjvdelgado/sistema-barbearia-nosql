from database import Database
from crud_clientes import menu_clientes
from crud_barbeiros import menu_barbeiros
from crud_servicos import menu_servicos
from relatorios import menu_relatorios
from processos import menu_processos
from crud_produtos import menu_produtos

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def inicializar_banco(db):
    """Cria as tabelas do banco de dados"""
    print("\nVerificando banco de dados...")

    query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'cliente'
        );
    """
    resultado = db.executar_query(query)
    
    if resultado and resultado[0][0]:
        print("Tabelas já existem!")
        return
    
    print("Criando tabelas...")
    try:
        with open('../sql/schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()
        
        db.criar_tabelas(schema)
        print("Banco de dados inicializado!")
        
        print("\nDeseja popular o banco com dados de exemplo?")
        resposta = input("(S/N): ").strip().upper()
        
        if resposta == 'S':
            db.executar_arquivo_sql('../sql/populate.sql')
            print("Dados de exemplo inseridos!")
        
    except FileNotFoundError:
        print("Arquivo schema.sql não encontrado. Certifique-se de criar a pasta sql/ com o arquivo.")
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

def menu_principal(db):
    """Menu principal do sistema"""
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE GERENCIAMENTO - BARBEARIA")
        print("="*60)
        print("\n[1] Gerenciar Clientes")
        print("[2] Gerenciar Barbeiros")
        print("[3] Gerenciar Serviços")
        print("[4] Gerenciar Produtos")
        print("[5] Processos de Negócio (Agendamentos/Atendimentos)")
        print("[6] Relatórios")
        print("[0] Sair")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
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
            print("\nEncerrando sistema... Até logo! 👋")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("INICIANDO SISTEMA DA BARBEARIA")
    print("="*60)
    
    db = Database()
    db.conectar()
    
    # Inicializar banco (criar tabelas se não existirem)
    inicializar_banco(db)
    
    try:
        menu_principal(db)
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
    finally:
        db.desconectar()
        print("\nObrigado por usar o sistema!")