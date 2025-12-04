import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from datetime import datetime

class Relatorios:
    def __init__(self, db: DatabaseMongo):
        self.db = db
    
    def relatorio_atendimentos_periodo(self):
        """Relatório 1: Atendimentos realizados em um período"""
        print("\n=== RELATORIO: ATENDIMENTOS POR PERIODO ===\n")
        
        data_inicio = input("Data inicio (DD/MM/AAAA): ").strip()
        data_fim = input("Data fim (DD/MM/AAAA): ").strip()
        
        try:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y")
            # Adicionar um dia para incluir todo o dia final
            data_fim = datetime(data_fim.year, data_fim.month, data_fim.day, 23, 59, 59)
        except ValueError:
            print("Formato de data invalido! Use DD/MM/AAAA")
            return
        
        # Pipeline de agregação MongoDB
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {
                            "data_atendimento": {
                                "$gte": data_inicio,
                                "$lte": data_fim
                            }
                        },
                        {
                            "data_agendada": {
                                "$gte": data_inicio,
                                "$lte": data_fim
                            }
                        }
                    ],
                    "status": "finalizado"
                }
            },
            {
                "$addFields": {
                    "data_real": {
                        "$ifNull": ["$data_atendimento", "$data_agendada"]
                    }
                }
            },
            {
                "$sort": {"data_real": -1, "horario_inicio": -1}
            }
        ]
        
        resultados = self.db.agregacao("atendimentos", pipeline)
        
        if not resultados:
            print("\nNenhum atendimento encontrado neste periodo.")
            return
        
        print(f"{'Data':<12} {'Cliente':<25} {'Barbeiro':<20} {'Inicio':<8} {'Fim':<8} {'Tipo':<10} {'Valor':<12}")
        print("-" * 95)
        
        total_faturamento = 0
        
        for atend in resultados:
            data_real = atend.get('data_real')
            data_fmt = data_real.strftime("%d/%m/%Y") if data_real else "-"
            cliente = atend['cliente']['nome'][:23]
            barbeiro = atend['barbeiro']['nome'][:18]
            inicio = atend.get('horario_inicio', '-')
            fim = atend.get('horario_fim', '-')
            valor = atend.get('valor_total', 0)
            tipo = atend.get('tipo', '-')
            
            valor_fmt = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"{data_fmt:<12} {cliente:<25} {barbeiro:<20} {inicio:<8} {fim:<8} {tipo:<10} {valor_fmt:<12}")
            
            total_faturamento += valor
        
        total_fmt = f"R$ {total_faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 95)
        print(f"\nTotal de atendimentos: {len(resultados)}")
        print(f"Faturamento total: {total_fmt}")
    
    def relatorio_servicos_mais_solicitados(self):
        """Relatório 2: Ranking de serviços mais solicitados"""
        print("\n=== RELATORIO: SERVICOS MAIS SOLICITADOS ===\n")
        
        # Pipeline de agregação
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
                    "total_atendimentos": {"$sum": 1},
                    "faturamento": {"$sum": "$servicos.preco_cobrado"},
                    "preco_medio": {"$avg": "$servicos.preco_cobrado"}
                }
            },
            {
                "$sort": {"total_atendimentos": -1}
            }
        ]
        
        resultados = self.db.agregacao("atendimentos", pipeline)
        
        if not resultados:
            print("Nenhum servico foi solicitado ainda.")
            return
        
        print(f"{'Ranking':<8} {'Servico':<30} {'Atendimentos':<15} {'Preco Medio':<15} {'Faturamento':<15}")
        print("-" * 83)
        
        ranking = 1
        faturamento_total = 0
        
        for resultado in resultados:
            nome = resultado['_id'][:28]
            atendimentos = resultado['total_atendimentos']
            preco_medio = resultado['preco_medio']
            faturamento = resultado['faturamento']
            
            preco_fmt = f"R$ {preco_medio:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"{ranking}º{'':<6} {nome:<30} {atendimentos:<15} {preco_fmt:<15} {faturamento_fmt:<15}")
            
            faturamento_total += faturamento
            ranking += 1
        
        total_fmt = f"R$ {faturamento_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 83)
        print(f"\nFaturamento total dos servicos: {total_fmt}")
    
    def relatorio_faturamento_barbeiro(self):
        """Relatório 3: Faturamento por barbeiro em um período"""
        print("\n=== RELATORIO: FATURAMENTO POR BARBEIRO ===\n")
        
        data_inicio = input("Data inicio (DD/MM/AAAA): ").strip()
        data_fim = input("Data fim (DD/MM/AAAA): ").strip()
        
        try:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
            data_fim = datetime.strptime(data_fim, "%d/%m/%Y")
            data_fim = datetime(data_fim.year, data_fim.month, data_fim.day, 23, 59, 59)
        except ValueError:
            print("Formato de data invalido! Use DD/MM/AAAA")
            return
        
        # Pipeline de agregação
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {
                            "data_atendimento": {
                                "$gte": data_inicio,
                                "$lte": data_fim
                            }
                        },
                        {
                            "data_agendada": {
                                "$gte": data_inicio,
                                "$lte": data_fim
                            }
                        }
                    ],
                    "status": "finalizado"
                }
            },
            {
                "$group": {
                    "_id": "$barbeiro_id",
                    "nome": {"$first": "$barbeiro.nome"},
                    "comissao_percentual": {"$first": "$barbeiro.comissao_percentual"},
                    "total_atendimentos": {"$sum": 1},
                    "faturamento_total": {"$sum": "$valor_total"},
                    "comissao_total": {"$sum": "$comissao_barbeiro"}
                }
            },
            {
                "$sort": {"faturamento_total": -1}
            }
        ]
        
        resultados = self.db.agregacao("atendimentos", pipeline)
        
        # Buscar barbeiros ativos que não tiveram atendimentos
        barbeiros_ativos = self.db.buscar_todos("barbeiros", {"ativo": True})
        barbeiros_com_atendimento = {str(r['_id']) for r in resultados}
        
        # Adicionar barbeiros sem atendimento
        for barbeiro in barbeiros_ativos:
            if str(barbeiro['_id']) not in barbeiros_com_atendimento:
                resultados.append({
                    "_id": barbeiro['_id'],
                    "nome": barbeiro['nome'],
                    "comissao_percentual": barbeiro.get('comissao_percentual', 30.0),
                    "total_atendimentos": 0,
                    "faturamento_total": 0.0,
                    "comissao_total": 0.0
                })
        
        if not resultados:
            print("Nenhum barbeiro ativo encontrado.")
            return
        
        # Buscar especialidade dos barbeiros
        barbeiros_info = {}
        for barbeiro in barbeiros_ativos:
            barbeiros_info[str(barbeiro['_id'])] = barbeiro.get('especialidade', '-')
        
        print(f"{'Barbeiro':<30} {'Especialidade':<15} {'Atend.':<8} {'Faturamento':<15} {'Comissao':<12}")
        print("-" * 80)
        
        total_geral = 0
        total_comissoes = 0
        
        for resultado in resultados:
            nome = resultado['nome'][:28]
            barbeiro_id = str(resultado['_id'])
            espec = barbeiros_info.get(barbeiro_id, '-')
            atendimentos = resultado['total_atendimentos']
            faturamento = resultado['faturamento_total']
            comissao = resultado['comissao_total']
            
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            comissao_fmt = f"R$ {comissao:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            print(f"{nome:<30} {espec:<15} {atendimentos:<8} {faturamento_fmt:<15} {comissao_fmt:<12}")
            
            total_geral += faturamento
            total_comissoes += comissao
        
        lucro_liquido = total_geral - total_comissoes
        
        total_geral_fmt = f"R$ {total_geral:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        total_comissoes_fmt = f"R$ {total_comissoes:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        lucro_fmt = f"R$ {lucro_liquido:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        
        print("-" * 80)
        print(f"\nFaturamento total: {total_geral_fmt}")
        print(f"Total de comissoes: {total_comissoes_fmt}")
        print(f"Lucro liquido: {lucro_fmt}")
    
    def relatorio_clientes_frequentes(self):
        """Relatório 4: Clientes mais frequentes"""
        print("\n=== RELATORIO: CLIENTES MAIS FREQUENTES ===\n")
        
        # Pipeline de agregação
        pipeline = [
            {
                "$match": {"status": "finalizado"}
            },
            {
                "$group": {
                    "_id": "$cliente_id",
                    "nome": {"$first": "$cliente.nome"},
                    "telefone": {"$first": "$cliente.telefone"},
                    "total_atendimentos": {"$sum": 1},
                    "valor_gasto": {"$sum": "$valor_total"},
                    "ultima_visita": {"$max": "$data_atendimento"}
                }
            },
            {
                "$sort": {"total_atendimentos": -1, "valor_gasto": -1}
            },
            {
                "$limit": 20
            }
        ]
        
        resultados = self.db.agregacao("atendimentos", pipeline)
        
        if not resultados:
            print("Nenhum atendimento registrado ainda.")
            return
        
        print(f"{'#':<4} {'Cliente':<30} {'Telefone':<15} {'Atend.':<8} {'Gasto Total':<15} {'Ultima Visita':<15}")
        print("-" * 87)
        
        ranking = 1
        
        for resultado in resultados:
            nome = resultado['nome'][:28]
            telefone = resultado['telefone'][:13]
            atendimentos = resultado['total_atendimentos']
            valor = resultado['valor_gasto']
            ultima_visita = resultado.get('ultima_visita')
            
            valor_fmt = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            ultima_fmt = ultima_visita.strftime("%d/%m/%Y") if ultima_visita else "-"
            
            print(f"{ranking:<4} {nome:<30} {telefone:<15} {atendimentos:<8} {valor_fmt:<15} {ultima_fmt:<15}")
            ranking += 1
        
        print(f"\nTotal de clientes listados: {len(resultados)}")
    
    def relatorio_produtos_mais_vendidos(self):
        """Relatório 5: Produtos mais vendidos"""
        print("\n=== RELATORIO: PRODUTOS MAIS VENDIDOS ===\n")
        
        # Pipeline de agregação
        pipeline = [
            {
                "$match": {"status": "finalizado"}
            },
            {
                "$unwind": "$produtos_vendidos"
            },
            {
                "$group": {
                    "_id": "$produtos_vendidos.produto_id",
                    "nome": {"$first": "$produtos_vendidos.nome"},
                    "total_vendido": {"$sum": "$produtos_vendidos.quantidade"},
                    "faturamento": {"$sum": "$produtos_vendidos.subtotal"}
                }
            },
            {
                "$sort": {"total_vendido": -1}
            }
        ]
        
        vendas = self.db.agregacao("atendimentos", pipeline)
        
        if not vendas:
            print("Nenhuma venda de produto registrada ainda.")
            return
        
        # Buscar informações de estoque dos produtos
        produtos_dict = {}
        for venda in vendas:
            produto_id = venda['_id']
            produto_info = self.db.buscar_um("produtos", {"_id": produto_id})
            if produto_info:
                produtos_dict[str(produto_id)] = {
                    "estoque_atual": produto_info.get('estoque_atual', 0),
                    "estoque_minimo": produto_info.get('estoque_minimo', 5)
                }
        
        print(f"{'Produto':<30} {'Vendidos':<10} {'Faturamento':<15} {'Estoque':<10} {'Status':<10}")
        print("-" * 75)
        
        faturamento_total = 0
        
        for venda in vendas:
            nome = venda['nome'][:28]
            vendidos = venda['total_vendido']
            faturamento = venda['faturamento']
            
            produto_id_str = str(venda['_id'])
            info = produtos_dict.get(produto_id_str, {})
            estoque = info.get('estoque_atual', 0)
            estoque_min = info.get('estoque_minimo', 5)
            
            faturamento_fmt = f"R$ {faturamento:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            
            # Verificar status do estoque
            if estoque <= 0:
                status = "SEM"
            elif estoque <= estoque_min:
                status = "BAIXO"
            else:
                status = "OK"
            
            print(f"{nome:<30} {vendidos:<10} {faturamento_fmt:<15} {estoque:<10} {status:<10}")
            
            faturamento_total += faturamento
        
        total_fmt = f"R$ {faturamento_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print("-" * 75)
        print(f"\nFaturamento total em produtos: {total_fmt}")


def menu_relatorios(db: DatabaseMongo):
    """Menu de relatórios do sistema"""
    relatorios = Relatorios(db)
    
    while True:
        print("\n" + "="*60)
        print("          RELATORIOS")
        print("="*60)
        print("\n[1] Atendimentos por Periodo")
        print("[2] Servicos Mais Solicitados")
        print("[3] Faturamento por Barbeiro")
        print("[4] Clientes Mais Frequentes")
        print("[5] Produtos Mais Vendidos")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
        opcao = input("\nEscolha uma opcao: ").strip()
        
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
            print("\nOpcao invalida!")
        
        input("\nPressione ENTER para continuar...")