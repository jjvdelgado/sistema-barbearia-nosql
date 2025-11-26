from database import Database

class CRUDServico:
    def __init__(self, db: Database):
        self.db = db
    
    def criar_servico(self):
        """Cadastra um novo serviço"""
        print("\n=== CADASTRAR NOVO SERVIÇO ===\n")
        
        try:
            nome = input("Nome do serviço: ").strip()
            if not nome:
                print("Nome é obrigatório!")
                return
            
            descricao = input("Descrição (opcional): ").strip() or None
            
            preco = input("Preço (R$): ").strip()
            try:
                preco = float(preco.replace(',', '.'))
                if preco <= 0:
                    print("Preço deve ser maior que zero!")
                    return
            except ValueError:
                print("Preço inválido!")
                return
            
            duracao = input("Duração estimada (em minutos): ").strip()
            try:
                duracao = int(duracao)
                if duracao <= 0:
                    print("Duração deve ser maior que zero!")
                    return
            except ValueError:
                print("Duração inválida!")
                return
            
            query = """
                INSERT INTO servico (nome, descricao, preco, duracao_estimada)
                VALUES (%s, %s, %s, %s)
            """
            params = (nome, descricao, preco, duracao)
            
            if self.db.executar_comando(query, params):
                print(f"\n✓ Serviço '{nome}' cadastrado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao cadastrar serviço: {e}")
    
    def listar_servicos(self):
        """Lista todos os serviços cadastrados"""
        print("\n=== LISTA DE SERVIÇOS ===\n")
        
        query = """
            SELECT id_servico, nome, preco, duracao_estimada, ativo 
            FROM servico 
            ORDER BY nome
        """
        servicos = self.db.executar_query(query)
        
        if not servicos:
            print("Nenhum serviço cadastrado.")
            return
        
        print(f"{'ID':<5} {'Nome':<35} {'Preço':<12} {'Duração':<12} {'Status':<10}")
        print("-" * 74)
        
        for servico in servicos:
            id_s, nome, preco, duracao, ativo = servico
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            duracao_fmt = f"{duracao} min"
            status = "Ativo" if ativo else "Inativo"
            print(f"{id_s:<5} {nome:<35} {preco_fmt:<12} {duracao_fmt:<12} {status:<10}")
        
        print(f"\nTotal: {len(servicos)} serviço(s)")
    
    def buscar_servico(self):
        """Busca um serviço por ID ou Nome"""
        print("\n=== BUSCAR SERVIÇO ===\n")
        print("[1] Buscar por ID")
        print("[2] Buscar por Nome")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            id_servico = input("Digite o ID: ").strip()
            if not id_servico.isdigit():
                print("ID inválido!")
                return
            query = "SELECT * FROM servico WHERE id_servico = %s"
            params = (id_servico,)
        
        elif opcao == "2":
            nome = input("Digite o nome (ou parte dele): ").strip()
            query = "SELECT * FROM servico WHERE nome ILIKE %s"
            params = (f"%{nome}%",)
        
        else:
            print("Opção inválida!")
            return
        
        servicos = self.db.executar_query(query, params)
        
        if not servicos:
            print("\nServiço não encontrado.")
            return
        
        print("\n" + "="*70)
        for servico in servicos:
            id_s, nome, descricao, preco, duracao, ativo = servico
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"ID: {id_s}")
            print(f"Nome: {nome}")
            print(f"Descrição: {descricao if descricao else '-'}")
            print(f"Preço: {preco_fmt}")
            print(f"Duração: {duracao} minutos")
            print(f"Status: {'Ativo' if ativo else 'Inativo'}")
            print("="*70)
    
    def atualizar_servico(self):
        """Atualiza dados de um serviço"""
        print("\n=== ATUALIZAR SERVIÇO ===\n")
        
        id_servico = input("Digite o ID do serviço: ").strip()
        if not id_servico.isdigit():
            print("ID inválido!")
            return
        
        # Buscar serviço
        query = "SELECT * FROM servico WHERE id_servico = %s"
        servico = self.db.executar_query(query, (id_servico,))
        
        if not servico:
            print("Serviço não encontrado!")
            return
        
        servico = servico[0]
        id_s, nome_atual, desc_atual, preco_atual, duracao_atual, ativo_atual = servico
        
        print(f"\nServiço: {nome_atual}")
        print("\nDeixe em branco para manter o valor atual.\n")
        
        nome = input(f"Nome [{nome_atual}]: ").strip() or nome_atual
        
        descricao = input(f"Descrição [{desc_atual if desc_atual else '-'}]: ").strip()
        descricao = descricao if descricao else desc_atual
        
        preco_input = input(f"Preço (R$) [{preco_atual}]: ").strip()
        if preco_input:
            try:
                preco = float(preco_input.replace(',', '.'))
                if preco <= 0:
                    print("Preço inválido! Mantendo valor atual.")
                    preco = preco_atual
            except ValueError:
                print("Preço inválido! Mantendo valor atual.")
                preco = preco_atual
        else:
            preco = preco_atual
        
        duracao_input = input(f"Duração (min) [{duracao_atual}]: ").strip()
        if duracao_input:
            try:
                duracao = int(duracao_input)
                if duracao <= 0:
                    print("Duração inválida! Mantendo valor atual.")
                    duracao = duracao_atual
            except ValueError:
                print("Duração inválida! Mantendo valor atual.")
                duracao = duracao_atual
        else:
            duracao = duracao_atual
        
        query = """
            UPDATE servico 
            SET nome = %s, descricao = %s, preco = %s, duracao_estimada = %s
            WHERE id_servico = %s
        """
        params = (nome, descricao, preco, duracao, id_servico)
        
        if self.db.executar_comando(query, params):
            print(f"\n✓ Serviço atualizado com sucesso!")
    
    def ativar_desativar_servico(self):
        """Ativa ou desativa um serviço"""
        print("\n=== ATIVAR/DESATIVAR SERVIÇO ===\n")
        
        id_servico = input("Digite o ID do serviço: ").strip()
        if not id_servico.isdigit():
            print("ID inválido!")
            return

        query = "SELECT nome, ativo FROM servico WHERE id_servico = %s"
        servico = self.db.executar_query(query, (id_servico,))
        
        if not servico:
            print("Serviço não encontrado!")
            return
        
        nome, ativo = servico[0]
        status_atual = "Ativo" if ativo else "Inativo"
        novo_status = not ativo
        acao = "desativar" if ativo else "ativar"
        
        confirmacao = input(f"\nServiço '{nome}' está {status_atual}. Deseja {acao}? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("Operação cancelada.")
            return
        
        query = "UPDATE servico SET ativo = %s WHERE id_servico = %s"
        
        if self.db.executar_comando(query, (novo_status, id_servico)):
            print(f"\n✓ Serviço '{nome}' {'ativado' if novo_status else 'desativado'} com sucesso!")
    
    def deletar_servico(self):
        """Remove um serviço do sistema"""
        print("\n=== REMOVER SERVIÇO ===\n")
        
        id_servico = input("Digite o ID do serviço: ").strip()
        if not id_servico.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome FROM servico WHERE id_servico = %s"
        servico = self.db.executar_query(query, (id_servico,))
        
        if not servico:
            print("Serviço não encontrado!")
            return
        
        nome = servico[0][0]
        
        print(f"\nATENÇÃO: Remover o serviço '{nome}' pode afetar agendamentos e atendimentos!")
        confirmacao = input("Tem certeza? Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao != 'CONFIRMAR':
            print("Operação cancelada.")
            return
        
        query = "DELETE FROM servico WHERE id_servico = %s"
        
        if self.db.executar_comando(query, (id_servico,)):
            print(f"\n✓ Serviço '{nome}' removido com sucesso!")
    
    def listar_servicos_mais_solicitados(self):
        """Relatório: Serviços mais solicitados"""
        print("\n=== SERVIÇOS MAIS SOLICITADOS ===\n")
        
        query = """
            SELECT 
                s.nome,
                COUNT(a.id_agendamento) as total_agendamentos,
                s.preco,
                COUNT(a.id_agendamento) * s.preco as faturamento_potencial
            FROM servico s
            LEFT JOIN agendamento a ON s.id_servico = a.id_servico
            GROUP BY s.id_servico, s.nome, s.preco
            HAVING COUNT(a.id_agendamento) > 0
            ORDER BY total_agendamentos DESC
            LIMIT 10
        """
        
        resultados = self.db.executar_query(query)
        
        if not resultados:
            print("Nenhum serviço foi agendado ainda.")
            return
        
        print(f"{'Serviço':<35} {'Agendamentos':<15} {'Preço':<12} {'Faturamento':<15}")
        print("-" * 77)
        
        for resultado in resultados:
            nome, total, preco, faturamento = resultado
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"{nome:<35} {total:<15} {preco_fmt:<12} {faturamento_fmt:<15}")
        
        print(f"\nTotal de serviços listados: {len(resultados)}")


def menu_servicos(db: Database):
    """Menu de gerenciamento de serviços"""
    crud = CRUDServico(db)
    
    while True:
        print("\n" + "="*50)
        print("           GERENCIAR SERVIÇOS")
        print("="*50)
        print("[1] Cadastrar Serviço")
        print("[2] Listar Todos os Serviços")
        print("[3] Buscar Serviço")
        print("[4] Atualizar Serviço")
        print("[5] Ativar/Desativar Serviço")
        print("[6] Remover Serviço")
        print("[7] Relatório: Serviços Mais Solicitados")
        print("[0] Voltar ao Menu Principal")
        print("-"*50)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            crud.criar_servico()
        elif opcao == "2":
            crud.listar_servicos()
        elif opcao == "3":
            crud.buscar_servico()
        elif opcao == "4":
            crud.atualizar_servico()
        elif opcao == "5":
            crud.ativar_desativar_servico()
        elif opcao == "6":
            crud.deletar_servico()
        elif opcao == "7":
            crud.listar_servicos_mais_solicitados()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
        
        input("\nPressione ENTER para continuar...")