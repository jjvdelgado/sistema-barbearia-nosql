import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from bson import ObjectId
from datetime import datetime

class CRUDClientes:
    def __init__(self, db: DatabaseMongo):
        self.db = db
    
    def cadastrar(self):
        """CREATE - Cadastra novo cliente"""
        print("\n=== CADASTRAR CLIENTE ===\n")
        
        nome = input("Nome completo: ").strip()
        if not nome:
            print("❌ Nome é obrigatório!")
            return
        
        cpf = input("CPF (apenas números): ").strip()
        if not cpf or len(cpf) != 11:
            print("❌ CPF inválido! Digite 11 dígitos.")
            return
        
        # Verificar se CPF já existe
        if self.db.buscar_um("clientes", {"cpf": cpf}):
            print(f"\n❌ CPF {cpf} já está cadastrado!")
            return
        
        telefone = input("Telefone: ").strip()
        if not telefone:
            print("❌ Telefone é obrigatório!")
            return
        
        email = input("Email (opcional): ").strip() or None
        
        data_nasc_str = input("Data de Nascimento DD/MM/AAAA (opcional): ").strip()
        data_nasc = None
        if data_nasc_str:
            try:
                data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y")
            except ValueError:
                print("⚠️  Data inválida, continuando sem data de nascimento.")
                data_nasc = None
        
        observacoes = input("Observações (opcional): ").strip() or None
        
        # Criar documento
        cliente = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email,
            "data_nascimento": data_nasc,
            "data_cadastro": datetime.now(),
            "observacoes": observacoes,
            "stats": {
                "total_atendimentos": 0,
                "valor_total_gasto": 0.0,
                "ultima_visita": None
            }
        }
        
        cliente_id = self.db.inserir("clientes", cliente)
        
        if cliente_id:
            print(f"\n✅ Cliente cadastrado com sucesso!")
            print(f"   ID: {cliente_id}")
            print(f"   Nome: {nome}")
        else:
            print("\n❌ Erro ao cadastrar cliente!")
    
    def consultar(self):
        """READ - Consulta clientes"""
        print("\n=== CONSULTAR CLIENTES ===\n")
        print("[1] Listar todos")
        print("[2] Buscar por nome")
        print("[3] Buscar por CPF")
        print("[0] Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            self._listar_todos()
        elif opcao == "2":
            self._buscar_por_nome()
        elif opcao == "3":
            self._buscar_por_cpf()
        elif opcao == "0":
            return
        else:
            print("\n❌ Opção inválida!")
    
    def _listar_todos(self):
        """Lista todos os clientes"""
        from pymongo import ASCENDING
        
        clientes = self.db.buscar_todos(
            "clientes",
            ordenacao=[("nome", ASCENDING)],
            limite=50
        )
        
        if not clientes:
            print("\n⚠️  Nenhum cliente cadastrado.")
            return
        
        print(f"\n{'Nome':<30} {'CPF':<15} {'Telefone':<15} {'Atend.':<8}")
        print("-" * 68)
        
        for c in clientes:
            nome = c['nome'][:28]
            cpf = c['cpf']
            telefone = c['telefone']
            atend = c['stats']['total_atendimentos']
            
            print(f"{nome:<30} {cpf:<15} {telefone:<15} {atend:<8}")
        
        print(f"\nTotal: {len(clientes)} cliente(s)")
        
        if len(clientes) == 50:
            print("⚠️  Mostrando apenas os primeiros 50 clientes")
    
    def _buscar_por_nome(self):
        """Busca clientes por nome"""
        nome = input("\nNome (pode ser parcial): ").strip()
        
        if not nome:
            print("❌ Digite um nome para buscar!")
            return
        
        from pymongo import ASCENDING
        
        clientes = self.db.buscar_todos(
            "clientes",
            {"nome": {"$regex": nome, "$options": "i"}},  # Case insensitive
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not clientes:
            print(f"\n⚠️  Nenhum cliente encontrado com '{nome}'")
            return
        
        print(f"\n✅ Encontrado(s) {len(clientes)} cliente(s):\n")
        
        for c in clientes:
            self._exibir_cliente_detalhado(c)
    
    def _buscar_por_cpf(self):
        """Busca cliente por CPF"""
        cpf = input("\nCPF (apenas números): ").strip()
        
        if not cpf:
            print("❌ Digite um CPF!")
            return
        
        cliente = self.db.buscar_um("clientes", {"cpf": cpf})
        
        if cliente:
            self._exibir_cliente_detalhado(cliente)
        else:
            print(f"\n⚠️  Cliente com CPF {cpf} não encontrado.")
    
    def _exibir_cliente_detalhado(self, cliente):
        """Exibe dados completos do cliente"""
        print("\n" + "="*50)
        print(f"ID: {cliente['_id']}")
        print(f"Nome: {cliente['nome']}")
        print(f"CPF: {cliente['cpf']}")
        print(f"Telefone: {cliente['telefone']}")
        print(f"Email: {cliente.get('email', '-')}")
        
        if cliente.get('data_nascimento'):
            print(f"Data Nascimento: {cliente['data_nascimento'].strftime('%d/%m/%Y')}")
        
        print(f"Cadastrado em: {cliente['data_cadastro'].strftime('%d/%m/%Y')}")
        
        stats = cliente.get('stats', {})
        print(f"\n📊 Estatísticas:")
        print(f"   Total de atendimentos: {stats.get('total_atendimentos', 0)}")
        
        valor_gasto = stats.get('valor_total_gasto', 0.0)
        valor_fmt = f"R$ {valor_gasto:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        print(f"   Valor total gasto: {valor_fmt}")
        
        if stats.get('ultima_visita'):
            print(f"   Última visita: {stats['ultima_visita'].strftime('%d/%m/%Y')}")
        
        if cliente.get('observacoes'):
            print(f"\nObservações: {cliente['observacoes']}")
        print("="*50)
    
    def atualizar(self):
        """UPDATE - Atualiza dados do cliente"""
        print("\n=== ATUALIZAR CLIENTE ===\n")
        
        cpf = input("CPF do cliente: ").strip()
        
        if not cpf:
            print("❌ CPF é obrigatório!")
            return
        
        cliente = self.db.buscar_um("clientes", {"cpf": cpf})
        
        if not cliente:
            print(f"\n⚠️  Cliente com CPF {cpf} não encontrado!")
            return
        
        print(f"\nCliente encontrado: {cliente['nome']}")
        print("\n💡 Deixe em branco para manter o valor atual\n")
        
        nome = input(f"Nome [{cliente['nome']}]: ").strip()
        telefone = input(f"Telefone [{cliente['telefone']}]: ").strip()
        email = input(f"Email [{cliente.get('email', '-')}]: ").strip()
        observacoes = input(f"Observações [{cliente.get('observacoes', '-')}]: ").strip()
        
        # Montar atualização
        atualizacao = {}
        
        if nome:
            atualizacao['nome'] = nome
        if telefone:
            atualizacao['telefone'] = telefone
        if email:
            atualizacao['email'] = email
        if observacoes:
            atualizacao['observacoes'] = observacoes
        
        if not atualizacao:
            print("\n⚠️  Nenhuma alteração informada.")
            return
        
        # Confirmar
        print("\n📝 Dados que serão atualizados:")
        for campo, valor in atualizacao.items():
            print(f"   • {campo}: {valor}")
        
        confirma = input("\nConfirmar atualização? (S/N): ").strip().upper()
        
        if confirma != 'S':
            print("❌ Atualização cancelada.")
            return
        
        if self.db.atualizar("clientes", {"_id": cliente['_id']}, atualizacao):
            print("\n✅ Cliente atualizado com sucesso!")
        else:
            print("\n❌ Erro ao atualizar cliente!")
    
    def deletar(self):
        """DELETE - Remove cliente"""
        print("\n=== DELETAR CLIENTE ===\n")
        
        cpf = input("CPF do cliente: ").strip()
        
        if not cpf:
            print("❌ CPF é obrigatório!")
            return
        
        cliente = self.db.buscar_um("clientes", {"cpf": cpf})
        
        if not cliente:
            print(f"\n⚠️  Cliente com CPF {cpf} não encontrado!")
            return
        
        print(f"\nCliente encontrado: {cliente['nome']}")
        
        # Verificar se tem atendimentos
        atendimento = self.db.buscar_um("atendimentos", {"cliente_id": cliente['_id']})
        
        if atendimento:
            print("\n❌ NÃO É POSSÍVEL DELETAR!")
            print("   Este cliente possui atendimentos registrados.")
            print("   Por questões de integridade, não pode ser removido.")
            return
        
        print("\n⚠️  ATENÇÃO: Esta ação não pode ser desfeita!")
        confirma = input(f"Deseja realmente deletar '{cliente['nome']}'? Digite 'SIM' para confirmar: ").strip().upper()
        
        if confirma == "SIM":
            if self.db.deletar("clientes", {"_id": cliente['_id']}):
                print("\n✅ Cliente deletado com sucesso!")
            else:
                print("\n❌ Erro ao deletar cliente!")
        else:
            print("\n❌ Operação cancelada.")


def menu_clientes(db: DatabaseMongo):
    """Menu CRUD de clientes"""
    crud = CRUDClientes(db)
    
    while True:
        print("\n" + "="*60)
        print("          GERENCIAR CLIENTES")
        print("="*60)
        print("\n[1] Cadastrar Cliente")
        print("[2] Consultar Clientes")
        print("[3] Atualizar Cliente")
        print("[4] Deletar Cliente")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            crud.cadastrar()
        elif opcao == "2":
            crud.consultar()
        elif opcao == "3":
            crud.atualizar()
        elif opcao == "4":
            crud.deletar()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")