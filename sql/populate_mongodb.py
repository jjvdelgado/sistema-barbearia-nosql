from database_mongodb import DatabaseMongo
from datetime import datetime

def popular_banco():
    """Popula o banco MongoDB com dados de exemplo"""
    
    print("="*60)
    print("   POPULAR BANCO DE DADOS - BARBEARIA MONGODB")
    print("="*60)
    
    db = DatabaseMongo()
    
    # Verificar se já tem dados
    total_docs = sum([
        db.clientes.count_documents({}),
        db.barbeiros.count_documents({}),
        db.servicos.count_documents({}),
        db.produtos.count_documents({})
    ])
    
    if total_docs > 0:
        print(f"\nATENCAO: Ja existem {total_docs} documentos no banco!")
        resposta = input("Deseja limpar e popular novamente? (S/N): ").strip().upper()
        
        if resposta == 'S':
            print("\nLimpando colecoes...")
            db.clientes.delete_many({})
            db.barbeiros.delete_many({})
            db.servicos.delete_many({})
            db.produtos.delete_many({})
            db.atendimentos.delete_many({})
            print("Colecoes limpas!")
        else:
            print("Operacao cancelada.")
            db.fechar()
            return
    
    print("\nInserindo dados de exemplo...\n")
    
    # ==================== CLIENTES ====================
    clientes_exemplo = [
        {
            "nome": "João Silva",
            "cpf": "12345678901",
            "telefone": "(41) 99999-1111",
            "email": "joao@email.com",
            "data_nascimento": datetime(1990, 5, 15),
            "data_cadastro": datetime.now(),
            "observacoes": "Cliente VIP",
            "stats": {"total_atendimentos": 0, "valor_total_gasto": 0.0, "ultima_visita": None}
        },
        {
            "nome": "Maria Santos",
            "cpf": "98765432100",
            "telefone": "(41) 98888-2222",
            "email": "maria@email.com",
            "data_nascimento": datetime(1985, 8, 20),
            "data_cadastro": datetime.now(),
            "observacoes": None,
            "stats": {"total_atendimentos": 0, "valor_total_gasto": 0.0, "ultima_visita": None}
        },
        {
            "nome": "Pedro Oliveira",
            "cpf": "11122233344",
            "telefone": "(41) 97777-3333",
            "email": "pedro@email.com",
            "data_nascimento": datetime(1995, 3, 10),
            "data_cadastro": datetime.now(),
            "observacoes": None,
            "stats": {"total_atendimentos": 0, "valor_total_gasto": 0.0, "ultima_visita": None}
        },
        {
            "nome": "Ana Costa",
            "cpf": "55544433322",
            "telefone": "(41) 96666-7777",
            "email": "ana@email.com",
            "data_nascimento": datetime(1992, 11, 25),
            "data_cadastro": datetime.now(),
            "observacoes": "Prefere atendimento pela manhã",
            "stats": {"total_atendimentos": 0, "valor_total_gasto": 0.0, "ultima_visita": None}
        },
        {
            "nome": "Carlos Mendes",
            "cpf": "66677788899",
            "telefone": "(41) 95555-8888",
            "email": "carlos.m@email.com",
            "data_nascimento": datetime(1988, 7, 8),
            "data_cadastro": datetime.now(),
            "observacoes": None,
            "stats": {"total_atendimentos": 0, "valor_total_gasto": 0.0, "ultima_visita": None}
        }
    ]
    
    # ==================== BARBEIROS ====================
    barbeiros_exemplo = [
        {
            "nome": "Carlos Barbeiro",
            "cpf": "55566677788",
            "telefone": "(41) 96666-4444",
            "email": "carlos@barbearia.com",
            "data_contratacao": datetime(2023, 1, 15),
            "especialidade": "Corte e Barba",
            "comissao_percentual": 30.0,
            "ativo": True,
            "horarios_trabalho": [
                {"dia_semana": 1, "horario_inicio": "09:00", "horario_fim": "18:00", "ativo": True},
                {"dia_semana": 2, "horario_inicio": "09:00", "horario_fim": "18:00", "ativo": True},
                {"dia_semana": 3, "horario_inicio": "09:00", "horario_fim": "18:00", "ativo": True},
                {"dia_semana": 4, "horario_inicio": "09:00", "horario_fim": "18:00", "ativo": True},
                {"dia_semana": 5, "horario_inicio": "09:00", "horario_fim": "18:00", "ativo": True},
            ]
        },
        {
            "nome": "Roberto Costa",
            "cpf": "44455566677",
            "telefone": "(41) 95555-5555",
            "email": "roberto@barbearia.com",
            "data_contratacao": datetime(2023, 6, 1),
            "especialidade": "Degradê",
            "comissao_percentual": 25.0,
            "ativo": True,
            "horarios_trabalho": [
                {"dia_semana": 2, "horario_inicio": "10:00", "horario_fim": "19:00", "ativo": True},
                {"dia_semana": 3, "horario_inicio": "10:00", "horario_fim": "19:00", "ativo": True},
                {"dia_semana": 4, "horario_inicio": "10:00", "horario_fim": "19:00", "ativo": True},
                {"dia_semana": 5, "horario_inicio": "10:00", "horario_fim": "19:00", "ativo": True},
                {"dia_semana": 6, "horario_inicio": "09:00", "horario_fim": "17:00", "ativo": True},
            ]
        },
        {
            "nome": "Fernando Alves",
            "cpf": "33344455566",
            "telefone": "(41) 94444-3333",
            "email": "fernando@barbearia.com",
            "data_contratacao": datetime(2024, 2, 10),
            "especialidade": "Corte Moderno",
            "comissao_percentual": 28.0,
            "ativo": True,
            "horarios_trabalho": [
                {"dia_semana": 1, "horario_inicio": "13:00", "horario_fim": "21:00", "ativo": True},
                {"dia_semana": 3, "horario_inicio": "13:00", "horario_fim": "21:00", "ativo": True},
                {"dia_semana": 5, "horario_inicio": "13:00", "horario_fim": "21:00", "ativo": True},
                {"dia_semana": 6, "horario_inicio": "09:00", "horario_fim": "17:00", "ativo": True},
            ]
        }
    ]
    
    # ==================== SERVIÇOS ====================
    servicos_exemplo = [
        {
            "nome": "Corte Masculino",
            "descricao": "Corte tradicional ou moderno",
            "preco": 45.0,
            "duracao_estimada": 30,
            "ativo": True,
            "stats": {"total_realizados": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Barba",
            "descricao": "Aparar e modelar barba",
            "preco": 25.0,
            "duracao_estimada": 20,
            "ativo": True,
            "stats": {"total_realizados": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Corte + Barba",
            "descricao": "Combo completo",
            "preco": 60.0,
            "duracao_estimada": 45,
            "ativo": True,
            "stats": {"total_realizados": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Degradê",
            "descricao": "Degradê profissional",
            "preco": 50.0,
            "duracao_estimada": 40,
            "ativo": True,
            "stats": {"total_realizados": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Corte Infantil",
            "descricao": "Corte para crianças até 12 anos",
            "preco": 35.0,
            "duracao_estimada": 25,
            "ativo": True,
            "stats": {"total_realizados": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Pigmentação de Barba",
            "descricao": "Tingimento e pigmentação",
            "preco": 40.0,
            "duracao_estimada": 35,
            "ativo": True,
            "stats": {"total_realizados": 0, "faturamento_total": 0.0}
        }
    ]
    
    # ==================== PRODUTOS ====================
    produtos_exemplo = [
        {
            "nome": "Pomada Modeladora",
            "descricao": "Fixação forte, acabamento natural",
            "preco_venda": 35.0,
            "estoque_atual": 20,
            "estoque_minimo": 5,
            "ativo": True,
            "stats": {"total_vendido": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Cera para Cabelo",
            "descricao": "Modelagem e brilho",
            "preco_venda": 30.0,
            "estoque_atual": 15,
            "estoque_minimo": 5,
            "ativo": True,
            "stats": {"total_vendido": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Óleo para Barba",
            "descricao": "Hidratação e perfume",
            "preco_venda": 40.0,
            "estoque_atual": 10,
            "estoque_minimo": 3,
            "ativo": True,
            "stats": {"total_vendido": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Shampoo Anticaspa",
            "descricao": "Tratamento e limpeza",
            "preco_venda": 25.0,
            "estoque_atual": 12,
            "estoque_minimo": 5,
            "ativo": True,
            "stats": {"total_vendido": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Balm para Barba",
            "descricao": "Hidratação profunda",
            "preco_venda": 45.0,
            "estoque_atual": 8,
            "estoque_minimo": 3,
            "ativo": True,
            "stats": {"total_vendido": 0, "faturamento_total": 0.0}
        },
        {
            "nome": "Gel Fixador",
            "descricao": "Fixação extrema",
            "preco_venda": 28.0,
            "estoque_atual": 18,
            "estoque_minimo": 5,
            "ativo": True,
            "stats": {"total_vendido": 0, "faturamento_total": 0.0}
        }
    ]
    
    # ==================== INSERIR DADOS PRIMEIRO! ====================
    try:
        db.clientes.insert_many(clientes_exemplo)
        print(f"OK - {len(clientes_exemplo)} clientes inseridos")
        
        db.barbeiros.insert_many(barbeiros_exemplo)
        print(f"OK - {len(barbeiros_exemplo)} barbeiros inseridos")
        
        db.servicos.insert_many(servicos_exemplo)
        print(f"OK - {len(servicos_exemplo)} servicos inseridos")
        
        db.produtos.insert_many(produtos_exemplo)
        print(f"OK - {len(produtos_exemplo)} produtos inseridos")
        
    except Exception as e:
        print(f"\nERRO ao inserir dados: {e}")
        db.fechar()
        return
    
# ==================== ATENDIMENTOS (após ter IDs) ====================
    
    print("\nCriando atendimentos de exemplo...")
    
    # Buscar IDs dos clientes, barbeiros e serviços inseridos
    cliente_joao = db.clientes.find_one({"cpf": "12345678901"})
    cliente_maria = db.clientes.find_one({"cpf": "98765432100"})
    cliente_pedro = db.clientes.find_one({"cpf": "11122233344"})
    cliente_ana = db.clientes.find_one({"cpf": "55544433322"})
    cliente_carlos = db.clientes.find_one({"cpf": "66677788899"})
    
    barbeiro_carlos = db.barbeiros.find_one({"cpf": "55566677788"})
    barbeiro_roberto = db.barbeiros.find_one({"cpf": "44455566677"})
    barbeiro_fernando = db.barbeiros.find_one({"cpf": "33344455566"})
    
    servico_corte = db.servicos.find_one({"nome": "Corte Masculino"})
    servico_barba = db.servicos.find_one({"nome": "Barba"})
    servico_combo = db.servicos.find_one({"nome": "Corte + Barba"})
    servico_degrade = db.servicos.find_one({"nome": "Degradê"})
    
    produto_pomada = db.produtos.find_one({"nome": "Pomada Modeladora"})
    produto_oleo = db.produtos.find_one({"nome": "Óleo para Barba"})
    
    atendimentos_exemplo = []
    
    # ========== ATENDIMENTOS FINALIZADOS (passado recente) ==========
    
    # Atendimento 1: João - Walk-in finalizado (ontem 02/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_joao['_id'],
        "barbeiro_id": barbeiro_carlos['_id'],
        "cliente": {
            "nome": cliente_joao['nome'],
            "telefone": cliente_joao['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_carlos['nome'],
            "comissao_percentual": barbeiro_carlos['comissao_percentual']
        },
        "tipo": "walkin",
        "status": "finalizado",
        "data_agendada": None,
        "horario_agendado": None,
        "data_atendimento": datetime(2025, 12, 2, 10, 30, 0),
        "horario_inicio": "10:30",
        "horario_fim": "11:15",
        "servicos": [
            {
                "servico_id": servico_corte['_id'],
                "nome": servico_corte['nome'],
                "preco_cobrado": servico_corte['preco']
            },
            {
                "servico_id": servico_barba['_id'],
                "nome": servico_barba['nome'],
                "preco_cobrado": servico_barba['preco']
            }
        ],
        "produtos_vendidos": [
            {
                "produto_id": produto_pomada['_id'],
                "nome": produto_pomada['nome'],
                "quantidade": 1,
                "preco_unitario": produto_pomada['preco_venda'],
                "subtotal": produto_pomada['preco_venda']
            }
        ],
        "valor_servicos": servico_corte['preco'] + servico_barba['preco'],
        "valor_produtos": produto_pomada['preco_venda'],
        "valor_total": servico_corte['preco'] + servico_barba['preco'] + produto_pomada['preco_venda'],
        "comissao_barbeiro": (servico_corte['preco'] + servico_barba['preco'] + produto_pomada['preco_venda']) * (barbeiro_carlos['comissao_percentual'] / 100),
        "forma_pagamento": "pix",
        "observacoes": "Cliente satisfeito",
        "created_at": datetime(2025, 12, 2, 10, 30, 0),
        "updated_at": datetime(2025, 12, 2, 11, 15, 0)
    })
    
    # Atendimento 2: Maria - Walk-in finalizado (ontem 02/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_maria['_id'],
        "barbeiro_id": barbeiro_roberto['_id'],
        "cliente": {
            "nome": cliente_maria['nome'],
            "telefone": cliente_maria['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_roberto['nome'],
            "comissao_percentual": barbeiro_roberto['comissao_percentual']
        },
        "tipo": "walkin",
        "status": "finalizado",
        "data_agendada": None,
        "horario_agendado": None,
        "data_atendimento": datetime(2025, 12, 2, 14, 0, 0),
        "horario_inicio": "14:00",
        "horario_fim": "14:40",
        "servicos": [
            {
                "servico_id": servico_degrade['_id'],
                "nome": servico_degrade['nome'],
                "preco_cobrado": servico_degrade['preco']
            }
        ],
        "produtos_vendidos": [],
        "valor_servicos": servico_degrade['preco'],
        "valor_produtos": 0.0,
        "valor_total": servico_degrade['preco'],
        "comissao_barbeiro": servico_degrade['preco'] * (barbeiro_roberto['comissao_percentual'] / 100),
        "forma_pagamento": "cartao_debito",
        "observacoes": None,
        "created_at": datetime(2025, 12, 2, 14, 0, 0),
        "updated_at": datetime(2025, 12, 2, 14, 40, 0)
    })
    
    # Atendimento 3: Pedro - Agendado e finalizado (semana passada 29/11/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_pedro['_id'],
        "barbeiro_id": barbeiro_carlos['_id'],
        "cliente": {
            "nome": cliente_pedro['nome'],
            "telefone": cliente_pedro['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_carlos['nome'],
            "comissao_percentual": barbeiro_carlos['comissao_percentual']
        },
        "tipo": "agendado",
        "status": "finalizado",
        "data_agendada": datetime(2025, 11, 29, 0, 0, 0),
        "horario_agendado": "16:00",
        "data_atendimento": datetime(2025, 11, 29, 16, 0, 0),
        "horario_inicio": "16:00",
        "horario_fim": "16:45",
        "servicos": [
            {
                "servico_id": servico_combo['_id'],
                "nome": servico_combo['nome'],
                "preco_cobrado": servico_combo['preco']
            }
        ],
        "produtos_vendidos": [
            {
                "produto_id": produto_oleo['_id'],
                "nome": produto_oleo['nome'],
                "quantidade": 1,
                "preco_unitario": produto_oleo['preco_venda'],
                "subtotal": produto_oleo['preco_venda']
            }
        ],
        "valor_servicos": servico_combo['preco'],
        "valor_produtos": produto_oleo['preco_venda'],
        "valor_total": servico_combo['preco'] + produto_oleo['preco_venda'],
        "comissao_barbeiro": (servico_combo['preco'] + produto_oleo['preco_venda']) * (barbeiro_carlos['comissao_percentual'] / 100),
        "forma_pagamento": "dinheiro",
        "observacoes": "Cliente regular",
        "created_at": datetime(2025, 11, 25, 10, 0, 0),
        "updated_at": datetime(2025, 11, 29, 16, 45, 0)
    })
    
    # ========== ATENDIMENTOS DE HOJE (03/12/2025) ==========
    
    # Atendimento 4: Ana - Walk-in finalizado HOJE pela manhã (03/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_ana['_id'],
        "barbeiro_id": barbeiro_fernando['_id'],
        "cliente": {
            "nome": cliente_ana['nome'],
            "telefone": cliente_ana['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_fernando['nome'],
            "comissao_percentual": barbeiro_fernando['comissao_percentual']
        },
        "tipo": "walkin",
        "status": "finalizado",
        "data_agendada": None,
        "horario_agendado": None,
        "data_atendimento": datetime(2025, 12, 3, 9, 15, 0),
        "horario_inicio": "09:15",
        "horario_fim": "09:45",
        "servicos": [
            {
                "servico_id": servico_corte['_id'],
                "nome": servico_corte['nome'],
                "preco_cobrado": servico_corte['preco']
            }
        ],
        "produtos_vendidos": [],
        "valor_servicos": servico_corte['preco'],
        "valor_produtos": 0.0,
        "valor_total": servico_corte['preco'],
        "comissao_barbeiro": servico_corte['preco'] * (barbeiro_fernando['comissao_percentual'] / 100),
        "forma_pagamento": "pix",
        "observacoes": None,
        "created_at": datetime(2025, 12, 3, 9, 15, 0),
        "updated_at": datetime(2025, 12, 3, 9, 45, 0)
    })
    
    # Atendimento 5: Carlos - Walk-in EM ANDAMENTO AGORA (03/12/2025 14:30)
    atendimentos_exemplo.append({
        "cliente_id": cliente_carlos['_id'],
        "barbeiro_id": barbeiro_roberto['_id'],
        "cliente": {
            "nome": cliente_carlos['nome'],
            "telefone": cliente_carlos['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_roberto['nome'],
            "comissao_percentual": barbeiro_roberto['comissao_percentual']
        },
        "tipo": "walkin",
        "status": "em_andamento",
        "data_agendada": None,
        "horario_agendado": None,
        "data_atendimento": datetime(2025, 12, 3, 14, 30, 0),
        "horario_inicio": "14:30",
        "horario_fim": None,
        "servicos": [
            {
                "servico_id": servico_barba['_id'],
                "nome": servico_barba['nome'],
                "preco_cobrado": servico_barba['preco']
            }
        ],
        "produtos_vendidos": [],
        "valor_servicos": servico_barba['preco'],
        "valor_produtos": 0.0,
        "valor_total": servico_barba['preco'],
        "comissao_barbeiro": servico_barba['preco'] * (barbeiro_roberto['comissao_percentual'] / 100),
        "forma_pagamento": None,
        "observacoes": "Em atendimento",
        "created_at": datetime(2025, 12, 3, 14, 30, 0),
        "updated_at": datetime(2025, 12, 3, 14, 30, 0)
    })
    
    # Atendimento 6: Pedro - Walk-in HOJE tarde (03/12/2025 16:00)
    atendimentos_exemplo.append({
        "cliente_id": cliente_pedro['_id'],
        "barbeiro_id": barbeiro_carlos['_id'],
        "cliente": {
            "nome": cliente_pedro['nome'],
            "telefone": cliente_pedro['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_carlos['nome'],
            "comissao_percentual": barbeiro_carlos['comissao_percentual']
        },
        "tipo": "walkin",
        "status": "finalizado",
        "data_agendada": None,
        "horario_agendado": None,
        "data_atendimento": datetime(2025, 12, 3, 16, 0, 0),
        "horario_inicio": "16:00",
        "horario_fim": "16:30",
        "servicos": [
            {
                "servico_id": servico_corte['_id'],
                "nome": servico_corte['nome'],
                "preco_cobrado": servico_corte['preco']
            }
        ],
        "produtos_vendidos": [],
        "valor_servicos": servico_corte['preco'],
        "valor_produtos": 0.0,
        "valor_total": servico_corte['preco'],
        "comissao_barbeiro": servico_corte['preco'] * (barbeiro_carlos['comissao_percentual'] / 100),
        "forma_pagamento": "dinheiro",
        "observacoes": None,
        "created_at": datetime(2025, 12, 3, 16, 0, 0),
        "updated_at": datetime(2025, 12, 3, 16, 30, 0)
    })
    
    # ========== ATENDIMENTOS AGENDADOS (futuro próximo) ==========
    
    # Atendimento 7: João - Agendado para AMANHÃ (04/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_joao['_id'],
        "barbeiro_id": barbeiro_carlos['_id'],
        "cliente": {
            "nome": cliente_joao['nome'],
            "telefone": cliente_joao['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_carlos['nome'],
            "comissao_percentual": barbeiro_carlos['comissao_percentual']
        },
        "tipo": "agendado",
        "status": "agendado",
        "data_agendada": datetime(2025, 12, 4, 0, 0, 0),
        "horario_agendado": "10:00",
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
        "observacoes": "Agendamento confirmado",
        "created_at": datetime(2025, 12, 3, 8, 0, 0),
        "updated_at": datetime(2025, 12, 3, 8, 0, 0)
    })
    
    # Atendimento 8: Maria - Agendado para AMANHÃ (04/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_maria['_id'],
        "barbeiro_id": barbeiro_roberto['_id'],
        "cliente": {
            "nome": cliente_maria['nome'],
            "telefone": cliente_maria['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_roberto['nome'],
            "comissao_percentual": barbeiro_roberto['comissao_percentual']
        },
        "tipo": "agendado",
        "status": "agendado",
        "data_agendada": datetime(2025, 12, 4, 0, 0, 0),
        "horario_agendado": "15:30",
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
        "observacoes": None,
        "created_at": datetime(2025, 12, 2, 18, 30, 0),
        "updated_at": datetime(2025, 12, 2, 18, 30, 0)
    })
    
    # Atendimento 9: Ana - Agendado para QUINTA-FEIRA (05/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_ana['_id'],
        "barbeiro_id": barbeiro_fernando['_id'],
        "cliente": {
            "nome": cliente_ana['nome'],
            "telefone": cliente_ana['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_fernando['nome'],
            "comissao_percentual": barbeiro_fernando['comissao_percentual']
        },
        "tipo": "agendado",
        "status": "agendado",
        "data_agendada": datetime(2025, 12, 5, 0, 0, 0),
        "horario_agendado": "09:00",
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
        "observacoes": "Prefere atendimento pela manhã",
        "created_at": datetime(2025, 12, 3, 12, 0, 0),
        "updated_at": datetime(2025, 12, 3, 12, 0, 0)
    })
    
    # Atendimento 10: Carlos - Agendado para SEXTA-FEIRA (06/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_carlos['_id'],
        "barbeiro_id": barbeiro_roberto['_id'],
        "cliente": {
            "nome": cliente_carlos['nome'],
            "telefone": cliente_carlos['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_roberto['nome'],
            "comissao_percentual": barbeiro_roberto['comissao_percentual']
        },
        "tipo": "agendado",
        "status": "agendado",
        "data_agendada": datetime(2025, 12, 6, 0, 0, 0),
        "horario_agendado": "11:00",
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
        "observacoes": None,
        "created_at": datetime(2025, 12, 3, 10, 0, 0),
        "updated_at": datetime(2025, 12, 3, 10, 0, 0)
    })
    
    # Atendimento 11: Pedro - Agendado para SEXTA-FEIRA (06/12/2025)
    atendimentos_exemplo.append({
        "cliente_id": cliente_pedro['_id'],
        "barbeiro_id": barbeiro_carlos['_id'],
        "cliente": {
            "nome": cliente_pedro['nome'],
            "telefone": cliente_pedro['telefone']
        },
        "barbeiro": {
            "nome": barbeiro_carlos['nome'],
            "comissao_percentual": barbeiro_carlos['comissao_percentual']
        },
        "tipo": "agendado",
        "status": "agendado",
        "data_agendada": datetime(2025, 12, 6, 0, 0, 0),
        "horario_agendado": "16:00",
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
        "observacoes": "Cliente preferencial",
        "created_at": datetime(2025, 11, 28, 16, 30, 0),
        "updated_at": datetime(2025, 11, 28, 16, 30, 0)
    })
    
    # Inserir atendimentos
    try:
        if atendimentos_exemplo:
            db.atendimentos.insert_many(atendimentos_exemplo)
            print(f"OK - {len(atendimentos_exemplo)} atendimentos inseridos")
            
            # Contar por status
            finalizados = sum(1 for a in atendimentos_exemplo if a['status'] == 'finalizado')
            em_andamento = sum(1 for a in atendimentos_exemplo if a['status'] == 'em_andamento')
            agendados = sum(1 for a in atendimentos_exemplo if a['status'] == 'agendado')
            
            print(f"  - {finalizados} finalizados")
            print(f"  - {em_andamento} em andamento")
            print(f"  - {agendados} agendados")
            
            # Atualizar estatísticas dos clientes
            print("\nAtualizando estatisticas dos clientes...")
            
            for atend in atendimentos_exemplo:
                if atend['status'] == 'finalizado':
                    cliente = db.clientes.find_one({"_id": atend['cliente_id']})
                    if cliente:
                        stats = cliente.get('stats', {})
                        stats['total_atendimentos'] = stats.get('total_atendimentos', 0) + 1
                        stats['valor_total_gasto'] = stats.get('valor_total_gasto', 0.0) + atend['valor_total']
                        stats['ultima_visita'] = atend['data_atendimento']
                        
                        db.clientes.update_one(
                            {"_id": atend['cliente_id']},
                            {"$set": {"stats": stats}}
                        )
            
            print("Estatisticas atualizadas!")
            
    except Exception as e:
        print(f"\nERRO ao inserir atendimentos: {e}")
    
    print("\n" + "="*60)
    print("   DADOS INSERIDOS COM SUCESSO!")
    print("="*60)
    print("\nResumo:")
    print(f"  - {len(clientes_exemplo)} clientes")
    print(f"  - {len(barbeiros_exemplo)} barbeiros")
    print(f"  - {len(servicos_exemplo)} servicos")
    print(f"  - {len(produtos_exemplo)} produtos")
    print(f"  - {len(atendimentos_exemplo)} atendimentos")
    print(f"\nTotal: {len(clientes_exemplo) + len(barbeiros_exemplo) + len(servicos_exemplo) + len(produtos_exemplo) + len(atendimentos_exemplo)} documentos")
    
    db.fechar()

if __name__ == "__main__":
    popular_banco()