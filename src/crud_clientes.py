from database import Database
from datetime import datetime

class CRUDCliente:
    def __init__(self, db: Database):
        self.db = db
    
    def criar_cliente(self):
        """Cadastra um novo cliente"""
        print("\n=== CADASTRAR NOVO CLIENTE ===\n")
        
        try:
            nome = input("Nome completo: ").strip()
            if not nome:
                print("Nome é obrigatório!")
                return
            
            cpf = input("CPF (apenas números): ").strip()
            if len(cpf) != 11 or not cpf.isdigit():
                print("CPF inválido! Deve conter 11 dígitos.")
                return
            
            telefone = input("Telefone: ").strip()
            if not telefone:
                print("Telefone é obrigatório!")
                return
            
            email = input("Email (opcional): ").strip() or None
            
            data_nasc = input("Data de nascimento (DD/MM/AAAA) (opcional): ").strip()
            if data_nasc:
                try:
                    data_nasc = datetime.strptime(data_nasc, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    print("Data inválida! Use o formato DD/MM/AAAA")
                    return
            else:
                data_nasc = None
            
            observacoes = input("Observações (alergias, preferências) (opcional): ").strip() or None
            
            query = """
                INSERT INTO cliente (nome, cpf, telefone, email, data_nascimento, observacoes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (nome, cpf, telefone, email, data_nasc, observacoes)
            
            if self.db.executar_comando(query, params):
                print(f"\n✓ Cliente '{nome}' cadastrado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao cadastrar cliente: {e}")
    
    def listar_clientes(self):
        """Lista todos os clientes cadastrados"""
        print("\n=== LISTA DE CLIENTES ===\n")
        
        query = "SELECT id_cliente, nome, cpf, telefone, email, data_cadastro FROM cliente ORDER BY nome"
        clientes = self.db.executar_query(query)
        
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        print(f"{'ID':<5} {'Nome':<30} {'CPF':<15} {'Telefone':<15} {'Email':<30}")
        print("-" * 95)
        
        for cliente in clientes:
            id_c, nome, cpf, telefone, email, data_cad = cliente
            cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            email_fmt = email if email else "-"
            print(f"{id_c:<5} {nome:<30} {cpf_fmt:<15} {telefone:<15} {email_fmt:<30}")
        
        print(f"\nTotal: {len(clientes)} cliente(s)")
    
    def buscar_cliente(self):
        """Busca um cliente por ID ou CPF"""
        print("\n=== BUSCAR CLIENTE ===\n")
        print("[1] Buscar por ID")
        print("[2] Buscar por CPF")
        print("[3] Buscar por Nome")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            id_cliente = input("Digite o ID: ").strip()
            if not id_cliente.isdigit():
                print("ID inválido!")
                return
            query = "SELECT * FROM cliente WHERE id_cliente = %s"
            params = (id_cliente,)
        
        elif opcao == "2":
            cpf = input("Digite o CPF (apenas números): ").strip()
            query = "SELECT * FROM cliente WHERE cpf = %s"
            params = (cpf,)
        
        elif opcao == "3":
            nome = input("Digite o nome (ou parte dele): ").strip()
            query = "SELECT * FROM cliente WHERE nome ILIKE %s"
            params = (f"%{nome}%",)
        
        else:
            print("Opção inválida!")
            return
        
        clientes = self.db.executar_query(query, params)
        
        if not clientes:
            print("\nCliente não encontrado.")
            return
        
        print("\n" + "="*80)
        for cliente in clientes:
            id_c, nome, cpf, telefone, email, data_nasc, data_cad, obs = cliente
            cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            
            print(f"ID: {id_c}")
            print(f"Nome: {nome}")
            print(f"CPF: {cpf_fmt}")
            print(f"Telefone: {telefone}")
            print(f"Email: {email if email else '-'}")
            print(f"Data Nascimento: {data_nasc if data_nasc else '-'}")
            print(f"Data Cadastro: {data_cad}")
            print(f"Observações: {obs if obs else '-'}")
            print("="*80)
    
    def atualizar_cliente(self):
        """Atualiza dados de um cliente"""
        print("\n=== ATUALIZAR CLIENTE ===\n")
        
        id_cliente = input("Digite o ID do cliente: ").strip()
        if not id_cliente.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT * FROM cliente WHERE id_cliente = %s"
        cliente = self.db.executar_query(query, (id_cliente,))
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        cliente = cliente[0]
        id_c, nome_atual, cpf_atual, tel_atual, email_atual, nasc_atual, cad_atual, obs_atual = cliente
        
        print(f"\nCliente: {nome_atual}")
        print("\nDeixe em branco para manter o valor atual.\n")
        
        nome = input(f"Nome [{nome_atual}]: ").strip() or nome_atual
        telefone = input(f"Telefone [{tel_atual}]: ").strip() or tel_atual
        email = input(f"Email [{email_atual if email_atual else '-'}]: ").strip()
        email = email if email else email_atual
        
        observacoes = input(f"Observações [{obs_atual if obs_atual else '-'}]: ").strip()
        observacoes = observacoes if observacoes else obs_atual
        
        query = """
            UPDATE cliente 
            SET nome = %s, telefone = %s, email = %s, observacoes = %s
            WHERE id_cliente = %s
        """
        params = (nome, telefone, email, observacoes, id_cliente)
        
        if self.db.executar_comando(query, params):
            print(f"\n✓ Cliente atualizado com sucesso!")
    
    def deletar_cliente(self):
        """Remove um cliente do sistema"""
        print("\n=== REMOVER CLIENTE ===\n")
        
        id_cliente = input("Digite o ID do cliente: ").strip()
        if not id_cliente.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome FROM cliente WHERE id_cliente = %s"
        cliente = self.db.executar_query(query, (id_cliente,))
        
        if not cliente:
            print("Cliente não encontrado!")
            return
        
        nome = cliente[0][0]
        
        confirmacao = input(f"\nTem certeza que deseja remover o cliente '{nome}'? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("Operação cancelada.")
            return
        
        query = "DELETE FROM cliente WHERE id_cliente = %s"
        
        if self.db.executar_comando(query, (id_cliente,)):
            print(f"\n✓ Cliente '{nome}' removido com sucesso!")


def menu_clientes(db: Database):
    """Menu de gerenciamento de clientes"""
    crud = CRUDCliente(db)
    
    while True:
        print("\n" + "="*50)
        print("           GERENCIAR CLIENTES")
        print("="*50)
        print("[1] Cadastrar Cliente")
        print("[2] Listar Todos os Clientes")
        print("[3] Buscar Cliente")
        print("[4] Atualizar Cliente")
        print("[5] Remover Cliente")
        print("[0] Voltar ao Menu Principal")
        print("-"*50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            crud.criar_cliente()
        elif opcao == "2":
            crud.listar_clientes()
        elif opcao == "3":
            crud.buscar_cliente()
        elif opcao == "4":
            crud.atualizar_cliente()
        elif opcao == "5":
            crud.deletar_cliente()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
        
        input("\nPressione ENTER para continuar...")