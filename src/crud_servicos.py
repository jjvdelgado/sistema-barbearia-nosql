import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from bson import ObjectId

class CRUDServico:
    def __init__(self, db: DatabaseMongo):
        self.db = db
    
    def criar_servico(self):
        """Cadastra um novo serviço"""
        print("\n=== CADASTRAR NOVO SERVIÇO ===\n")
        
        try:
            nome = input("Nome do serviço: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                return
            
            # Verificar se já existe serviço com esse nome
            if self.db.buscar_um("servicos", {"nome": nome}):
                print(f"\n⚠️  Já existe um serviço com o nome '{nome}'!")
                continuar = input("Deseja cadastrar mesmo assim? (S/N): ").strip().upper()
                if continuar != 'S':
                    return
            
            descricao = input("Descrição (opcional): ").strip() or None
            
            preco = input("Preço (R$): ").strip()
            try:
                preco = float(preco.replace(',', '.'))
                if preco <= 0:
                    print("❌ Preço deve ser maior que zero!")
                    return
            except ValueError:
                print("❌ Preço inválido!")
                return
            
            duracao = input("Duração estimada (em minutos): ").strip()
            try:
                duracao = int(duracao)
                if duracao <= 0:
                    print("❌ Duração deve ser maior que zero!")
                    return
            except ValueError:
                print("❌ Duração inválida!")
                return
            
            # Criar documento
            servico = {
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "duracao_estimada": duracao,
                "ativo": True,
                "stats": {
                    "total_realizados": 0,
                    "faturamento_total": 0.0
                }
            }
            
            servico_id = self.db.inserir("servicos", servico)
            
            if servico_id:
                preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"\n✅ Serviço '{nome}' cadastrado com sucesso!")
                print(f"   ID: {servico_id}")
                print(f"   Preço: {preco_fmt}")
                print(f"   Duração: {duracao} minutos")
            else:
                print("\n❌ Erro ao cadastrar serviço!")
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar serviço: {e}")
    
    def listar_servicos(self):
        """Lista todos os serviços cadastrados"""
        print("\n=== LISTA DE SERVIÇOS ===\n")
        
        from pymongo import ASCENDING
        
        servicos = self.db.buscar_todos(
            "servicos",
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not servicos:
            print("⚠️  Nenhum serviço cadastrado.")
            return
        
        print(f"{'Nome':<35} {'Preço':<12} {'Duração':<12} {'Status':<10}")
        print("-" * 69)
        
        for servico in servicos:
            nome = servico['nome'][:33]
            preco = servico['preco']
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            duracao = servico['duracao_estimada']
            duracao_fmt = f"{duracao} min"
            ativo = servico.get('ativo', True)
            status = "Ativo" if ativo else "Inativo"
            
            print(f"{nome:<35} {preco_fmt:<12} {duracao_fmt:<12} {status:<10}")
        
        print(f"\nTotal: {len(servicos)} serviço(s)")
    
    def buscar_servico(self):
        """Busca um serviço por Nome"""
        print("\n=== BUSCAR SERVIÇO ===\n")
        print("[1] Buscar por Nome")
        print("[2] Listar apenas Ativos")
        print("[0] Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            nome = input("\nDigite o nome (ou parte dele): ").strip()
            
            if not nome:
                print("❌ Digite um nome para buscar!")
                return
            
            from pymongo import ASCENDING
            
            servicos = self.db.buscar_todos(
                "servicos",
                {"nome": {"$regex": nome, "$options": "i"}},
                ordenacao=[("nome", ASCENDING)]
            )
            
            if not servicos:
                print(f"\n⚠️  Nenhum serviço encontrado com '{nome}'")
                return
            
            print(f"\n✅ Encontrado(s) {len(servicos)} serviço(s):\n")
            
            for servico in servicos:
                self._exibir_servico_detalhado(servico)
        
        elif opcao == "2":
            from pymongo import ASCENDING
            
            servicos = self.db.buscar_todos(
                "servicos",
                {"ativo": True},
                ordenacao=[("nome", ASCENDING)]
            )
            
            if not servicos:
                print("\n⚠️  Nenhum serviço ativo encontrado.")
                return
            
            print(f"\n✅ {len(servicos)} serviço(s) ativo(s):\n")
            
            for servico in servicos:
                self._exibir_servico_detalhado(servico)
        
        elif opcao == "0":
            return
        else:
            print("\n❌ Opção inválida!")
    
    def _exibir_servico_detalhado(self, servico):
        """Exibe dados completos do serviço"""
        preco = servico['preco']
        preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        
        print("\n" + "="*70)
        print(f"ID: {servico['_id']}")
        print(f"Nome: {servico['nome']}")
        print(f"Descrição: {servico.get('descricao', '-')}")
        print(f"Preço: {preco_fmt}")
        print(f"Duração: {servico['duracao_estimada']} minutos")
        print(f"Status: {'Ativo' if servico.get('ativo', True) else 'Inativo'}")
        
        stats = servico.get('stats', {})
        if stats.get('total_realizados', 0) > 0:
            faturamento = stats.get('faturamento_total', 0.0)
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"\n📊 Estatísticas:")
            print(f"   Total realizado: {stats.get('total_realizados', 0)} vez(es)")
            print(f"   Faturamento: {faturamento_fmt}")
        
        print("="*70)
    
    def atualizar_servico(self):
        """Atualiza dados de um serviço"""
        print("\n=== ATUALIZAR SERVIÇO ===\n")
        
        nome_busca = input("Nome do serviço (ou parte dele): ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        # Buscar serviços com esse nome
        from pymongo import ASCENDING
        
        servicos = self.db.buscar_todos(
            "servicos",
            {"nome": {"$regex": nome_busca, "$options": "i"}},
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not servicos:
            print(f"\n⚠️  Nenhum serviço encontrado com '{nome_busca}'")
            return
        
        if len(servicos) > 1:
            print(f"\n✅ Encontrados {len(servicos)} serviços:\n")
            for i, s in enumerate(servicos, 1):
                preco_fmt = f"R$ {s['preco']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"[{i}] {s['nome']} - {preco_fmt}")
            
            escolha = input("\nEscolha o número do serviço: ").strip()
            try:
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(servicos):
                    print("❌ Opção inválida!")
                    return
                servico = servicos[idx]
            except ValueError:
                print("❌ Opção inválida!")
                return
        else:
            servico = servicos[0]
        
        print(f"\nServiço: {servico['nome']}")
        print("\n💡 Deixe em branco para manter o valor atual\n")
        
        nome = input(f"Nome [{servico['nome']}]: ").strip()
        
        descricao = input(f"Descrição [{servico.get('descricao', '-')}]: ").strip()
        
        preco_input = input(f"Preço (R$) [{servico['preco']}]: ").strip()
        preco = None
        if preco_input:
            try:
                preco = float(preco_input.replace(',', '.'))
                if preco <= 0:
                    print("⚠️  Preço inválido! Mantendo valor atual.")
                    preco = None
            except ValueError:
                print("⚠️  Preço inválido! Mantendo valor atual.")
                preco = None
        
        duracao_input = input(f"Duração (min) [{servico['duracao_estimada']}]: ").strip()
        duracao = None
        if duracao_input:
            try:
                duracao = int(duracao_input)
                if duracao <= 0:
                    print("⚠️  Duração inválida! Mantendo valor atual.")
                    duracao = None
            except ValueError:
                print("⚠️  Duração inválida! Mantendo valor atual.")
                duracao = None
        
        # Montar atualização
        atualizacao = {}
        
        if nome:
            atualizacao['nome'] = nome
        if descricao:
            atualizacao['descricao'] = descricao
        if preco is not None:
            atualizacao['preco'] = preco
        if duracao is not None:
            atualizacao['duracao_estimada'] = duracao
        
        if not atualizacao:
            print("\n⚠️  Nenhuma alteração informada.")
            return
        
        # Confirmar
        print("\n📝 Dados que serão atualizados:")
        for campo, valor in atualizacao.items():
            if campo == 'preco':
                valor = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"   • {campo}: {valor}")
        
        confirma = input("\nConfirmar atualização? (S/N): ").strip().upper()
        
        if confirma != 'S':
            print("❌ Atualização cancelada.")
            return
        
        if self.db.atualizar("servicos", {"_id": servico['_id']}, atualizacao):
            print("\n✅ Serviço atualizado com sucesso!")
        else:
            print("\n❌ Erro ao atualizar serviço!")
    
    def ativar_desativar_servico(self):
        """Ativa ou desativa um serviço"""
        print("\n=== ATIVAR/DESATIVAR SERVIÇO ===\n")
        
        nome_busca = input("Nome do serviço: ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        servico = self.db.buscar_um("servicos", {"nome": {"$regex": f"^{nome_busca}$", "$options": "i"}})
        
        if not servico:
            print(f"\n⚠️  Serviço '{nome_busca}' não encontrado!")
            return
        
        nome = servico['nome']
        ativo = servico.get('ativo', True)
        status_atual = "Ativo" if ativo else "Inativo"
        novo_status = not ativo
        acao = "desativar" if ativo else "ativar"
        
        confirmacao = input(f"\nServiço '{nome}' está {status_atual}. Deseja {acao}? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("❌ Operação cancelada.")
            return
        
        if self.db.atualizar("servicos", {"_id": servico['_id']}, {"ativo": novo_status}):
            print(f"\n✅ Serviço '{nome}' {'ativado' if novo_status else 'desativado'} com sucesso!")
        else:
            print("\n❌ Erro ao atualizar status!")
    
    def deletar_servico(self):
        """Remove um serviço do sistema"""
        print("\n=== REMOVER SERVIÇO ===\n")
        
        nome_busca = input("Nome do serviço: ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        servico = self.db.buscar_um("servicos", {"nome": {"$regex": f"^{nome_busca}$", "$options": "i"}})
        
        if not servico:
            print(f"\n⚠️  Serviço '{nome_busca}' não encontrado!")
            return
        
        nome = servico['nome']
        
        # Verificar se tem atendimentos com esse serviço
        atendimento = self.db.buscar_um("atendimentos", {"servicos.servico_id": servico['_id']})
        
        if atendimento:
            print(f"\n❌ NÃO É POSSÍVEL DELETAR!")
            print(f"   O serviço '{nome}' já foi usado em atendimentos.")
            print("   Por questões de integridade, não pode ser removido.")
            print("\n💡 Dica: Use a opção 'Desativar' para parar de oferecer este serviço.")
            return
        
        print(f"\n⚠️  ATENÇÃO: Remover o serviço '{nome}' é irreversível!")
        confirmacao = input("Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao != 'CONFIRMAR':
            print("❌ Operação cancelada.")
            return
        
        if self.db.deletar("servicos", {"_id": servico['_id']}):
            print(f"\n✅ Serviço '{nome}' removido com sucesso!")
        else:
            print("\n❌ Erro ao deletar serviço!")
    
    def listar_servicos_mais_solicitados(self):
        """Relatório: Serviços mais solicitados"""
        print("\n=== SERVIÇOS MAIS SOLICITADOS ===\n")
        
        # Agregação MongoDB para contar serviços nos atendimentos
        pipeline = [
            {
                "$match": {"status": "finalizado"}
            },
            {
                "$unwind": "$servicos"
            },
            {
                "$group": {
                    "_id": "$servicos.nome",
                    "total_realizados": {"$sum": 1},
                    "faturamento": {"$sum": "$servicos.preco_cobrado"}
                }
            },
            {
                "$sort": {"total_realizados": -1}
            },
            {
                "$limit": 10
            }
        ]
        
        resultados = self.db.agregacao("atendimentos", pipeline)
        
        if not resultados:
            print("⚠️  Nenhum serviço foi realizado ainda.")
            return
        
        print(f"{'Serviço':<35} {'Realizados':<12} {'Faturamento':<15}")
        print("-" * 62)
        
        total_geral = 0
        
        for resultado in resultados:
            nome = resultado['_id'][:33]
            total = resultado['total_realizados']
            faturamento = resultado['faturamento']
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"{nome:<35} {total:<12} {faturamento_fmt:<15}")
            total_geral += faturamento
        
        total_fmt = f"R$ {total_geral:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 62)
        print(f"\nTotal de serviços listados: {len(resultados)}")
        print(f"Faturamento total: {total_fmt}")


def menu_servicos(db: DatabaseMongo):
    """Menu de gerenciamento de serviços"""
    crud = CRUDServico(db)
    
    while True:
        print("\n" + "="*60)
        print("          GERENCIAR SERVIÇOS")
        print("="*60)
        print("\n[1] Cadastrar Serviço")
        print("[2] Listar Todos os Serviços")
        print("[3] Buscar Serviço")
        print("[4] Atualizar Serviço")
        print("[5] Ativar/Desativar Serviço")
        print("[6] Remover Serviço")
        print("[7] Relatório: Serviços Mais Solicitados")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
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
            print("\n❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")