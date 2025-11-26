from database import Database

class CRUDProduto:
    def __init__(self, db: Database):
        self.db = db
    
    def criar_produto(self):
        """Cadastra um novo produto"""
        print("\n=== CADASTRAR NOVO PRODUTO ===\n")
        
        try:
            nome = input("Nome do produto: ").strip()
            if not nome:
                print("Nome é obrigatório!")
                return
            
            descricao = input("Descrição (opcional): ").strip()
            if not descricao:
                descricao = None
            
            preco = input("Preço de venda (R$): ").strip()
            try:
                preco = float(preco.replace(',', '.'))
                if preco <= 0:
                    print("Preço deve ser maior que zero!")
                    return
            except ValueError:
                print("Preço inválido!")
                return
            
            estoque_atual = input("Estoque atual (quantidade): ").strip()
            try:
                estoque_atual = int(estoque_atual)
                if estoque_atual < 0:
                    print("Estoque não pode ser negativo!")
                    return
            except ValueError:
                print("Quantidade inválida!")
                return
            
            estoque_minimo = input("Estoque mínimo (padrão=5): ").strip()
            if estoque_minimo:
                try:
                    estoque_minimo = int(estoque_minimo)
                    if estoque_minimo < 0:
                        print("Estoque mínimo inválido, usando padrão (5).")
                        estoque_minimo = 5
                except ValueError:
                    print("Estoque mínimo inválido, usando padrão (5).")
                    estoque_minimo = 5
            else:
                estoque_minimo = 5
            
            query = """
                INSERT INTO produto (nome, descricao, preco_venda, estoque_atual, estoque_minimo)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (nome, descricao, preco, estoque_atual, estoque_minimo)
            
            if self.db.executar_comando(query, params):
                print(f"\n✓ Produto '{nome}' cadastrado com sucesso!")
                
                if estoque_atual <= estoque_minimo:
                    print(f"ATENÇÃO: Estoque está baixo ou no limite!")
            
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")
    
    def listar_produtos(self):
        """Lista todos os produtos cadastrados"""
        print("\n=== LISTA DE PRODUTOS ===\n")
        
        query = """
            SELECT id_produto, nome, preco_venda, estoque_atual, estoque_minimo, ativo 
            FROM produto 
            ORDER BY nome
        """
        produtos = self.db.executar_query(query)
        
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
        
        print(f"{'ID':<5} {'Nome':<30} {'Preço':<12} {'Estoque':<10} {'Mín.':<8} {'Status':<10}")
        print("-" * 75)
        
        for produto in produtos:
            id_p, nome, preco, estoque, minimo, ativo = produto
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            status = "Ativo" if ativo else "Inativo"
            
            alerta = ""
            if estoque <= 0:
                alerta = "SEM ESTOQUE"
            elif estoque <= minimo:
                alerta = "BAIXO"
            
            print(f"{id_p:<5} {nome:<30} {preco_fmt:<12} {estoque:<10} {minimo:<8} {status:<10}{alerta}")
        
        print(f"\nTotal: {len(produtos)} produto(s)")
    
    def buscar_produto(self):
        """Busca um produto por ID ou Nome"""
        print("\n=== BUSCAR PRODUTO ===\n")
        print("[1] Buscar por ID")
        print("[2] Buscar por Nome")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            id_produto = input("Digite o ID: ").strip()
            if not id_produto.isdigit():
                print("ID inválido!")
                return
            query = "SELECT * FROM produto WHERE id_produto = %s"
            params = (id_produto,)
        
        elif opcao == "2":
            nome = input("Digite o nome (ou parte dele): ").strip()
            query = "SELECT * FROM produto WHERE nome ILIKE %s"
            params = (f"%{nome}%",)
        
        else:
            print("Opção inválida!")
            return
        
        produtos = self.db.executar_query(query, params)
        
        if not produtos:
            print("\nProduto não encontrado.")
            return
        
        print("\n" + "="*70)
        for produto in produtos:
            id_p, nome, descricao, preco, estoque, minimo, ativo = produto
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"ID: {id_p}")
            print(f"Nome: {nome}")
            print(f"Descrição: {descricao if descricao else '-'}")
            print(f"Preço: {preco_fmt}")
            print(f"Estoque Atual: {estoque}")
            print(f"Estoque Mínimo: {minimo}")
            print(f"Status: {'Ativo' if ativo else 'Inativo'}")
            
            if estoque <= 0:
                print("ATENÇÃO: PRODUTO SEM ESTOQUE!")
            elif estoque <= minimo:
                print("ATENÇÃO: ESTOQUE BAIXO!")
            
            print("="*70)
    
    def atualizar_produto(self):
        """Atualiza dados de um produto"""
        print("\n=== ATUALIZAR PRODUTO ===\n")
        
        id_produto = input("Digite o ID do produto: ").strip()
        if not id_produto.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT * FROM produto WHERE id_produto = %s"
        produto = self.db.executar_query(query, (id_produto,))
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        produto = produto[0]
        id_p, nome_atual, desc_atual, preco_atual, estoque_atual, minimo_atual, ativo_atual = produto
        
        print(f"\nProduto: {nome_atual}")
        print("\nDeixe em branco para manter o valor atual.\n")
        
        nome = input(f"Nome [{nome_atual}]: ").strip()
        if not nome:
            nome = nome_atual
        
        descricao = input(f"Descrição [{desc_atual if desc_atual else '-'}]: ").strip()
        if not descricao:
            descricao = desc_atual
        
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
        
        minimo_input = input(f"Estoque Mínimo [{minimo_atual}]: ").strip()
        if minimo_input:
            try:
                minimo = int(minimo_input)
                if minimo < 0:
                    print("Estoque mínimo inválido! Mantendo valor atual.")
                    minimo = minimo_atual
            except ValueError:
                print("Estoque mínimo inválido! Mantendo valor atual.")
                minimo = minimo_atual
        else:
            minimo = minimo_atual
        
        query = """
            UPDATE produto 
            SET nome = %s, descricao = %s, preco_venda = %s, estoque_minimo = %s
            WHERE id_produto = %s
        """
        params = (nome, descricao, preco, minimo, id_produto)
        
        if self.db.executar_comando(query, params):
            print(f"\n✓ Produto atualizado com sucesso!")
    
    def atualizar_estoque(self):
        """Atualiza o estoque de um produto"""
        print("\n=== ATUALIZAR ESTOQUE ===\n")
        
        id_produto = input("Digite o ID do produto: ").strip()
        if not id_produto.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome, estoque_atual, estoque_minimo FROM produto WHERE id_produto = %s"
        produto = self.db.executar_query(query, (id_produto,))
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        nome, estoque_atual, estoque_minimo = produto[0]
        
        print(f"\nProduto: {nome}")
        print(f"Estoque atual: {estoque_atual}")
        print(f"Estoque mínimo: {estoque_minimo}")
        
        print("\n[1] Adicionar ao estoque (entrada)")
        print("[2] Remover do estoque (saída)")
        print("[3] Definir novo valor")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            quantidade = input("\nQuantidade a adicionar: ").strip()
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero!")
                    return
                
                novo_estoque = estoque_atual + quantidade
                query = "UPDATE produto SET estoque_atual = %s WHERE id_produto = %s"
                
                if self.db.executar_comando(query, (novo_estoque, id_produto)):
                    print(f"\n✓ Estoque atualizado!")
                    print(f"  Anterior: {estoque_atual}")
                    print(f"  Adicionado: +{quantidade}")
                    print(f"  Novo: {novo_estoque}")
            
            except ValueError:
                print("Quantidade inválida!")
        
        elif opcao == "2":
            quantidade = input("\nQuantidade a remover: ").strip()
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    print("Quantidade deve ser maior que zero!")
                    return
                
                if quantidade > estoque_atual:
                    print(f"Quantidade maior que o estoque disponível ({estoque_atual})!")
                    return
                
                novo_estoque = estoque_atual - quantidade
                query = "UPDATE produto SET estoque_atual = %s WHERE id_produto = %s"
                
                if self.db.executar_comando(query, (novo_estoque, id_produto)):
                    print(f"\n✓ Estoque atualizado!")
                    print(f"  Anterior: {estoque_atual}")
                    print(f"  Removido: -{quantidade}")
                    print(f"  Novo: {novo_estoque}")
                    
                    if novo_estoque <= estoque_minimo:
                        print(f"\nATENÇÃO: Estoque está baixo ou no limite!")
            
            except ValueError:
                print("Quantidade inválida!")
        
        elif opcao == "3":
            novo_estoque = input("\nNovo valor do estoque: ").strip()
            try:
                novo_estoque = int(novo_estoque)
                if novo_estoque < 0:
                    print("Estoque não pode ser negativo!")
                    return
                
                query = "UPDATE produto SET estoque_atual = %s WHERE id_produto = %s"
                
                if self.db.executar_comando(query, (novo_estoque, id_produto)):
                    diferenca = novo_estoque - estoque_atual
                    sinal = "+" if diferenca > 0 else ""
                    
                    print(f"\n✓ Estoque atualizado!")
                    print(f"  Anterior: {estoque_atual}")
                    print(f"  Diferença: {sinal}{diferenca}")
                    print(f"  Novo: {novo_estoque}")
                    
                    if novo_estoque <= estoque_minimo:
                        print(f"\nATENÇÃO: Estoque está baixo ou no limite!")
            
            except ValueError:
                print("Valor inválido!")
        
        else:
            print("Opção inválida!")
    
    def ativar_desativar_produto(self):
        """Ativa ou desativa um produto"""
        print("\n=== ATIVAR/DESATIVAR PRODUTO ===\n")
        
        id_produto = input("Digite o ID do produto: ").strip()
        if not id_produto.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome, ativo FROM produto WHERE id_produto = %s"
        produto = self.db.executar_query(query, (id_produto,))
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        nome, ativo = produto[0]
        status_atual = "Ativo" if ativo else "Inativo"
        novo_status = not ativo
        acao = "desativar" if ativo else "ativar"
        
        confirmacao = input(f"\nProduto '{nome}' está {status_atual}. Deseja {acao}? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("Operação cancelada.")
            return
        
        query = "UPDATE produto SET ativo = %s WHERE id_produto = %s"
        
        if self.db.executar_comando(query, (novo_status, id_produto)):
            print(f"\n✓ Produto '{nome}' {'ativado' if novo_status else 'desativado'} com sucesso!")
    
    def deletar_produto(self):
        """Remove um produto do sistema"""
        print("\n=== REMOVER PRODUTO ===\n")
        
        id_produto = input("Digite o ID do produto: ").strip()
        if not id_produto.isdigit():
            print("ID inválido!")
            return
        
        query = "SELECT nome FROM produto WHERE id_produto = %s"
        produto = self.db.executar_query(query, (id_produto,))
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        nome = produto[0][0]
        
        print(f"\nATENÇÃO: Remover o produto '{nome}' pode afetar vendas registradas!")
        confirmacao = input("Tem certeza? Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao != 'CONFIRMAR':
            print("Operação cancelada.")
            return
        
        query = "DELETE FROM produto WHERE id_produto = %s"
        
        if self.db.executar_comando(query, (id_produto,)):
            print(f"\n✓ Produto '{nome}' removido com sucesso!")
    
    def produtos_estoque_baixo(self):
        """Lista produtos com estoque baixo"""
        print("\n=== PRODUTOS COM ESTOQUE BAIXO ===\n")
        
        query = """
            SELECT id_produto, nome, estoque_atual, estoque_minimo, preco_venda
            FROM produto 
            WHERE ativo = TRUE 
                AND estoque_atual <= estoque_minimo
            ORDER BY estoque_atual ASC
        """
        
        produtos = self.db.executar_query(query)
        
        if not produtos:
            print("✓ Nenhum produto com estoque baixo!")
            return
        
        print(f"{'ID':<5} {'Nome':<30} {'Estoque':<10} {'Mínimo':<10} {'Preço':<12}")
        print("-" * 67)
        
        for produto in produtos:
            id_p, nome, estoque, minimo, preco = produto
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            alerta = "⚠️ SEM ESTOQUE" if estoque == 0 else "⚠️ BAIXO"
            print(f"{id_p:<5} {nome:<30} {estoque:<10} {minimo:<10} {preco_fmt:<12} {alerta}")
        
        print(f"\nTotal: {len(produtos)} produto(s) com estoque baixo")
        print("Recomendação: Realizar reposição o quanto antes!")


def menu_produtos(db: Database):
    """Menu de gerenciamento de produtos"""
    crud = CRUDProduto(db)
    
    while True:
        print("\n" + "="*50)
        print("           GERENCIAR PRODUTOS")
        print("="*50)
        print("[1] Cadastrar Produto")
        print("[2] Listar Todos os Produtos")
        print("[3] Buscar Produto")
        print("[4] Atualizar Produto")
        print("[5] Atualizar Estoque")
        print("[6] Ativar/Desativar Produto")
        print("[7] Remover Produto")
        print("[8] Produtos com Estoque Baixo")
        print("[0] Voltar ao Menu Principal")
        print("-"*50)
        
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
            print("\nOpção inválida!")
        
        input("\nPressione ENTER para continuar...")