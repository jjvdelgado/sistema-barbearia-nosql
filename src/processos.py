import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from bson import ObjectId
from datetime import datetime, timedelta

class ProcessosNegocio:
    def __init__(self, db: DatabaseMongo):
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
            print("❌ Opção inválida!")
    
    def _criar_atendimento_agendado(self):
        """Cria atendimento para data futura"""
        print("\n📅 AGENDAR ATENDIMENTO\n")
        
        # Selecionar cliente
        cliente = self._selecionar_cliente()
        if not cliente:
            return
        
        # Selecionar barbeiro
        barbeiro = self._selecionar_barbeiro()
        if not barbeiro:
            return
        
        # Data e horário
        data_agendada = input("\nData do atendimento (DD/MM/AAAA): ").strip()
        try:
            data_agendada = datetime.strptime(data_agendada, "%d/%m/%Y")
        except ValueError:
            print("❌ Data inválida!")
            return
        
        horario = input("Horário (HH:MM): ").strip()
        try:
            datetime.strptime(horario, "%H:%M")
        except ValueError:
            print("❌ Horário inválido!")
            return
        
        observacoes = input("Observações (opcional): ").strip() or None
        
        # Criar documento de atendimento
        atendimento = {
            "cliente_id": cliente['_id'],
            "barbeiro_id": barbeiro['_id'],
            "cliente": {
                "nome": cliente['nome'],
                "telefone": cliente['telefone']
            },
            "barbeiro": {
                "nome": barbeiro['nome'],
                "comissao_percentual": barbeiro.get('comissao_percentual', 30.0)
            },
            "tipo": "agendado",
            "status": "agendado",
            "data_agendada": data_agendada,
            "horario_agendado": horario,
            "data_atendimento": None,
            "horario_inicio": None,
            "horario_fim": None,
            "servicos": [],
            "produtos_vendidos": [],
            "valor_servicos": 0.0,
            "valor_produtos": 0.0,
            "valor_total": 0.0,
            "comissao_barbeiro": 0.0,
            "forma_pagamento": None,
            "observacoes": observacoes,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        atendimento_id = self.db.inserir("atendimentos", atendimento)
        
        if atendimento_id:
            data_fmt = data_agendada.strftime('%d/%m/%Y')
            print(f"\n✅ Atendimento agendado com sucesso!")
            print(f"   ID: {atendimento_id}")
            print(f"   Data: {data_fmt} às {horario}")
            print(f"   Cliente: {cliente['nome']}")
            print(f"   Barbeiro: {barbeiro['nome']}")
        else:
            print("\n❌ Erro ao agendar atendimento!")
    
    def _criar_atendimento_walkin(self):
        """Cria atendimento walk-in (atender agora)"""
        print("\n🚶 ATENDIMENTO WALK-IN\n")
        
        # Selecionar cliente
        cliente = self._selecionar_cliente()
        if not cliente:
            return
        
        # Selecionar barbeiro
        barbeiro = self._selecionar_barbeiro()
        if not barbeiro:
            return
        
        horario_inicio = datetime.now().strftime("%H:%M")
        observacoes = input("\nObservações (opcional): ").strip() or None
        
        # Criar documento de atendimento
        atendimento = {
            "cliente_id": cliente['_id'],
            "barbeiro_id": barbeiro['_id'],
            "cliente": {
                "nome": cliente['nome'],
                "telefone": cliente['telefone']
            },
            "barbeiro": {
                "nome": barbeiro['nome'],
                "comissao_percentual": barbeiro.get('comissao_percentual', 30.0)
            },
            "tipo": "walkin",
            "status": "em_andamento",
            "data_agendada": None,
            "horario_agendado": None,
            "data_atendimento": datetime.now(),
            "horario_inicio": horario_inicio,
            "horario_fim": None,
            "servicos": [],
            "produtos_vendidos": [],
            "valor_servicos": 0.0,
            "valor_produtos": 0.0,
            "valor_total": 0.0,
            "comissao_barbeiro": 0.0,
            "forma_pagamento": None,
            "observacoes": observacoes,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        atendimento_id = self.db.inserir("atendimentos", atendimento)
        
        if atendimento_id:
            print(f"\n✅ Atendimento iniciado com sucesso!")
            print(f"   ID: {atendimento_id}")
            print(f"   Horário: {horario_inicio}")
            print(f"   Cliente: {cliente['nome']}")
            print(f"   Barbeiro: {barbeiro['nome']}")
            print("\n💡 Não esqueça de adicionar os serviços e finalizar o atendimento.")
        else:
            print("\n❌ Erro ao criar atendimento!")
    
    def _selecionar_cliente(self):
        """Helper: Seleciona um cliente"""
        from pymongo import ASCENDING
        
        clientes = self.db.buscar_todos(
            "clientes",
            ordenacao=[("nome", ASCENDING)],
            limite=15
        )
        
        if not clientes:
            print("❌ Nenhum cliente cadastrado!")
            return None
        
        print("👥 Clientes:")
        for cliente in clientes:
            print(f"  • {cliente['nome']} - {cliente['telefone']}")
        
        if len(clientes) == 15:
            print("  ... (mostrando apenas os primeiros 15)")
        
        nome_busca = input("\nNome do cliente (pode ser parcial): ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return None
        
        # Buscar cliente
        cliente = self.db.buscar_um("clientes", {"nome": {"$regex": f"^{nome_busca}", "$options": "i"}})
        
        if not cliente:
            # Tentar busca parcial
            clientes_encontrados = self.db.buscar_todos(
                "clientes",
                {"nome": {"$regex": nome_busca, "$options": "i"}},
                ordenacao=[("nome", ASCENDING)],
                limite=5
            )
            
            if not clientes_encontrados:
                print(f"❌ Cliente '{nome_busca}' não encontrado!")
                return None
            
            if len(clientes_encontrados) > 1:
                print(f"\n✅ Encontrados {len(clientes_encontrados)} clientes:\n")
                for i, c in enumerate(clientes_encontrados, 1):
                    print(f"[{i}] {c['nome']} - {c['telefone']}")
                
                escolha = input("\nEscolha o número: ").strip()
                try:
                    idx = int(escolha) - 1
                    if idx < 0 or idx >= len(clientes_encontrados):
                        print("❌ Opção inválida!")
                        return None
                    cliente = clientes_encontrados[idx]
                except ValueError:
                    print("❌ Opção inválida!")
                    return None
            else:
                cliente = clientes_encontrados[0]
        
        print(f"✅ Cliente selecionado: {cliente['nome']}")
        return cliente
    
    def _selecionar_barbeiro(self):
        """Helper: Seleciona um barbeiro"""
        from pymongo import ASCENDING
        
        barbeiros = self.db.buscar_todos(
            "barbeiros",
            {"ativo": True},
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not barbeiros:
            print("❌ Nenhum barbeiro ativo!")
            return None
        
        print("\n💈 Barbeiros disponíveis:")
        for barbeiro in barbeiros:
            espec = barbeiro.get('especialidade', 'Geral')
            print(f"  • {barbeiro['nome']} - {espec}")
        
        nome_busca = input("\nNome do barbeiro: ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return None
        
        # Buscar barbeiro
        barbeiro = self.db.buscar_um("barbeiros", {
            "nome": {"$regex": f"^{nome_busca}", "$options": "i"},
            "ativo": True
        })
        
        if not barbeiro:
            print(f"❌ Barbeiro '{nome_busca}' não encontrado ou inativo!")
            return None
        
        print(f"✅ Barbeiro selecionado: {barbeiro['nome']}")
        return barbeiro
    
    def listar_atendimentos_dia(self):
        """Lista atendimentos do dia (agendados e em andamento)"""
        print("\n=== ATENDIMENTOS DE HOJE ===\n")
        
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        amanha = hoje + timedelta(days=1)
        
        # Buscar atendimentos de hoje
        filtro = {
            "$or": [
                {
                    "data_agendada": {
                        "$gte": hoje,
                        "$lt": amanha
                    }
                },
                {
                    "data_atendimento": {
                        "$gte": hoje,
                        "$lt": amanha
                    }
                }
            ],
            "status": {"$ne": "cancelado"}
        }
        
        atendimentos = self.db.buscar_todos(
            "atendimentos",
            filtro,
            ordenacao=[("horario_agendado", 1), ("horario_inicio", 1)]
        )
        
        if not atendimentos:
            print("⚠️  Nenhum atendimento para hoje.")
            return
        
        print(f"{'ID':<26} {'Horário':<10} {'Cliente':<25} {'Barbeiro':<20} {'Tipo':<12} {'Status':<15}")
        print("-" * 108)
        
        for atend in atendimentos:
            id_str = str(atend['_id'])[:24]
            horario = atend.get('horario_agendado') or atend.get('horario_inicio') or '-'
            cliente = atend['cliente']['nome'][:23]
            barbeiro = atend['barbeiro']['nome'][:18]
            tipo = atend['tipo']
            status = atend['status']
            
            print(f"{id_str:<26} {horario:<10} {cliente:<25} {barbeiro:<20} {tipo:<12} {status:<15}")
        
        print(f"\nTotal: {len(atendimentos)} atendimento(s)")
    
    def adicionar_servicos_atendimento(self):
        """Adiciona serviços a um atendimento"""
        print("\n=== ADICIONAR SERVIÇOS AO ATENDIMENTO ===\n")
        
        # Listar atendimentos recentes em andamento
        atendimentos = self.db.buscar_todos(
            "atendimentos",
            {"status": {"$in": ["agendado", "em_andamento"]}},
            ordenacao=[("created_at", -1)],
            limite=20
        )
        
        if not atendimentos:
            print("Nenhum atendimento em andamento.")
            return
        
        print("Atendimentos disponiveis:\n")
        for atend in atendimentos:
            cliente = atend['cliente']['nome']
            barbeiro = atend['barbeiro']['nome']
            status = atend['status']
            horario = atend.get('horario_inicio', atend.get('horario_agendado', '-'))
            print(f"  - {cliente} com {barbeiro} - {horario} ({status})")
        
        # BUSCAR POR NOME DO CLIENTE
        nome_cliente = input("\nNome do cliente (pode ser parcial): ").strip()
        
        if not nome_cliente:
            print("Nome e obrigatorio!")
            return
        
        # Filtrar atendimentos por nome do cliente
        atendimentos_filtrados = [
            atend for atend in atendimentos 
            if nome_cliente.lower() in atend['cliente']['nome'].lower()
        ]
        
        if not atendimentos_filtrados:
            print(f"\nNenhum atendimento encontrado para cliente '{nome_cliente}'")
            return
        
        # Se encontrou múltiplos, listar para escolher
        if len(atendimentos_filtrados) > 1:
            print(f"\nEncontrados {len(atendimentos_filtrados)} atendimentos:\n")
            for i, atend in enumerate(atendimentos_filtrados, 1):
                cliente = atend['cliente']['nome']
                barbeiro = atend['barbeiro']['nome']
                horario = atend.get('horario_inicio', atend.get('horario_agendado', '-'))
                status = atend['status']
                print(f"[{i}] {cliente} com {barbeiro} - {horario} ({status})")
            
            escolha = input("\nEscolha o numero: ").strip()
            try:
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(atendimentos_filtrados):
                    print("Opcao invalida!")
                    return
                atendimento = atendimentos_filtrados[idx]
            except ValueError:
                print("Opcao invalida!")
                return
        else:
            atendimento = atendimentos_filtrados[0]
            print(f"\nAtendimento selecionado: {atendimento['cliente']['nome']} com {atendimento['barbeiro']['nome']}")
        
        # Verificar status
        if atendimento['status'] == 'finalizado':
            print("Atendimento ja foi finalizado!")
            return
        
        if atendimento['status'] == 'cancelado':
            print("Atendimento foi cancelado!")
            return
        
        # Listar serviços disponíveis
        from pymongo import ASCENDING
        
        servicos = self.db.buscar_todos(
            "servicos",
            {"ativo": True},
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not servicos:
            print("Nenhum servico disponivel!")
            return
        
        print("\nServicos disponiveis:")
        for i, servico in enumerate(servicos, 1):
            preco = servico['preco']
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            duracao = servico['duracao_estimada']
            print(f"  [{i}] {servico['nome']} - {preco_fmt} ({duracao} min)")
        
        print("\nDigite os numeros dos servicos separados por virgula")
        print("Exemplo: 1,3,5")
        
        indices = input("\nServicos: ").strip().split(',')
        
        servicos_para_adicionar = []
        valor_total = 0.0
        
        for idx_str in indices:
            idx_str = idx_str.strip()
            if not idx_str.isdigit():
                continue
            
            idx = int(idx_str) - 1
            if idx < 0 or idx >= len(servicos):
                continue
            
            servico = servicos[idx]
            
            # Verificar se já não foi adicionado
            ja_adicionado = False
            for s in atendimento.get('servicos', []):
                if s.get('servico_id') == servico['_id']:
                    print(f"Servico '{servico['nome']}' ja foi adicionado, pulando...")
                    ja_adicionado = True
                    break
            
            if ja_adicionado:
                continue
            
            servicos_para_adicionar.append({
                "servico_id": servico['_id'],
                "nome": servico['nome'],
                "preco_cobrado": servico['preco']
            })
            
            valor_total += servico['preco']
        
        if servicos_para_adicionar:
            # Atualizar atendimento com novos serviços
            novos_servicos = atendimento.get('servicos', []) + servicos_para_adicionar
            novo_valor_servicos = atendimento.get('valor_servicos', 0.0) + valor_total
            
            atualizacao = {
                "servicos": novos_servicos,
                "valor_servicos": novo_valor_servicos,
                "valor_total": novo_valor_servicos + atendimento.get('valor_produtos', 0.0),
                "updated_at": datetime.now()
            }
            
            # Recalcular comissão
            comissao_pct = atendimento['barbeiro'].get('comissao_percentual', 30.0)
            atualizacao['comissao_barbeiro'] = atualizacao['valor_total'] * (comissao_pct / 100)
            
            if self.db.atualizar("atendimentos", {"_id": atendimento['_id']}, atualizacao):
                print(f"\nServicos adicionados:")
                for s in servicos_para_adicionar:
                    print(f"   - {s['nome']}")
                
                valor_fmt = f"R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"\nValor adicionado: {valor_fmt}")
                
                total_fmt = f"R$ {atualizacao['valor_total']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"Valor total do atendimento: {total_fmt}")
            else:
                print("\nErro ao adicionar servicos!")
        else:
            print("\nNenhum servico valido foi adicionado.")
    
    def finalizar_atendimento(self):
        """Finaliza um atendimento em andamento"""
        print("\n=== FINALIZAR ATENDIMENTO ===\n")
        
        # Listar atendimentos em andamento
        atendimentos = self.db.buscar_todos(
            "atendimentos",
            {"status": {"$in": ["agendado", "em_andamento"]}},
            ordenacao=[("created_at", -1)],
            limite=20
        )
        
        if not atendimentos:
            print("Nenhum atendimento em andamento.")
            return
        
        print("Atendimentos em andamento:\n")
        for atend in atendimentos:
            cliente = atend['cliente']['nome']
            barbeiro = atend['barbeiro']['nome']
            horario = atend.get('horario_inicio', atend.get('horario_agendado', '-'))
            tipo = atend['tipo']
            print(f"  - {cliente} com {barbeiro} - {horario} ({tipo})")
        
        # BUSCAR POR NOME DO CLIENTE
        nome_cliente = input("\nNome do cliente (pode ser parcial): ").strip()
        
        if not nome_cliente:
            print("Nome e obrigatorio!")
            return
        
        # Filtrar atendimentos por nome do cliente
        atendimentos_filtrados = [
            atend for atend in atendimentos 
            if nome_cliente.lower() in atend['cliente']['nome'].lower()
        ]
        
        if not atendimentos_filtrados:
            print(f"\nNenhum atendimento encontrado para cliente '{nome_cliente}'")
            return
        
        # Se encontrou múltiplos, listar para escolher
        if len(atendimentos_filtrados) > 1:
            print(f"\nEncontrados {len(atendimentos_filtrados)} atendimentos:\n")
            for i, atend in enumerate(atendimentos_filtrados, 1):
                cliente = atend['cliente']['nome']
                barbeiro = atend['barbeiro']['nome']
                horario = atend.get('horario_inicio', atend.get('horario_agendado', '-'))
                tipo = atend['tipo']
                print(f"[{i}] {cliente} com {barbeiro} - {horario} ({tipo})")
            
            escolha = input("\nEscolha o numero: ").strip()
            try:
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(atendimentos_filtrados):
                    print("Opcao invalida!")
                    return
                atendimento = atendimentos_filtrados[idx]
            except ValueError:
                print("Opcao invalida!")
                return
        else:
            atendimento = atendimentos_filtrados[0]
            print(f"\nAtendimento selecionado: {atendimento['cliente']['nome']} com {atendimento['barbeiro']['nome']}")
        
        # Verificar serviços
        valor_servicos = atendimento.get('valor_servicos', 0.0)
        
        if valor_servicos == 0:
            print("\nATENCAO: Nenhum servico foi adicionado a este atendimento!")
            adicionar = input("Deseja adicionar servicos antes de finalizar? (S/N): ").strip().upper()
            if adicionar == 'S':
                print("Use a opcao 'Adicionar Servicos ao Atendimento' no menu.")
                return
        
        print(f"\nValor dos servicos: R$ {valor_servicos:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        
        # Perguntar sobre produtos
        valor_produtos = atendimento.get('valor_produtos', 0.0)
        
        vender_produtos = input("\nDeseja adicionar venda de produtos? (S/N): ").strip().upper()
        if vender_produtos == 'S':
            valor_produtos_novos = self._vender_produtos(atendimento)
            valor_produtos += valor_produtos_novos
        
        valor_total = valor_servicos + valor_produtos
        
        # Horário de término
        horario_fim = input("\nHorario de termino (HH:MM) [Enter = agora]: ").strip()
        if not horario_fim:
            horario_fim = datetime.now().strftime("%H:%M")
        else:
            try:
                datetime.strptime(horario_fim, "%H:%M")
            except ValueError:
                print("Horario invalido, usando horario atual.")
                horario_fim = datetime.now().strftime("%H:%M")
        
        # Forma de pagamento
        print("\nFormas de pagamento:")
        print("[1] Dinheiro")
        print("[2] PIX")
        print("[3] Cartao Debito")
        print("[4] Cartao Credito")
        
        forma_opcao = input("\nEscolha: ").strip()
        formas = {
            '1': 'dinheiro',
            '2': 'pix',
            '3': 'cartao_debito',
            '4': 'cartao_credito'
        }
        forma_pagamento = formas.get(forma_opcao, 'dinheiro')
        
        observacoes = input("Observacoes finais (opcional): ").strip() or atendimento.get('observacoes')
        
        # Calcular comissão
        comissao_pct = atendimento['barbeiro'].get('comissao_percentual', 30.0)
        comissao = valor_total * (comissao_pct / 100)
        
        # Finalizar atendimento
        atualizacao = {
            "horario_fim": horario_fim,
            "data_atendimento": atendimento.get('data_atendimento') or datetime.now(),
            "valor_produtos": valor_produtos,
            "valor_total": valor_total,
            "comissao_barbeiro": comissao,
            "forma_pagamento": forma_pagamento,
            "status": "finalizado",
            "observacoes": observacoes,
            "updated_at": datetime.now()
        }
        
        if self.db.atualizar("atendimentos", {"_id": atendimento['_id']}, atualizacao):
            valor_fmt = f"R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            comissao_fmt = f"R$ {comissao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"\nAtendimento finalizado com sucesso!")
            print(f"   Cliente: {atendimento['cliente']['nome']}")
            print(f"   Barbeiro: {atendimento['barbeiro']['nome']}")
            print(f"   Valor total: {valor_fmt}")
            print(f"   Pagamento: {forma_pagamento}")
            print(f"   Comissao barbeiro ({comissao_pct}%): {comissao_fmt}")
            
            # Atualizar estatísticas do cliente
            self._atualizar_stats_cliente(atendimento['cliente_id'], valor_total)
        else:
            print("\nErro ao finalizar atendimento!")
    
    def _vender_produtos(self, atendimento):
        """Helper: Vende produtos durante atendimento"""
        print("\n📦 VENDA DE PRODUTOS\n")
        
        from pymongo import ASCENDING
        
        produtos = self.db.buscar_todos(
            "produtos",
            {"ativo": True, "estoque_atual": {"$gt": 0}},
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not produtos:
            print("⚠️  Nenhum produto disponível em estoque!")
            return 0.0
        
        print("Produtos disponíveis:")
        for i, produto in enumerate(produtos, 1):
            preco = produto['preco_venda']
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            estoque = produto['estoque_atual']
            print(f"  [{i}] {produto['nome']} - {preco_fmt} (Estoque: {estoque})")
        
        produtos_vendidos = atendimento.get('produtos_vendidos', [])
        valor_total_produtos = 0.0
        
        while True:
            escolha = input("\nNúmero do produto (ou Enter para finalizar): ").strip()
            
            if not escolha:
                break
            
            if not escolha.isdigit():
                print("❌ Número inválido!")
                continue
            
            idx = int(escolha) - 1
            if idx < 0 or idx >= len(produtos):
                print("❌ Produto não encontrado!")
                continue
            
            produto = produtos[idx]
            estoque = produto['estoque_atual']
            
            if estoque <= 0:
                print(f"❌ Produto '{produto['nome']}' sem estoque!")
                continue
            
            quantidade = input(f"Quantidade (máx {estoque}): ").strip()
            try:
                quantidade = int(quantidade)
                if quantidade <= 0 or quantidade > estoque:
                    print("❌ Quantidade inválida!")
                    continue
            except ValueError:
                print("❌ Quantidade inválida!")
                continue
            
            preco = produto['preco_venda']
            subtotal = preco * quantidade
            
            # Adicionar à lista de produtos vendidos
            produtos_vendidos.append({
                "produto_id": produto['_id'],
                "nome": produto['nome'],
                "quantidade": quantidade,
                "preco_unitario": preco,
                "subtotal": subtotal
            })
            
            # Atualizar estoque
            novo_estoque = estoque - quantidade
            self.db.atualizar("produtos", {"_id": produto['_id']}, {"estoque_atual": novo_estoque})
            
            # Atualizar produto na lista local
            produto['estoque_atual'] = novo_estoque
            
            subtotal_fmt = f"R$ {subtotal:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"✅ {quantidade}x {produto['nome']} - {subtotal_fmt}")
            
            valor_total_produtos += subtotal
        
        if valor_total_produtos > 0:
            # Atualizar atendimento com produtos
            valor_servicos = atendimento.get('valor_servicos', 0.0)
            novo_valor_total = valor_servicos + valor_total_produtos
            comissao_pct = atendimento['barbeiro'].get('comissao_percentual', 30.0)
            
            self.db.atualizar("atendimentos", {"_id": atendimento['_id']}, {
                "produtos_vendidos": produtos_vendidos,
                "valor_produtos": valor_total_produtos,
                "valor_total": novo_valor_total,
                "comissao_barbeiro": novo_valor_total * (comissao_pct / 100),
                "updated_at": datetime.now()
            })
            
            total_fmt = f"R$ {valor_total_produtos:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"\n💰 Total em produtos: {total_fmt}")
        
        return valor_total_produtos
    
    def _atualizar_stats_cliente(self, cliente_id, valor_gasto):
        """Helper: Atualiza estatísticas do cliente"""
        cliente = self.db.buscar_um("clientes", {"_id": cliente_id})
        
        if cliente:
            stats = cliente.get('stats', {})
            stats['total_atendimentos'] = stats.get('total_atendimentos', 0) + 1
            stats['valor_total_gasto'] = stats.get('valor_total_gasto', 0.0) + valor_gasto
            stats['ultima_visita'] = datetime.now()
            
            self.db.atualizar("clientes", {"_id": cliente_id}, {"stats": stats})
    
    def cancelar_atendimento(self):
        """Cancela um atendimento agendado"""
        print("\n=== CANCELAR ATENDIMENTO ===\n")
        
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Listar atendimentos agendados
        atendimentos = self.db.buscar_todos(
            "atendimentos",
            {
                "status": "agendado",
                "data_agendada": {"$gte": hoje}
            },
            ordenacao=[("data_agendada", 1), ("horario_agendado", 1)]
        )
        
        if not atendimentos:
            print("Nenhum atendimento agendado para cancelar.")
            return
        
        print("Atendimentos agendados:\n")
        for atend in atendimentos:
            data_fmt = atend['data_agendada'].strftime("%d/%m/%Y")
            horario = atend['horario_agendado']
            cliente = atend['cliente']['nome']
            barbeiro = atend['barbeiro']['nome']
            print(f"  - {data_fmt} {horario} - {cliente} com {barbeiro}")
        
        # BUSCAR POR NOME DO CLIENTE
        nome_cliente = input("\nNome do cliente (pode ser parcial): ").strip()
        
        if not nome_cliente:
            print("Nome e obrigatorio!")
            return
        
        # Filtrar atendimentos por nome do cliente
        atendimentos_filtrados = [
            atend for atend in atendimentos 
            if nome_cliente.lower() in atend['cliente']['nome'].lower()
        ]
        
        if not atendimentos_filtrados:
            print(f"\nNenhum atendimento encontrado para cliente '{nome_cliente}'")
            return
        
        # Se encontrou múltiplos, listar para escolher
        if len(atendimentos_filtrados) > 1:
            print(f"\nEncontrados {len(atendimentos_filtrados)} atendimentos:\n")
            for i, atend in enumerate(atendimentos_filtrados, 1):
                data_fmt = atend['data_agendada'].strftime("%d/%m/%Y")
                horario = atend['horario_agendado']
                cliente = atend['cliente']['nome']
                barbeiro = atend['barbeiro']['nome']
                print(f"[{i}] {data_fmt} {horario} - {cliente} com {barbeiro}")
            
            escolha = input("\nEscolha o numero: ").strip()
            try:
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(atendimentos_filtrados):
                    print("Opcao invalida!")
                    return
                atendimento = atendimentos_filtrados[idx]
            except ValueError:
                print("Opcao invalida!")
                return
        else:
            atendimento = atendimentos_filtrados[0]
            print(f"\nAtendimento selecionado: {atendimento['cliente']['nome']} - {atendimento['data_agendada'].strftime('%d/%m/%Y')} {atendimento['horario_agendado']}")
        
        motivo = input("\nMotivo do cancelamento (opcional): ").strip()
        observacao = f"Cancelado. Motivo: {motivo}" if motivo else "Cancelado"
        
        if self.db.atualizar("atendimentos", {"_id": atendimento['_id']}, {
            "status": "cancelado",
            "observacoes": observacao,
            "updated_at": datetime.now()
        }):
            print("\nAtendimento cancelado!")
        else:
            print("\nErro ao cancelar atendimento!")


def menu_processos(db: DatabaseMongo):
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
            print("\n❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")