import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from bson import ObjectId

class CRUDProduto:
    def __init__(self, db: DatabaseMongo):
        self.db = db
    
    def criar_produto(self):
        """Cadastra um novo produto"""
        print("\n=== CADASTRAR NOVO PRODUTO ===\n")
        
        try:
            nome = input("Nome do produto: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                return
            
            # Verificar se já existe produto com esse nome
            if self.db.buscar_um("produtos", {"nome": nome}):
                print(f"\n⚠️  Já existe um produto com o nome '{nome}'!")
                continuar = input("Deseja cadastrar mesmo assim? (S/N): ").strip().upper()
                if continuar != 'S':
                    return
            
            descricao = input("Descrição (opcional): ").strip() or None
            
            preco = input("Preço de venda (R$): ").strip()
            try:
                preco = float(preco.replace(',', '.'))
                if preco <= 0:
                    print("❌ Preço deve ser maior que zero!")
                    return
            except ValueError:
                print("❌ Preço inválido!")
                return
            
            estoque_atual = input("Estoque atual (quantidade): ").strip()
            try:
                estoque_atual = int(estoque_atual)
                if estoque_atual < 0:
                    print("❌ Estoque não pode ser negativo!")
                    return
            except ValueError:
                print("❌ Quantidade inválida!")
                return
            
            estoque_minimo = input("Estoque mínimo [padrão=5]: ").strip()
            if estoque_minimo:
                try:
                    estoque_minimo = int(estoque_minimo)
                    if estoque_minimo < 0:
                        print("⚠️  Estoque mínimo inválido, usando padrão (5).")
                        estoque_minimo = 5
                except ValueError:
                    print("⚠️  Estoque mínimo inválido, usando padrão (5).")
                    estoque_minimo = 5
            else:
                estoque_minimo = 5
            
            # Criar documento
            produto = {
                "nome": nome,
                "descricao": descricao,
                "preco_venda": preco,
                "estoque_atual": estoque_atual,
                "estoque_minimo": estoque_minimo,
                "ativo": True,
                "stats": {
                    "total_vendido": 0,
                    "faturamento_total": 0.0
                }
            }
            
            produto_id = self.db.inserir("produtos", produto)
            
            if produto_id:
                preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"\n✅ Produto '{nome}' cadastrado com sucesso!")
                print(f"   ID: {produto_id}")
                print(f"   Preço: {preco_fmt}")
                print(f"   Estoque: {estoque_atual}")
                
                if estoque_atual <= estoque_minimo:
                    print(f"\n⚠️  ATENÇÃO: Estoque está baixo ou no limite!")
            else:
                print("\n❌ Erro ao cadastrar produto!")
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar produto: {e}")
    
    def listar_produtos(self):
        """Lista todos os produtos cadastrados"""
        print("\n=== LISTA DE PRODUTOS ===\n")
        
        from pymongo import ASCENDING
        
        produtos = self.db.buscar_todos(
            "produtos",
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not produtos:
            print("⚠️  Nenhum produto cadastrado.")
            return
        
        print(f"{'Nome':<30} {'Preço':<12} {'Estoque':<10} {'Mín.':<8} {'Status':<10} {'Alerta':<15}")
        print("-" * 85)
        
        for produto in produtos:
            nome = produto['nome'][:28]
            preco = produto['preco_venda']
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            estoque = produto['estoque_atual']
            minimo = produto['estoque_minimo']
            ativo = produto.get('ativo', True)
            status = "Ativo" if ativo else "Inativo"
            
            alerta = ""
            if estoque <= 0:
                alerta = "⚠️ SEM ESTOQUE"
            elif estoque <= minimo:
                alerta = "⚠️ BAIXO"
            
            print(f"{nome:<30} {preco_fmt:<12} {estoque:<10} {minimo:<8} {status:<10} {alerta:<15}")
        
        print(f"\nTotal: {len(produtos)} produto(s)")
    
    def buscar_produto(self):
        """Busca um produto por Nome"""
        print("\n=== BUSCAR PRODUTO ===\n")
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
            
            produtos = self.db.buscar_todos(
                "produtos",
                {"nome": {"$regex": nome, "$options": "i"}},
                ordenacao=[("nome", ASCENDING)]
            )
            
            if not produtos:
                print(f"\n⚠️  Nenhum produto encontrado com '{nome}'")
                return
            
            print(f"\n✅ Encontrado(s) {len(produtos)} produto(s):\n")
            
            for produto in produtos:
                self._exibir_produto_detalhado(produto)
        
        elif opcao == "2":
            from pymongo import ASCENDING
            
            produtos = self.db.buscar_todos(
                "produtos",
                {"ativo": True},
                ordenacao=[("nome", ASCENDING)]
            )
            
            if not produtos:
                print("\n⚠️  Nenhum produto ativo encontrado.")
                return
            
            print(f"\n✅ {len(produtos)} produto(s) ativo(s):\n")
            
            for produto in produtos:
                self._exibir_produto_detalhado(produto)
        
        elif opcao == "0":
            return
        else:
            print("\n❌ Opção inválida!")
    
    def _exibir_produto_detalhado(self, produto):
        """Exibe dados completos do produto"""
        preco = produto['preco_venda']
        preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        estoque = produto['estoque_atual']
        minimo = produto['estoque_minimo']
        
        print("\n" + "="*70)
        print(f"ID: {produto['_id']}")
        print(f"Nome: {produto['nome']}")
        print(f"Descrição: {produto.get('descricao', '-')}")
        print(f"Preço: {preco_fmt}")
        print(f"Estoque Atual: {estoque}")
        print(f"Estoque Mínimo: {minimo}")
        print(f"Status: {'Ativo' if produto.get('ativo', True) else 'Inativo'}")
        
        if estoque <= 0:
            print("\n⚠️  ATENÇÃO: PRODUTO SEM ESTOQUE!")
        elif estoque <= minimo:
            print("\n⚠️  ATENÇÃO: ESTOQUE BAIXO!")
        
        stats = produto.get('stats', {})
        if stats.get('total_vendido', 0) > 0:
            faturamento = stats.get('faturamento_total', 0.0)
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"\n📊 Estatísticas:")
            print(f"   Total vendido: {stats.get('total_vendido', 0)} unidade(s)")
            print(f"   Faturamento: {faturamento_fmt}")
        
        print("="*70)
    
    def atualizar_produto(self):
        """Atualiza dados de um produto"""
        print("\n=== ATUALIZAR PRODUTO ===\n")
        
        nome_busca = input("Nome do produto (ou parte dele): ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        # Buscar produtos com esse nome
        from pymongo import ASCENDING
        
        produtos = self.db.buscar_todos(
            "produtos",
            {"nome": {"$regex": nome_busca, "$options": "i"}},
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not produtos:
            print(f"\n⚠️  Nenhum produto encontrado com '{nome_busca}'")
            return
        
        if len(produtos) > 1:
            print(f"\n✅ Encontrados {len(produtos)} produtos:\n")
            for i, p in enumerate(produtos, 1):
                preco_fmt = f"R$ {p['preco_venda']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                print(f"[{i}] {p['nome']} - {preco_fmt} (Estoque: {p['estoque_atual']})")
            
            escolha = input("\nEscolha o número do produto: ").strip()
            try:
                idx = int(escolha) - 1
                if idx < 0 or idx >= len(produtos):
                    print("❌ Opção inválida!")
                    return
                produto = produtos[idx]
            except ValueError:
                print("❌ Opção inválida!")
                return
        else:
            produto = produtos[0]
        
        print(f"\nProduto: {produto['nome']}")
        print("\n💡 Deixe em branco para manter o valor atual\n")
        
        nome = input(f"Nome [{produto['nome']}]: ").strip()
        descricao = input(f"Descrição [{produto.get('descricao', '-')}]: ").strip()
        
        preco_input = input(f"Preço (R$) [{produto['preco_venda']}]: ").strip()
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
        
        minimo_input = input(f"Estoque Mínimo [{produto['estoque_minimo']}]: ").strip()
        minimo = None
        if minimo_input:
            try:
                minimo = int(minimo_input)
                if minimo < 0:
                    print("⚠️  Estoque mínimo inválido! Mantendo valor atual.")
                    minimo = None
            except ValueError:
                print("⚠️  Estoque mínimo inválido! Mantendo valor atual.")
                minimo = None
        
        # Montar atualização
        atualizacao = {}
        
        if nome:
            atualizacao['nome'] = nome
        if descricao:
            atualizacao['descricao'] = descricao
        if preco is not None:
            atualizacao['preco_venda'] = preco
        if minimo is not None:
            atualizacao['estoque_minimo'] = minimo
        
        if not atualizacao:
            print("\n⚠️  Nenhuma alteração informada.")
            return
        
        # Confirmar
        print("\n📝 Dados que serão atualizados:")
        for campo, valor in atualizacao.items():
            if campo == 'preco_venda':
                valor = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            print(f"   • {campo}: {valor}")
        
        confirma = input("\nConfirmar atualização? (S/N): ").strip().upper()
        
        if confirma != 'S':
            print("❌ Atualização cancelada.")
            return
        
        if self.db.atualizar("produtos", {"_id": produto['_id']}, atualizacao):
            print("\n✅ Produto atualizado com sucesso!")
        else:
            print("\n❌ Erro ao atualizar produto!")
    
    def atualizar_estoque(self):
        """Atualiza o estoque de um produto"""
        print("\n=== ATUALIZAR ESTOQUE ===\n")
        
        nome_busca = input("Nome do produto: ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        produto = self.db.buscar_um("produtos", {"nome": {"$regex": f"^{nome_busca}$", "$options": "i"}})
        
        if not produto:
            # Tentar busca parcial
            from pymongo import ASCENDING
            produtos = self.db.buscar_todos(
                "produtos",
                {"nome": {"$regex": nome_busca, "$options": "i"}},
                ordenacao=[("nome", ASCENDING)],
                limite=5
            )
            
            if not produtos:
                print(f"\n⚠️  Produto '{nome_busca}' não encontrado!")
                return
            
            if len(produtos) > 1:
                print(f"\n✅ Encontrados {len(produtos)} produtos:\n")
                for i, p in enumerate(produtos, 1):
                    print(f"[{i}] {p['nome']} (Estoque: {p['estoque_atual']})")
                
                escolha = input("\nEscolha o número do produto: ").strip()
                try:
                    idx = int(escolha) - 1
                    if idx < 0 or idx >= len(produtos):
                        print("❌ Opção inválida!")
                        return
                    produto = produtos[idx]
                except ValueError:
                    print("❌ Opção inválida!")
                    return
            else:
                produto = produtos[0]
        
        nome = produto['nome']
        estoque_atual = produto['estoque_atual']
        estoque_minimo = produto['estoque_minimo']
        
        print(f"\nProduto: {nome}")
        print(f"Estoque atual: {estoque_atual}")
        print(f"Estoque mínimo: {estoque_minimo}")
        
        print("\n[1] Adicionar ao estoque (entrada)")
        print("[2] Remover do estoque (saída)")
        print("[3] Definir novo valor")
        print("[0] Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            quantidade = input("\nQuantidade a adicionar: ").strip()
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    print("❌ Quantidade deve ser maior que zero!")
                    return
                
                novo_estoque = estoque_atual + quantidade
                
                if self.db.atualizar("produtos", {"_id": produto['_id']}, {"estoque_atual": novo_estoque}):
                    print(f"\n✅ Estoque atualizado!")
                    print(f"  Anterior: {estoque_atual}")
                    print(f"  Adicionado: +{quantidade}")
                    print(f"  Novo: {novo_estoque}")
                else:
                    print("\n❌ Erro ao atualizar estoque!")
            
            except ValueError:
                print("❌ Quantidade inválida!")
        
        elif opcao == "2":
            quantidade = input("\nQuantidade a remover: ").strip()
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    print("❌ Quantidade deve ser maior que zero!")
                    return
                
                if quantidade > estoque_atual:
                    print(f"❌ Quantidade maior que o estoque disponível ({estoque_atual})!")
                    return
                
                novo_estoque = estoque_atual - quantidade
                
                if self.db.atualizar("produtos", {"_id": produto['_id']}, {"estoque_atual": novo_estoque}):
                    print(f"\n✅ Estoque atualizado!")
                    print(f"  Anterior: {estoque_atual}")
                    print(f"  Removido: -{quantidade}")
                    print(f"  Novo: {novo_estoque}")
                    
                    if novo_estoque <= estoque_minimo:
                        print(f"\n⚠️  ATENÇÃO: Estoque está baixo ou no limite!")
                else:
                    print("\n❌ Erro ao atualizar estoque!")
            
            except ValueError:
                print("❌ Quantidade inválida!")
        
        elif opcao == "3":
            novo_estoque = input("\nNovo valor do estoque: ").strip()
            try:
                novo_estoque = int(novo_estoque)
                if novo_estoque < 0:
                    print("❌ Estoque não pode ser negativo!")
                    return
                
                if self.db.atualizar("produtos", {"_id": produto['_id']}, {"estoque_atual": novo_estoque}):
                    diferenca = novo_estoque - estoque_atual
                    sinal = "+" if diferenca > 0 else ""
                    
                    print(f"\n✅ Estoque atualizado!")
                    print(f"  Anterior: {estoque_atual}")
                    print(f"  Diferença: {sinal}{diferenca}")
                    print(f"  Novo: {novo_estoque}")
                    
                    if novo_estoque <= estoque_minimo:
                        print(f"\n⚠️  ATENÇÃO: Estoque está baixo ou no limite!")
                else:
                    print("\n❌ Erro ao atualizar estoque!")
            
            except ValueError:
                print("❌ Valor inválido!")
        
        elif opcao == "0":
            return
        else:
            print("❌ Opção inválida!")
    
    def ativar_desativar_produto(self):
        """Ativa ou desativa um produto"""
        print("\n=== ATIVAR/DESATIVAR PRODUTO ===\n")
        
        nome_busca = input("Nome do produto: ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        produto = self.db.buscar_um("produtos", {"nome": {"$regex": f"^{nome_busca}$", "$options": "i"}})
        
        if not produto:
            print(f"\n⚠️  Produto '{nome_busca}' não encontrado!")
            return
        
        nome = produto['nome']
        ativo = produto.get('ativo', True)
        status_atual = "Ativo" if ativo else "Inativo"
        novo_status = not ativo
        acao = "desativar" if ativo else "ativar"
        
        confirmacao = input(f"\nProduto '{nome}' está {status_atual}. Deseja {acao}? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("❌ Operação cancelada.")
            return
        
        if self.db.atualizar("produtos", {"_id": produto['_id']}, {"ativo": novo_status}):
            print(f"\n✅ Produto '{nome}' {'ativado' if novo_status else 'desativado'} com sucesso!")
        else:
            print("\n❌ Erro ao atualizar status!")
    
    def deletar_produto(self):
        """Remove um produto do sistema"""
        print("\n=== REMOVER PRODUTO ===\n")
        
        nome_busca = input("Nome do produto: ").strip()
        
        if not nome_busca:
            print("❌ Nome é obrigatório!")
            return
        
        produto = self.db.buscar_um("produtos", {"nome": {"$regex": f"^{nome_busca}$", "$options": "i"}})
        
        if not produto:
            print(f"\n⚠️  Produto '{nome_busca}' não encontrado!")
            return
        
        nome = produto['nome']
        
        # Verificar se tem vendas com esse produto
        venda = self.db.buscar_um("atendimentos", {"produtos_vendidos.produto_id": produto['_id']})
        
        if venda:
            print(f"\n❌ NÃO É POSSÍVEL DELETAR!")
            print(f"   O produto '{nome}' já foi vendido em atendimentos.")
            print("   Por questões de integridade, não pode ser removido.")
            print("\n💡 Dica: Use a opção 'Desativar' para parar de oferecer este produto.")
            return
        
        print(f"\n⚠️  ATENÇÃO: Remover o produto '{nome}' é irreversível!")
        confirmacao = input("Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao != 'CONFIRMAR':
            print("❌ Operação cancelada.")
            return
        
        if self.db.deletar("produtos", {"_id": produto['_id']}):
            print(f"\n✅ Produto '{nome}' removido com sucesso!")
        else:
            print("\n❌ Erro ao deletar produto!")
    
    def produtos_estoque_baixo(self):
        """Lista produtos com estoque baixo"""
        print("\n=== PRODUTOS COM ESTOQUE BAIXO ===\n")
        
        # Buscar produtos onde estoque_atual <= estoque_minimo
        from pymongo import ASCENDING
        
        produtos = self.db.buscar_todos(
            "produtos",
            {
                "ativo": True,
                "$expr": {"$lte": ["$estoque_atual", "$estoque_minimo"]}
            },
            ordenacao=[("estoque_atual", ASCENDING)]
        )
        
        if not produtos:
            print("✅ Nenhum produto com estoque baixo!")
            return
        
        print(f"{'Nome':<30} {'Estoque':<10} {'Mínimo':<10} {'Preço':<12} {'Alerta':<15}")
        print("-" * 77)
        
        for produto in produtos:
            nome = produto['nome'][:28]
            estoque = produto['estoque_atual']
            minimo = produto['estoque_minimo']
            preco = produto['preco_venda']
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            alerta = "⚠️ SEM ESTOQUE" if estoque == 0 else "⚠️ BAIXO"
            
            print(f"{nome:<30} {estoque:<10} {minimo:<10} {preco_fmt:<12} {alerta:<15}")
        
        print(f"\nTotal: {len(produtos)} produto(s) com estoque baixo")
        print("💡 Recomendação: Realizar reposição o quanto antes!")


def menu_produtos(db: DatabaseMongo):
    """Menu de gerenciamento de produtos"""
    crud = CRUDProduto(db)
    
    while True:
        print("\n" + "="*60)
        print("          GERENCIAR PRODUTOS")
        print("="*60)
        print("\n[1] Cadastrar Produto")
        print("[2] Listar Todos os Produtos")
        print("[3] Buscar Produto")
        print("[4] Atualizar Produto")
        print("[5] Atualizar Estoque")
        print("[6] Ativar/Desativar Produto")
        print("[7] Remover Produto")
        print("[8] Produtos com Estoque Baixo")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            crud.criar_produto()
        elif opcao == "2":
            crud.listar_produtos()
        elif opcao == "3":
            crud.buscar_produto()
        elif opcao == "4":
            crud.atualizar_produto()
        elif opcao == "5":
            crud.atualizar_estoque()
        elif opcao == "6":
            crud.ativar_desativar_produto()
        elif opcao == "7":
            crud.deletar_produto()
        elif opcao == "8":
            crud.produtos_estoque_baixo()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")