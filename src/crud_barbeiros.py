import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sql'))
from database_mongodb import DatabaseMongo
from bson import ObjectId
from datetime import datetime

class CRUDBarbeiro:
    def __init__(self, db: DatabaseMongo):
        self.db = db
    
    def criar_barbeiro(self):
        """Cadastra um novo barbeiro"""
        print("\n=== CADASTRAR NOVO BARBEIRO ===\n")
        
        try:
            nome = input("Nome completo: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                return
            
            cpf = input("CPF (apenas números): ").strip()
            if len(cpf) != 11 or not cpf.isdigit():
                print("❌ CPF inválido! Deve conter 11 dígitos.")
                return
            
            # Verificar se CPF já existe
            if self.db.buscar_um("barbeiros", {"cpf": cpf}):
                print(f"\n❌ CPF {cpf} já está cadastrado!")
                return
            
            telefone = input("Telefone: ").strip()
            if not telefone:
                print("❌ Telefone é obrigatório!")
                return
            
            email = input("Email (opcional): ").strip() or None
            
            data_contratacao_str = input("Data de contratação (DD/MM/AAAA) [Enter=hoje]: ").strip()
            if data_contratacao_str:
                try:
                    data_contratacao = datetime.strptime(data_contratacao_str, "%d/%m/%Y")
                except ValueError:
                    print("⚠️  Data inválida! Usando data atual.")
                    data_contratacao = datetime.now()
            else:
                data_contratacao = datetime.now()
            
            print("\n💡 Especialidades: corte, barba, designer, coloração, tratamento")
            especialidade = input("Especialidade principal: ").strip() or None
            
            comissao_str = input("Comissão (%) [padrão=30%]: ").strip()
            if comissao_str:
                try:
                    comissao = float(comissao_str)
                    if comissao < 0 or comissao > 100:
                        print("⚠️  Comissão deve estar entre 0 e 100! Usando 30%.")
                        comissao = 30.0
                except ValueError:
                    print("⚠️  Comissão inválida! Usando 30%.")
                    comissao = 30.0
            else:
                comissao = 30.0
            
            # Configurar horários de trabalho
            print("\n📅 CONFIGURAR HORÁRIOS DE TRABALHO")
            print("(Deixe em branco para pular a configuração agora)\n")
            
            configurar = input("Deseja configurar horários agora? (S/N): ").strip().upper()
            
            horarios_trabalho = []
            if configurar == 'S':
                horarios_trabalho = self._configurar_horarios()
            
            # Criar documento
            barbeiro = {
                "nome": nome,
                "cpf": cpf,
                "telefone": telefone,
                "email": email,
                "data_contratacao": data_contratacao,
                "especialidade": especialidade,
                "comissao_percentual": comissao,
                "ativo": True,
                "horarios_trabalho": horarios_trabalho
            }
            
            barbeiro_id = self.db.inserir("barbeiros", barbeiro)
            
            if barbeiro_id:
                print(f"\n✅ Barbeiro '{nome}' cadastrado com sucesso!")
                print(f"   ID: {barbeiro_id}")
            else:
                print("\n❌ Erro ao cadastrar barbeiro!")
        
        except Exception as e:
            print(f"❌ Erro ao cadastrar barbeiro: {e}")
    
    def _configurar_horarios(self):
        """Helper: Configura horários de trabalho do barbeiro"""
        dias_semana = {
            '0': 'Domingo',
            '1': 'Segunda-feira',
            '2': 'Terça-feira',
            '3': 'Quarta-feira',
            '4': 'Quinta-feira',
            '5': 'Sexta-feira',
            '6': 'Sábado'
        }
        
        horarios = []
        
        print("\nDias da semana (0=Domingo, 1=Segunda, ..., 6=Sábado)")
        print("Digite os dias separados por vírgula (ex: 1,2,3,4,5)")
        
        dias_str = input("\nDias de trabalho: ").strip()
        dias = [d.strip() for d in dias_str.split(',') if d.strip() in dias_semana]
        
        if not dias:
            print("⚠️  Nenhum dia válido informado.")
            return []
        
        horario_inicio = input("Horário de início (HH:MM): ").strip()
        horario_fim = input("Horário de término (HH:MM): ").strip()
        
        # Validar horários
        try:
            datetime.strptime(horario_inicio, "%H:%M")
            datetime.strptime(horario_fim, "%H:%M")
        except ValueError:
            print("⚠️  Horário inválido! Use formato HH:MM")
            return []
        
        for dia in dias:
            horarios.append({
                "dia_semana": int(dia),
                "horario_inicio": horario_inicio,
                "horario_fim": horario_fim,
                "ativo": True
            })
        
        print(f"\n✅ Configurado para {len(dias)} dia(s) da semana")
        return horarios
    
    def listar_barbeiros(self):
        """Lista todos os barbeiros cadastrados"""
        print("\n=== LISTA DE BARBEIROS ===\n")
        
        from pymongo import ASCENDING
        
        barbeiros = self.db.buscar_todos(
            "barbeiros",
            ordenacao=[("nome", ASCENDING)]
        )
        
        if not barbeiros:
            print("⚠️  Nenhum barbeiro cadastrado.")
            return
        
        print(f"{'Nome':<30} {'CPF':<15} {'Especialidade':<15} {'Comissão':<10} {'Status':<10}")
        print("-" * 80)
        
        for barbeiro in barbeiros:
            nome = barbeiro['nome'][:28]
            cpf = barbeiro['cpf']
            cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            especialidade = barbeiro.get('especialidade', '-')[:13]
            comissao = barbeiro.get('comissao_percentual', 30.0)
            ativo = barbeiro.get('ativo', True)
            status = "Ativo" if ativo else "Inativo"
            
            print(f"{nome:<30} {cpf_fmt:<15} {especialidade:<15} {comissao}%{'':<6} {status:<10}")
        
        print(f"\nTotal: {len(barbeiros)} barbeiro(s)")
    
    def buscar_barbeiro(self):
        """Busca um barbeiro por CPF ou Nome"""
        print("\n=== BUSCAR BARBEIRO ===\n")
        print("[1] Buscar por CPF")
        print("[2] Buscar por Nome")
        print("[0] Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            cpf = input("\nDigite o CPF (apenas números): ").strip()
            barbeiro = self.db.buscar_um("barbeiros", {"cpf": cpf})
            
            if barbeiro:
                self._exibir_barbeiro_detalhado(barbeiro)
            else:
                print(f"\n⚠️  Barbeiro com CPF {cpf} não encontrado.")
        
        elif opcao == "2":
            nome = input("\nDigite o nome (ou parte dele): ").strip()
            from pymongo import ASCENDING
            
            barbeiros = self.db.buscar_todos(
                "barbeiros",
                {"nome": {"$regex": nome, "$options": "i"}},
                ordenacao=[("nome", ASCENDING)]
            )
            
            if not barbeiros:
                print(f"\n⚠️  Nenhum barbeiro encontrado com '{nome}'")
                return
            
            print(f"\n✅ Encontrado(s) {len(barbeiros)} barbeiro(s):\n")
            
            for barbeiro in barbeiros:
                self._exibir_barbeiro_detalhado(barbeiro)
        
        elif opcao == "0":
            return
        else:
            print("\n❌ Opção inválida!")
    
    def _exibir_barbeiro_detalhado(self, barbeiro):
        """Exibe dados completos do barbeiro"""
        cpf = barbeiro['cpf']
        cpf_fmt = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        
        print("\n" + "="*70)
        print(f"ID: {barbeiro['_id']}")
        print(f"Nome: {barbeiro['nome']}")
        print(f"CPF: {cpf_fmt}")
        print(f"Telefone: {barbeiro['telefone']}")
        print(f"Email: {barbeiro.get('email', '-')}")
        print(f"Data Contratação: {barbeiro['data_contratacao'].strftime('%d/%m/%Y')}")
        print(f"Especialidade: {barbeiro.get('especialidade', '-')}")
        print(f"Comissão: {barbeiro.get('comissao_percentual', 30.0)}%")
        print(f"Status: {'Ativo' if barbeiro.get('ativo', True) else 'Inativo'}")
        
        horarios = barbeiro.get('horarios_trabalho', [])
        if horarios:
            dias_semana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
            print(f"\n📅 Horários de Trabalho:")
            for h in horarios:
                dia_nome = dias_semana[h['dia_semana']]
                status_h = "✓" if h.get('ativo', True) else "✗"
                print(f"   {status_h} {dia_nome}: {h['horario_inicio']} - {h['horario_fim']}")
        else:
            print("\n📅 Horários: Não configurado")
        
        print("="*70)
    
    def atualizar_barbeiro(self):
        """Atualiza dados de um barbeiro"""
        print("\n=== ATUALIZAR BARBEIRO ===\n")
        
        cpf = input("CPF do barbeiro: ").strip()
        
        if not cpf:
            print("❌ CPF é obrigatório!")
            return
        
        barbeiro = self.db.buscar_um("barbeiros", {"cpf": cpf})
        
        if not barbeiro:
            print(f"\n⚠️  Barbeiro com CPF {cpf} não encontrado!")
            return
        
        print(f"\nBarbeiro: {barbeiro['nome']}")
        print("\n💡 Deixe em branco para manter o valor atual\n")
        
        nome = input(f"Nome [{barbeiro['nome']}]: ").strip()
        telefone = input(f"Telefone [{barbeiro['telefone']}]: ").strip()
        email = input(f"Email [{barbeiro.get('email', '-')}]: ").strip()
        especialidade = input(f"Especialidade [{barbeiro.get('especialidade', '-')}]: ").strip()
        
        comissao_str = input(f"Comissão (%) [{barbeiro.get('comissao_percentual', 30.0)}]: ").strip()
        comissao = None
        if comissao_str:
            try:
                comissao = float(comissao_str)
                if comissao < 0 or comissao > 100:
                    print("⚠️  Comissão inválida! Mantendo valor atual.")
                    comissao = None
            except ValueError:
                print("⚠️  Comissão inválida! Mantendo valor atual.")
                comissao = None
        
        # Montar atualização
        atualizacao = {}
        
        if nome:
            atualizacao['nome'] = nome
        if telefone:
            atualizacao['telefone'] = telefone
        if email:
            atualizacao['email'] = email
        if especialidade:
            atualizacao['especialidade'] = especialidade
        if comissao is not None:
            atualizacao['comissao_percentual'] = comissao
        
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
        
        if self.db.atualizar("barbeiros", {"_id": barbeiro['_id']}, atualizacao):
            print("\n✅ Barbeiro atualizado com sucesso!")
        else:
            print("\n❌ Erro ao atualizar barbeiro!")
    
    def ativar_desativar_barbeiro(self):
        """Ativa ou desativa um barbeiro"""
        print("\n=== ATIVAR/DESATIVAR BARBEIRO ===\n")
        
        cpf = input("CPF do barbeiro: ").strip()
        
        if not cpf:
            print("❌ CPF é obrigatório!")
            return
        
        barbeiro = self.db.buscar_um("barbeiros", {"cpf": cpf})
        
        if not barbeiro:
            print(f"\n⚠️  Barbeiro com CPF {cpf} não encontrado!")
            return
        
        nome = barbeiro['nome']
        ativo = barbeiro.get('ativo', True)
        status_atual = "Ativo" if ativo else "Inativo"
        novo_status = not ativo
        acao = "desativar" if ativo else "ativar"
        
        confirmacao = input(f"\nBarbeiro '{nome}' está {status_atual}. Deseja {acao}? (S/N): ").strip().upper()
        
        if confirmacao != 'S':
            print("❌ Operação cancelada.")
            return
        
        if self.db.atualizar("barbeiros", {"_id": barbeiro['_id']}, {"ativo": novo_status}):
            print(f"\n✅ Barbeiro '{nome}' {'ativado' if novo_status else 'desativado'} com sucesso!")
        else:
            print("\n❌ Erro ao atualizar status!")
    
    def deletar_barbeiro(self):
        """Remove um barbeiro do sistema"""
        print("\n=== REMOVER BARBEIRO ===\n")
        
        cpf = input("CPF do barbeiro: ").strip()
        
        if not cpf:
            print("❌ CPF é obrigatório!")
            return
        
        barbeiro = self.db.buscar_um("barbeiros", {"cpf": cpf})
        
        if not barbeiro:
            print(f"\n⚠️  Barbeiro com CPF {cpf} não encontrado!")
            return
        
        nome = barbeiro['nome']
        
        # Verificar se tem atendimentos
        atendimento = self.db.buscar_um("atendimentos", {"barbeiro_id": barbeiro['_id']})
        
        if atendimento:
            print(f"\n❌ NÃO É POSSÍVEL DELETAR!")
            print(f"   O barbeiro '{nome}' possui atendimentos registrados.")
            print("   Por questões de integridade, não pode ser removido.")
            return
        
        print(f"\n⚠️  ATENÇÃO: Remover o barbeiro '{nome}' é irreversível!")
        confirmacao = input("Digite 'CONFIRMAR' para prosseguir: ").strip()
        
        if confirmacao != 'CONFIRMAR':
            print("❌ Operação cancelada.")
            return
        
        if self.db.deletar("barbeiros", {"_id": barbeiro['_id']}):
            print(f"\n✅ Barbeiro '{nome}' removido com sucesso!")
        else:
            print("\n❌ Erro ao deletar barbeiro!")


def menu_barbeiros(db: DatabaseMongo):
    """Menu de gerenciamento de barbeiros"""
    crud = CRUDBarbeiro(db)
    
    while True:
        print("\n" + "="*60)
        print("          GERENCIAR BARBEIROS")
        print("="*60)
        print("\n[1] Cadastrar Barbeiro")
        print("[2] Listar Todos os Barbeiros")
        print("[3] Buscar Barbeiro")
        print("[4] Atualizar Barbeiro")
        print("[5] Ativar/Desativar Barbeiro")
        print("[6] Remover Barbeiro")
        print("[0] Voltar ao Menu Principal")
        print("-"*60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            crud.criar_barbeiro()
        elif opcao == "2":
            crud.listar_barbeiros()
        elif opcao == "3":
            crud.buscar_barbeiro()
        elif opcao == "4":
            crud.atualizar_barbeiro()
        elif opcao == "5":
            crud.ativar_desativar_barbeiro()
        elif opcao == "6":
            crud.deletar_barbeiro()
        elif opcao == "0":
            break
        else:
            print("\n❌ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")