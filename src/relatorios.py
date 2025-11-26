from database import Database
from datetime import datetime

class Relatorios:
    def __init__(self, db: Database):
        self.db = db
    
    def relatorio_atendimentos_periodo(self):
        """Relatório 1: Atendimentos realizados em um período"""
        print("\n=== RELATÓRIO: ATENDIMENTOS POR PERÍODO ===\n")
        
        data_inicio = input("Data início (DD/MM/AAAA): ").strip()
        data_fim = input("Data fim (DD/MM/AAAA): ").strip()
        
        try:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("Formato de data inválido! Use DD/MM/AAAA")
            return
        
        query = """
            SELECT 
                a.id_atendimento,
                COALESCE(a.data_atendimento, a.data_agendada) as data_real,
                c.nome as cliente,
                b.nome as barbeiro,
                a.horario_inicio,
                a.horario_fim,
                a.valor_total,
                a.forma_pagamento,
                a.tipo
            FROM atendimento a
            JOIN cliente c ON a.id_cliente = c.id_cliente
            JOIN barbeiro b ON a.id_barbeiro = b.id_barbeiro
            WHERE COALESCE(a.data_atendimento, a.data_agendada) BETWEEN %s AND %s
                AND a.status = 'finalizado'
            ORDER BY data_real DESC, a.horario_inicio DESC
        """
        
        resultados = self.db.executar_query(query, (data_inicio, data_fim))
        
        if not resultados:
            print("\nNenhum atendimento encontrado neste período.")
            return
        
        print(f"{'ID':<5} {'Data':<12} {'Cliente':<25} {'Barbeiro':<20} {'Início':<8} {'Fim':<8} {'Tipo':<10} {'Valor':<12}")
        print("-" * 110)
        
        total_faturamento = 0
        
        for resultado in resultados:
            id_atend, data, cliente, barbeiro, inicio, fim, valor, forma_pag, tipo = resultado
            data_fmt = datetime.strptime(str(data), "%Y-%m-%d").strftime("%d/%m/%Y")
            valor_fmt = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.') if valor else "R$ 0,00"
            inicio_str = str(inicio)[:5] if inicio else "-"
            fim_str = str(fim)[:5] if fim else "-"
            
            print(f"{id_atend:<5} {data_fmt:<12} {cliente:<25} {barbeiro:<20} {inicio_str:<8} {fim_str:<8} {tipo:<10} {valor_fmt:<12}")
            
            if valor:
                total_faturamento += float(valor)
        
        total_fmt = f"R$ {total_faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 110)
        print(f"\nTotal de atendimentos: {len(resultados)}")
        print(f"Faturamento total: {total_fmt}")
    
    def relatorio_servicos_mais_solicitados(self):
        """Relatório 2: Ranking de serviços mais solicitados"""
        print("\n=== RELATÓRIO: SERVIÇOS MAIS SOLICITADOS ===\n")
        
        query = """
            SELECT 
                s.nome,
                s.preco,
                COUNT(ats.id_atendimento) as total_atendimentos,
                COALESCE(SUM(ats.preco_cobrado), 0) as faturamento_real
            FROM servico s
            LEFT JOIN atendimento_servico ats ON s.id_servico = ats.id_servico
            LEFT JOIN atendimento a ON ats.id_atendimento = a.id_atendimento
                AND a.status = 'finalizado'
            WHERE s.ativo = TRUE
            GROUP BY s.id_servico, s.nome, s.preco
            HAVING COUNT(ats.id_atendimento) > 0
            ORDER BY total_atendimentos DESC, faturamento_real DESC
        """
        
        resultados = self.db.executar_query(query)
        
        if not resultados:
            print("Nenhum serviço foi solicitado ainda.")
            return
        
        print(f"{'Ranking':<8} {'Serviço':<30} {'Atendimentos':<15} {'Preço Padrão':<15} {'Faturamento':<15}")
        print("-" * 83)
        
        ranking = 1
        faturamento_total = 0
        
        for resultado in resultados:
            nome, preco, atendimentos, faturamento = resultado
            preco_fmt = f"R$ {preco:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"{ranking}º{'':<6} {nome:<30} {atendimentos:<15} {preco_fmt:<15} {faturamento_fmt:<15}")
            
            faturamento_total += float(faturamento)
            ranking += 1
        
        total_fmt = f"R$ {faturamento_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 83)
        print(f"\nFaturamento total dos serviços: {total_fmt}")
    
    def relatorio_faturamento_barbeiro(self):
        """Relatório 3: Faturamento por barbeiro em um período"""
        print("\n=== RELATÓRIO: FATURAMENTO POR BARBEIRO ===\n")
        
        data_inicio = input("Data início (DD/MM/AAAA): ").strip()
        data_fim = input("Data fim (DD/MM/AAAA): ").strip()
        
        try:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            print("Formato de data inválido! Use DD/MM/AAAA")
            return
        
        query = """
            SELECT 
                b.nome as barbeiro,
                b.especialidade,
                b.comissao_percentual,
                COUNT(DISTINCT a.id_atendimento) as total_atendimentos,
                COALESCE(SUM(a.valor_total), 0) as faturamento_total,
                COALESCE(SUM(a.valor_total * b.comissao_percentual / 100), 0) as comissao_total
            FROM barbeiro b
            LEFT JOIN atendimento a ON b.id_barbeiro = a.id_barbeiro
                AND COALESCE(a.data_atendimento, a.data_agendada) BETWEEN %s AND %s
                AND a.status = 'finalizado'
            WHERE b.ativo = TRUE
            GROUP BY b.id_barbeiro, b.nome, b.especialidade, b.comissao_percentual
            ORDER BY faturamento_total DESC
        """
        
        resultados = self.db.executar_query(query, (data_inicio, data_fim))
        
        if not resultados:
            print("Nenhum barbeiro ativo encontrado.")
            return
        
        print(f"{'Barbeiro':<30} {'Especialidade':<15} {'Atend.':<8} {'Faturamento':<15} {'Comissão':<12}")
        print("-" * 80)
        
        total_geral = 0
        total_comissoes = 0
        
        for resultado in resultados:
            nome, espec, comissao_pct, atendimentos, faturamento, comissao = resultado
            
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            comissao_fmt = f"R$ {comissao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            espec_fmt = espec if espec else "-"
            
            print(f"{nome:<30} {espec_fmt:<15} {atendimentos:<8} {faturamento_fmt:<15} {comissao_fmt:<12}")
            
            total_geral += float(faturamento)
            total_comissoes += float(comissao)
        
        total_geral_fmt = f"R$ {total_geral:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        total_comissoes_fmt = f"R$ {total_comissoes:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        
        print("-" * 80)
        print(f"\nFaturamento total: {total_geral_fmt}")
        print(f"Total de comissões: {total_comissoes_fmt}")
        print(f"Lucro líquido: R$ {(total_geral - total_comissoes):,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
    
    def relatorio_clientes_frequentes(self):
        """Relatório 4: Clientes mais frequentes"""
        print("\n=== RELATÓRIO: CLIENTES MAIS FREQUENTES ===\n")
        
        query = """
            SELECT 
                c.nome,
                c.telefone,
                COUNT(DISTINCT a.id_atendimento) as total_atendimentos,
                COALESCE(SUM(a.valor_total), 0) as valor_gasto,
                MAX(COALESCE(a.data_atendimento, a.data_agendada)) as ultima_visita,
                COUNT(DISTINCT CASE 
                    WHEN a.status = 'agendado' AND a.data_agendada >= CURRENT_DATE 
                    THEN a.id_atendimento 
                END) as agendamentos_futuros
            FROM cliente c
            LEFT JOIN atendimento a ON c.id_cliente = a.id_cliente
            GROUP BY c.id_cliente, c.nome, c.telefone
            HAVING COUNT(DISTINCT CASE WHEN a.status = 'finalizado' THEN a.id_atendimento END) > 0
            ORDER BY total_atendimentos DESC, valor_gasto DESC
            LIMIT 20
        """
        
        resultados = self.db.executar_query(query)
        
        if not resultados:
            print("Nenhum atendimento registrado ainda.")
            return
        
        print(f"{'#':<4} {'Cliente':<30} {'Telefone':<15} {'Atend.':<8} {'Gasto Total':<15} {'Última Visita':<15}")
        print("-" * 87)
        
        ranking = 1
        
        for resultado in resultados:
            nome, telefone, atendimentos, valor, ultima_visita, agend_futuro = resultado
            
            valor_fmt = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            if ultima_visita:
                ultima_fmt = datetime.strptime(str(ultima_visita), "%Y-%m-%d").strftime("%d/%m/%Y")
            else:
                ultima_fmt = "-"
            
            print(f"{ranking:<4} {nome:<30} {telefone:<15} {atendimentos:<8} {valor_fmt:<15} {ultima_fmt:<15}")
            ranking += 1
        
        print(f"\nTotal de clientes listados: {len(resultados)}")
    
    def relatorio_produtos_mais_vendidos(self):
        """Relatório 5: Produtos mais vendidos"""
        print("\n=== RELATÓRIO: PRODUTOS MAIS VENDIDOS ===\n")
        
        query = """
            SELECT 
                p.nome,
                p.estoque_atual,
                p.estoque_minimo,
                COALESCE(SUM(vp.quantidade), 0) as total_vendido,
                COALESCE(SUM(vp.subtotal), 0) as faturamento,
                p.preco_venda
            FROM produto p
            LEFT JOIN venda_produto vp ON p.id_produto = vp.id_produto
            LEFT JOIN atendimento a ON vp.id_atendimento = a.id_atendimento
                AND a.status = 'finalizado'
            WHERE p.ativo = TRUE
            GROUP BY p.id_produto, p.nome, p.estoque_atual, p.estoque_minimo, p.preco_venda
            HAVING COALESCE(SUM(vp.quantidade), 0) > 0
            ORDER BY total_vendido DESC
        """
        
        resultados = self.db.executar_query(query)
        
        if not resultados:
            print("Nenhuma venda de produto registrada ainda.")
            return
        
        print(f"{'Produto':<30} {'Vendidos':<10} {'Faturamento':<15} {'Estoque':<10} {'Status':<10}")
        print("-" * 75)
        
        faturamento_total = 0
        
        for resultado in resultados:
            nome, estoque, estoque_min, vendidos, faturamento, preco = resultado
            
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            # Verificar status do estoque
            if estoque <= estoque_min:
                status = "BAIXO"
            else:
                status = "OK"
            
            print(f"{nome:<30} {vendidos:<10} {faturamento_fmt:<15} {estoque:<10} {status:<10}")
            
            faturamento_total += float(faturamento)
        
        total_fmt = f"R$ {faturamento_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 75)
        print(f"\nFaturamento total em produtos: {total_fmt}")


def menu_relatorios(db: Database):
    """Menu de relatórios do sistema"""
    relatorios = Relatorios(db)
    
    while True:
        print("\n" + "="*60)
        print("          RELATÓRIOS")
        print("="*60)
        print("\n[1] Atendimentos por Período")
        print("[2] Serviços Mais Solicitados")
        print("[3] Faturamento por Barbeiro")
        print("[4] Clientes Mais Frequentes")
        print("[5] Produtos Mais Vendidos")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            relatorios.relatorio_atendimentos_periodo()
        elif opcao == "2":
            relatorios.relatorio_servicos_mais_solicitados()
        elif opcao == "3":
            relatorios.relatorio_faturamento_barbeiro()
        elif opcao == "4":
            relatorios.relatorio_clientes_frequentes()
        elif opcao == "5":
            relatorios.relatorio_produtos_mais_vendidos()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
        
        input("\nPressione ENTER para continuar...")