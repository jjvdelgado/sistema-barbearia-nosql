from database import Database
from datetime import datetime, timedelta

class ProcessosNegocio:
    def __init__(self, db: Database):
        self.db = db
    
    def novo_atendimento(self):
        """Cria um novo atendimento (agendado ou walk-in)"""
        print("\n=== NOVO ATENDIMENTO ===\n")
        print("[1] Atendimento Agendado (para data futura)")
        print("[2] Atendimento Walk-in (atender agora)")
        
        tipo_opcao = input("\nEscolha: ").strip()
        
        if tipo_opcao == "1":
            self._criar_atendimento_agendado()
        elif tipo_opcao == "2":
            self._criar_atendimento_walkin()
        else:
            print("Opção inválida!")
    
    def _criar_atendimento_agendado(self):
        """Cria atendimento para data futura"""
        print("\nAGENDAR ATENDIMENTO\n")
        
        # Selecionar cliente
        id_cliente = self._selecionar_cliente()
        if not id_cliente:
            return
        
        # Selecionar barbeiro
        id_barbeiro = self._selecionar_barbeiro()
        if not id_barbeiro:
            return
        
        # Data e horário
        data_agendada = input("\nData do atendimento (DD/MM/AAAA): ").strip()
        try:
            data_agendada = datetime.strptime(data_agendada, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("Data inválida!")
            return
        
        horario = input("Horário (HH:MM): ").strip()
        try:
            datetime.strptime(horario, "%H:%M")
        except ValueError:
            print("Horário inválido!")
            return
        
        observacoes = input("Observações (opcional): ").strip()
        if not observacoes:
            observacoes = None
        
        # Inserir atendimento
        query = """
            INSERT INTO atendimento (id_cliente, id_barbeiro, tipo, data_agendada, horario_agendado, status, data_atendimento, observacoes)
            VALUES (%s, %s, 'agendado', %s, %s, 'agendado', NULL, %s)
        """
        params = (id_cliente, id_barbeiro, data_agendada, horario, observacoes)
        
        if self.db.executar_comando(query, params):
            data_fmt = datetime.strptime(data_agendada, '%Y-%m-%d').strftime('%d/%m/%Y')
            print(f"\nAtendimento agendado com sucesso!")
            print(f"  Data: {data_fmt} às {horario}")
    
    def _criar_atendimento_walkin(self):
        """Cria atendimento walk-in (atender agora)"""
        print("\nATENDIMENTO WALK-IN\n")
        
        # Selecionar cliente
        id_cliente = self._selecionar_cliente()
        if not id_cliente:
            return
        
        # Selecionar barbeiro
        id_barbeiro = self._selecionar_barbeiro()
        if not id_barbeiro:
            return
        
        horario_inicio = datetime.now().strftime("%H:%M")
        observacoes = input("\nObservações (opcional): ").strip()
        if not observacoes:
            observacoes = None
        
        # Inserir atendimento
        query = """
            INSERT INTO atendimento (id_cliente, id_barbeiro, tipo, horario_inicio, status, observacoes)
            VALUES (%s, %s, 'walkin', %s, 'em_andamento', %s)
            RETURNING id_atendimento
        """
        params = (id_cliente, id_barbeiro, horario_inicio, observacoes)
        
        try:
            self.db.cursor.execute(query, params)
            id_atendimento = self.db.cursor.fetchone()[0]
            self.db.conn.commit()
            
            print(f"\nAtendimento #{id_atendimento} iniciado às {horario_inicio}!")
            print("  Não esqueça de adicionar os serviços e finalizar o atendimento.")
        except Exception as e:
            print(f"Erro ao criar atendimento: {e}")
            self.db.conn.rollback()
    
    def _selecionar_cliente(self):
        """Helper: Seleciona um cliente"""
        clientes = self.db.executar_query(
            "SELECT id_cliente, nome, telefone FROM cliente ORDER BY nome LIMIT 15"
        )
        
        if not clientes:
            print("Nenhum cliente cadastrado!")
            return None
        
        print("Clientes:")
        for cliente in clientes:
            print(f"  [{cliente[0]}] {cliente[1]} - {cliente[2]}")
        
        if len(clientes) == 15:
            print("  ... (mostrando apenas os primeiros 15)")
        
        id_cliente = input("\nID do Cliente: ").strip()
        
        if not id_cliente.isdigit():
            print("ID inválido!")
            return None
        
        # Verificar se existe
        verifica = self.db.executar_query(
            "SELECT nome FROM cliente WHERE id_cliente = %s", 
            (id_cliente,)
        )
        
        if not verifica:
            print("Cliente não encontrado!")
            return None
        
        print(f"Cliente: {verifica[0][0]}")
        return id_cliente
    
    def _selecionar_barbeiro(self):
        """Helper: Seleciona um barbeiro"""
        barbeiros = self.db.executar_query(
            "SELECT id_barbeiro, nome, especialidade FROM barbeiro WHERE ativo = TRUE ORDER BY nome"
        )
        
        if not barbeiros:
            print("Nenhum barbeiro ativo!")
            return None
        
        print("\nBarbeiros:")
        for barbeiro in barbeiros:
            espec = barbeiro[2] if barbeiro[2] else "Geral"
            print(f"  [{barbeiro[0]}] {barbeiro[1]} - {espec}")
        
        id_barbeiro = input("\nID do Barbeiro: ").strip()
        
        if not id_barbeiro.isdigit():
            print("ID inválido!")
            return None
        
        # Verificar se existe
        verifica = self.db.executar_query(
            "SELECT nome FROM barbeiro WHERE id_barbeiro = %s AND ativo = TRUE",
            (id_barbeiro,)
        )
        
        if not verifica:
            print("Barbeiro não encontrado ou inativo!")
            return None
        
        print(f"Barbeiro: {verifica[0][0]}")
        return id_barbeiro
    
    def listar_atendimentos_dia(self):
        """Lista atendimentos do dia (agendados e em andamento)"""
        print("\n=== ATENDIMENTOS DE HOJE ===\n")
        
        query = """
            SELECT 
                a.id_atendimento,
                c.nome as cliente,
                b.nome as barbeiro,
                COALESCE(a.horario_agendado, a.horario_inicio) as horario,
                a.tipo,
                a.status
            FROM atendimento a
            JOIN cliente c ON a.id_cliente = c.id_cliente
            JOIN barbeiro b ON a.id_barbeiro = b.id_barbeiro
            WHERE (a.data_agendada = CURRENT_DATE OR a.data_atendimento = CURRENT_DATE)
                AND a.status != 'cancelado'
            ORDER BY horario
        """
        
        atendimentos = self.db.executar_query(query)
        
        if not atendimentos:
            print("Nenhum atendimento para hoje.")
            return
        
        print(f"{'ID':<5} {'Horário':<10} {'Cliente':<25} {'Barbeiro':<20} {'Tipo':<12} {'Status':<15}")
        print("-" * 87)
        
        for atend in atendimentos:
            id_a, cliente, barbeiro, horario, tipo, status = atend
            horario_str = str(horario)[:5] if horario else "-"
            print(f"{id_a:<5} {horario_str:<10} {cliente:<25} {barbeiro:<20} {tipo:<12} {status:<15}")
        
        print(f"\nTotal: {len(atendimentos)} atendimento(s)")
    
    def adicionar_servicos_atendimento(self):
        """Adiciona serviços a um atendimento"""
        print("\n=== ADICIONAR SERVIÇOS AO ATENDIMENTO ===\n")
        
        id_atendimento = input("ID do atendimento: ").strip()
        if not id_atendimento.isdigit():
            print("ID inválido!")
            return
        
        # Verificar se atendimento existe
        atend = self.db.executar_query(
            "SELECT status FROM atendimento WHERE id_atendimento = %s",
            (id_atendimento,)
        )
        
        if not atend:
            print("Atendimento não encontrado!")
            return
        
        if atend[0][0] == 'finalizado':
            print("Atendimento já foi finalizado!")
            return
        
        if atend[0][0] == 'cancelado':
            print("Atendimento foi cancelado!")
            return
        
        # Listar serviços
        servicos = self.db.executar_query(
            "SELECT id_servico, nome, preco, duracao_estimada FROM servico WHERE ativo = TRUE ORDER BY nome"
        )
        
        if not servicos:
            print("Nenhum serviço disponível!")
            return
        
        print("\n💼 Serviços disponíveis:")
        for servico in servicos:
            preco_fmt = f"R$ {servico[2]:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"  [{servico[0]}] {servico[1]} - {preco_fmt} ({servico[3]} min)")
        
        print("\nDigite os IDs dos serviços separados por vírgula")
        print("Exemplo: 1,3,5")
        
        ids_servicos = input("\nServiços: ").strip().split(',')
        
        valor_total = 0
        servicos_adicionados = []
        
        for id_s in ids_servicos:
            id_s = id_s.strip()
            if not id_s.isdigit():
                continue
            
            # Buscar preço do serviço
            servico_info = self.db.executar_query(
                "SELECT nome, preco FROM servico WHERE id_servico = %s AND ativo = TRUE",
                (id_s,)
            )
            
            if not servico_info:
                print(f"Serviço {id_s} não encontrado, pulando...")
                continue
            
            nome_servico, preco = servico_info[0]
            
            # Verificar se já não foi adicionado
            verifica = self.db.executar_query(
                "SELECT 1 FROM atendimento_servico WHERE id_atendimento = %s AND id_servico = %s",
                (id_atendimento, id_s)
            )
            
            if verifica:
                print(f"Serviço '{nome_servico}' já foi adicionado, pulando...")
                continue
            
            # Inserir na tabela associativa
            query = """
                INSERT INTO atendimento_servico (id_atendimento, id_servico, preco_cobrado)
                VALUES (%s, %s, %s)
            """
            try:
                self.db.cursor.execute(query, (id_atendimento, id_s, preco))
                valor_total += float(preco)
                servicos_adicionados.append(nome_servico)
            except Exception as e:
                print(f"Erro ao adicionar serviço: {e}")
        
        if servicos_adicionados:
            self.db.conn.commit()
            print(f"\nServiços adicionados:")
            for s in servicos_adicionados:
                print(f"  • {s}")
            
            valor_fmt = f"R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"\nValor total dos serviços: {valor_fmt}")
        else:
            print("\nNenhum serviço válido foi adicionado.")
    
    def finalizar_atendimento(self):
        """Finaliza um atendimento em andamento"""
        print("\n=== FINALIZAR ATENDIMENTO ===\n")
        
        # Listar atendimentos em andamento
        query = """
            SELECT 
                a.id_atendimento,
                c.nome as cliente,
                b.nome as barbeiro,
                a.horario_inicio,
                a.tipo
            FROM atendimento a
            JOIN cliente c ON a.id_cliente = c.id_cliente
            JOIN barbeiro b ON a.id_barbeiro = b.id_barbeiro
            WHERE a.status IN ('agendado', 'em_andamento')
            ORDER BY a.data_atendimento DESC, a.horario_inicio DESC
            LIMIT 10
        """
        
        atendimentos = self.db.executar_query(query)
        
        if not atendimentos:
            print("Nenhum atendimento em andamento.")
            return
        
        print("Atendimentos em andamento:")
        for atend in atendimentos:
            horario = str(atend[3])[:5] if atend[3] else "-"
            print(f"  [{atend[0]}] {atend[1]} com {atend[2]} - {horario} ({atend[4]})")
        
        id_atendimento = input("\nID do atendimento: ").strip()
        if not id_atendimento.isdigit():
            print("ID inválido!")
            return
        
        # Calcular valor dos serviços
        query_servicos = """
            SELECT COALESCE(SUM(preco_cobrado), 0)
            FROM atendimento_servico
            WHERE id_atendimento = %s
        """
        valor_servicos = self.db.executar_query(query_servicos, (id_atendimento,))
        valor_total = float(valor_servicos[0][0]) if valor_servicos else 0.0
        
        if valor_total == 0:
            print("\nATENÇÃO: Nenhum serviço foi adicionado a este atendimento!")
            adicionar = input("Deseja adicionar serviços antes de finalizar? (S/N): ").strip().upper()
            if adicionar == 'S':
                print("Use a opção 'Adicionar Serviços ao Atendimento' no menu.")
                return
        
        print(f"\nValor dos serviços: R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        
        # Perguntar sobre produtos
        vender_produtos = input("\nDeseja adicionar venda de produtos? (S/N): ").strip().upper()
        if vender_produtos == 'S':
            valor_produtos = self._vender_produtos(id_atendimento)
            valor_total += valor_produtos
        
        # Horário de término
        horario_fim = input("\nHorário de término (HH:MM) [Enter = agora]: ").strip()
        if not horario_fim:
            horario_fim = datetime.now().strftime("%H:%M")
        else:
            try:
                datetime.strptime(horario_fim, "%H:%M")
            except ValueError:
                print("⚠️  Horário inválido, usando horário atual.")
                horario_fim = datetime.now().strftime("%H:%M")
        
        # Forma de pagamento
        print("\nFormas de pagamento:")
        print("[1] Dinheiro")
        print("[2] PIX")
        print("[3] Cartão Débito")
        print("[4] Cartão Crédito")
        
        forma_opcao = input("\nEscolha: ").strip()
        formas = {
            '1': 'dinheiro',
            '2': 'pix',
            '3': 'cartao_debito',
            '4': 'cartao_credito'
        }
        forma_pagamento = formas.get(forma_opcao, 'dinheiro')
        
        observacoes = input("Observações finais (opcional): ").strip()
        if not observacoes:
            observacoes = None
        
        # Finalizar
        query = """
            UPDATE atendimento 
            SET horario_fim = %s, 
                valor_total = %s, 
                forma_pagamento = %s, 
                status = 'finalizado',
                observacoes = COALESCE(%s, observacoes)
            WHERE id_atendimento = %s
        """
        params = (horario_fim, valor_total, forma_pagamento, observacoes, id_atendimento)
        
        if self.db.executar_comando(query, params):
            valor_fmt = f"R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"\nAtendimento #{id_atendimento} finalizado!")
            print(f"  Valor total: {valor_fmt}")
            print(f"  Pagamento: {forma_pagamento}")
    
    def _vender_produtos(self, id_atendimento):
        """Helper: Vende produtos durante atendimento"""
        print("\n📦 VENDA DE PRODUTOS\n")
        
        produtos = self.db.executar_query(
            "SELECT id_produto, nome, preco_venda, estoque_atual FROM produto WHERE ativo = TRUE AND estoque_atual > 0 ORDER BY nome"
        )
        
        if not produtos:
            print("Nenhum produto disponível em estoque!")
            return 0.0
        
        print("Produtos disponíveis:")
        for produto in produtos:
            preco_fmt = f"R$ {produto[2]:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"  [{produto[0]}] {produto[1]} - {preco_fmt} (Estoque: {produto[3]})")
        
        valor_total_produtos = 0.0
        
        while True:
            id_produto = input("\nID do produto (ou Enter para finalizar): ").strip()
            
            if not id_produto:
                break
            
            if not id_produto.isdigit():
                print("ID inválido!")
                continue
            
            # Buscar produto
            produto_info = self.db.executar_query(
                "SELECT nome, preco_venda, estoque_atual FROM produto WHERE id_produto = %s AND ativo = TRUE",
                (id_produto,)
            )
            
            if not produto_info:
                print("Produto não encontrado!")
                continue
            
            nome, preco, estoque = produto_info[0]
            
            if estoque <= 0:
                print(f"Produto '{nome}' sem estoque!")
                continue
            
            quantidade = input(f"Quantidade (máx {estoque}): ").strip()
            try:
                quantidade = int(quantidade)
                if quantidade <= 0 or quantidade > estoque:
                    print("Quantidade inválida!")
                    continue
            except ValueError:
                print("Quantidade inválida!")
                continue
            
            subtotal = float(preco) * quantidade
            
            try:
                # Inserir venda
                query = """
                    INSERT INTO venda_produto (id_atendimento, id_produto, quantidade, preco_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.db.cursor.execute(query, (id_atendimento, id_produto, quantidade, preco, subtotal))
                
                # Atualizar estoque
                query_estoque = "UPDATE produto SET estoque_atual = estoque_atual - %s WHERE id_produto = %s"
                self.db.cursor.execute(query_estoque, (quantidade, id_produto))
                
                self.db.conn.commit()
                
                subtotal_fmt = f"R$ {subtotal:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"{quantidade}x {nome} - {subtotal_fmt}")
                
                valor_total_produtos += subtotal
            except Exception as e:
                print(f"Erro ao registrar venda: {e}")
                self.db.conn.rollback()
        
        if valor_total_produtos > 0:
            total_fmt = f"R$ {valor_total_produtos:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"\nTotal em produtos: {total_fmt}")
        
        return valor_total_produtos
    
    def cancelar_atendimento(self):
        """Cancela um atendimento agendado"""
        print("\n=== CANCELAR ATENDIMENTO ===\n")
        
        # Listar atendimentos agendados
        query = """
            SELECT 
                a.id_atendimento,
                c.nome as cliente,
                b.nome as barbeiro,
                a.data_agendada,
                a.horario_agendado
            FROM atendimento a
            JOIN cliente c ON a.id_cliente = c.id_cliente
            JOIN barbeiro b ON a.id_barbeiro = b.id_barbeiro
            WHERE a.status = 'agendado'
                AND a.data_agendada >= CURRENT_DATE
            ORDER BY a.data_agendada, a.horario_agendado
        """
        
        atendimentos = self.db.executar_query(query)
        
        if not atendimentos:
            print("Nenhum atendimento agendado para cancelar.")
            return
        
        print("📋 Atendimentos agendados:")
        for atend in atendimentos:
            data_fmt = datetime.strptime(str(atend[3]), "%Y-%m-%d").strftime("%d/%m/%Y")
            horario = str(atend[4])[:5]
            print(f"  [{atend[0]}] {data_fmt} {horario} - {atend[1]} com {atend[2]}")
        
        id_atendimento = input("\nID do atendimento para cancelar: ").strip()
        if not id_atendimento.isdigit():
            print("ID inválido!")
            return
        
        motivo = input("Motivo do cancelamento (opcional): ").strip()
        if motivo:
            observacao = f"Cancelado. Motivo: {motivo}"
        else:
            observacao = "Cancelado"
        
        query = "UPDATE atendimento SET status = 'cancelado', observacoes = %s WHERE id_atendimento = %s"
        
        if self.db.executar_comando(query, (observacao, id_atendimento)):
            print("\nAtendimento cancelado!")


def menu_processos(db: Database):
    """Menu de processos de negócio"""
    processos = ProcessosNegocio(db)
    
    while True:
        print("\n" + "="*60)
        print("          PROCESSOS DE NEGÓCIO")
        print("="*60)
        print("\n[1] Novo Atendimento (Agendar ou Walk-in)")
        print("[2] Ver Atendimentos de Hoje")
        print("[3] Adicionar Serviços ao Atendimento")
        print("[4] Finalizar Atendimento")
        print("[5] Cancelar Atendimento Agendado")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            processos.novo_atendimento()
        elif opcao == "2":
            processos.listar_atendimentos_dia()
        elif opcao == "3":
            processos.adicionar_servicos_atendimento()
        elif opcao == "4":
            processos.finalizar_atendimento()
        elif opcao == "5":
            processos.cancelar_atendimento()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
        
        input("\nPressione ENTER para continuar...")