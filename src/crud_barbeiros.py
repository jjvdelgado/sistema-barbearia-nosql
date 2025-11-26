from database import Database
from datetime import datetime

class CRUDBarbeiro:
    def __init__(self, db: Database):
        self.db = db
    
    def criar_barbeiro(self):
        """Cadastra um novo barbeiro"""
        print("\n=== CADASTRAR NOVO BARBEIRO ===\n")
        
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
            
            data_contratacao = input("Data de contratação (DD/MM/AAAA) (opcional, padrão=hoje): ").strip()
            if data_contratacao:
                try:
                    data_contratacao = datetime.strptime(data_contratacao, "%d/%m/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    print("Data inválida! Use o formato DD/MM/AAAA")
                    return
            else:
                data_contratacao = None
            
            print("\nEspecialidades: corte, barba, designer, coloração, tratamento")
            especialidade = input("Especialidade principal: ").strip() or None
            
            comissao = input("Comissão (%) (padrão=30%): ").strip()
            if comissao:
                try:
                    comissao = float(comissao)
                    if comissao < 0 or comissao > 100:
                        print("Comissão deve estar entre 0 e 100!")
                        return
                except ValueError:
                    print("Comissão inválida!")
                    return
            else:
                comissao = 30.00
            
            query = """
                INSERT INTO barbeiro (nome, cpf, telefone, email, data_contratacao, especialidade, comissao_percentual)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (nome, cpf, telefone, email, data_contratacao, especialidade, comissao)
            
            if self.db.executar_comando(query, params):
                print(f"\n✓ Barbeiro '{nome}' cadastrado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao cadastrar barbeiro: {e}")
    
    def listar_barbeiros(self):
        """Lista todos os barbeiros cadastrados"""
        print("\n=== LISTA DE BARBEIROS ===\n")
        
        query = """
            SELECT id_barbeiro, nome, cpf, telefone, especialidade, comissao_percentual, ativo 
            FROM barbeiro 
            ORDER BY nome
        """
        barbeiros = self.db.executar_query(query)
        
        if not barbeiros:
            print("Nenhum barbeiro cadastrado.")
            return
        
        print(f"{'ID':<5} {'Nome':<30} {'CPF':<15} {'Especialidade':<15} {'Comissão':<10} {'Status':<10}")
        print("-" * 90)
        
        for barbeiro in barbeiros:
            id_b, nome, cpf, telefone, especialidade, comissao, ativo = barbeiro
            cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            especialidade_fmt = especialidade if especialidade else "-"
            status = "Ativo" if ativo else "Inativo"
            print(f"{id_b:<5} {nome:<30} {cpf_fmt:<15} {especialidade_fmt:<15} {comissao}%{'':<6} {status:<10}")
        
        print(f"\nTotal: {len(barbeiros)} barbeiro(s)")
    
    def buscar_barbeiro(self):
        """Busca um barbeiro por ID, CPF ou Nome"""
        print("\n=== BUSCAR BARBEIRO ===\n")
        print("[1] Buscar por ID")
        print("[2] Buscar por CPF")
        print("[3] Buscar por Nome")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            id_barbeiro = input("Digite o ID: ").strip()
            if not id_barbeiro.isdigit():
                print("ID inválido!")
                return
            query = "SELECT * FROM barbeiro WHERE id_barbeiro = %s"
            params = (id_barbeiro,)
        
        elif opcao == "2":
            cpf = input("Digite o CPF (apenas números): ").strip()
            query = "SELECT * FROM barbeiro WHERE cpf = %s"
            params = (cpf,)
        
        elif opcao == "3":
            nome = input("Digite o nome (ou parte dele): ").strip()
            query = "SELECT * FROM barbeiro WHERE nome ILIKE %s"
            params = (f"%{nome}%",)
        
        else:
            print("Opção inválida!")
            return
        
        barbeiros = self.db.executar_query(query, params)
        
        if not barbeiros:
            print("\nBarbeiro não encontrado.")
            return
        
        print("\n" + "="*80)
        for barbeiro in barbeiros:
            id_b, nome, cpf, telefone, email, data_contrat, especialidade, comissao, ativo = barbeiro
            cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            
            print(f"ID: {id_b}")
            print(f"Nome: {nome}")
            print(f"CPF: {cpf_fmt}")
            print(f"Telefone: {telefone}")
            print(f"Email: {email if email else '-'}")
            print(f"Data Contratação: {data_contrat if data_contrat else '-'}")
            print(f"Especialidade: {especialidade if especialidade else '-'}")
            print(f"Comissão: {comissao}%")
            print(f"Status: {'Ativo' if ativo else 'Inativo'}")
            print("="*80)
    
    def atualizar_barbeiro(self):
        """Atualiza dados de um barbeiro"""
        print("\n=== ATUALIZAR BARBEIRO ===\n")
        
        id_barbeiro = input("Digite o ID do barbeiro: ").strip()
        if not id_barbeiro.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT * FROM barbeiro WHERE id_barbeiro = %s"
        barbeiro = self.db.executar_query(query, (id_barbeiro,))
        
        if not barbeiro:
            print("Barbeiro não encontrado!")
            return
        
        barbeiro = barbeiro[0]
        id_b, nome_atual, cpf_atual, tel_atual, email_atual, data_atual, esp_atual, com_atual, ativo_atual = barbeiro
        
        print(f"\nBarbeiro: {nome_atual}")
        print("\nDeixe em branco para manter o valor atual.\n")
        
        nome = input(f"Nome [{nome_atual}]: ").strip() or nome_atual
        telefone = input(f"Telefone [{tel_atual}]: ").strip() or tel_atual
        email = input(f"Email [{email_atual if email_atual else '-'}]: ").strip()
        email = email if email else email_atual
        
        especialidade = input(f"Especialidade [{esp_atual if esp_atual else '-'}]: ").strip()
        especialidade = especialidade if especialidade else esp_atual
        
        comissao = input(f"Comissão (%) [{com_atual}]: ").strip()
        if comissao:
            try:
                comissao = float(comissao)
            except ValueError:
                print("Comissão inválida! Mantendo valor atual.")
                comissao = com_atual
        else:
            comissao = com_atual
        
        query = """
            UPDATE barbeiro 
            SET nome = %s, telefone = %s, email = %s, especialidade = %s, comissao_percentual = %s
            WHERE id_barbeiro = %s
        """
        params = (nome, telefone, email, especialidade, comissao, id_barbeiro)
        
        if self.db.executar_comando(query, params):
            print(f"\n✓ Barbeiro atualizado com sucesso!")
    
    def ativar_desativar_barbeiro(self):
        """Ativa ou desativa um barbeiro"""
        print("\n=== ATIVAR/DESATIVAR BARBEIRO ===\n")
        
        id_barbeiro = input("Digite o ID do barbeiro: ").strip()
        if not id_barbeiro.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome, ativo FROM barbeiro WHERE id_barbeiro = %s"
        barbeiro = self.db.executar_query(query, (id_barbeiro,))
        
        if not barbeiro:
            print("Barbeiro não encontrado!")
            return
        
        nome, ativo = barbeiro[0]
        status_atual = "Ativo" if ativo else "Inativo"
        novo_status = False if ativo else True
        acao = "desativar" if ativo else "ativar"
        
        confirmacao = input(f"\nBarbeiro '{nome}' está {status_atual}. Deseja {acao}? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("Operação cancelada.")
            return
        
        query = "UPDATE barbeiro SET ativo = %s WHERE id_barbeiro = %s"
        
        if self.db.executar_comando(query, (novo_status, id_barbeiro)):
            print(f"\n✓ Barbeiro '{nome}' {'ativado' if novo_status else 'desativado'} com sucesso!")
    
    def deletar_barbeiro(self):
        """Remove um barbeiro do sistema"""
        print("\n=== REMOVER BARBEIRO ===\n")
        
        id_barbeiro = input("Digite o ID do barbeiro: ").strip()
        if not id_barbeiro.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome FROM barbeiro WHERE id_barbeiro = %s"
        barbeiro = self.db.executar_query(query, (id_barbeiro,))
        
        if not barbeiro:
            print("Barbeiro não encontrado!")
            return
        
        nome = barbeiro[0][0]
        
        print(f"\n⚠️  ATENÇÃO: Remover o barbeiro '{nome}' pode afetar agendamentos e atendimentos!")
        confirmacao = input("Tem certeza? Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao != 'CONFIRMAR':
            print("Operação cancelada.")
            return
        
        query = "DELETE FROM barbeiro WHERE id_barbeiro = %s"
        
        if self.db.executar_comando(query, (id_barbeiro,)):
            print(f"\n✓ Barbeiro '{nome}' removido com sucesso!")


def menu_barbeiros(db: Database):
    """Menu de gerenciamento de barbeiros"""
    crud = CRUDBarbeiro(db)
    
    while True:
        print("\n" + "="*50)
        print("           GERENCIAR BARBEIROS")
        print("="*50)
        print("[1] Cadastrar Barbeiro")
        print("[2] Listar Todos os Barbeiros")
        print("[3] Buscar Barbeiro")
        print("[4] Atualizar Barbeiro")
        print("[5] Ativar/Desativar Barbeiro")
        print("[6] Remover Barbeiro")
        print("[0] Voltar ao Menu Principal")
        print("-"*50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            crud.criar_barbeiro()
        elif opcao == "2":
            crud.listar_barbeiros()
        elif opcao == "3":
            crud.buscar_barbeiro()
        elif opcao == "4":
            crud.atualizar_barbeiro()
        elif opcao == "5":
            crud.ativar_desativar_barbeiro()
        elif opcao == "6":
            crud.deletar_barbeiro()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
        
        input("\nPressione ENTER para continuar...")