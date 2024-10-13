from abc import ABC,abstractmethod, abstractproperty
from datetime import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero_conta = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls,numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numeroconta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._agencia
        
    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
  
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("Operação falhou. Saldo insuficiente")
            return False

        elif valor > 0:
            self._saldo -= valor
            print(f"\nR${valor:.2f} foi sacado!")
            return True
        
        else:
            print("Operação falhou. Valor inválido")
            return False
        

    def depositar(self, valor):
        valor_positivo = valor > 0

        if valor_positivo:
            self._saldo += valor
            print(f"\nR${valor:.2f} foi depositado!")
            return True
                    
        else:
            print("Operação falhou. Valor inválido")
            return False
 
class Conta_corrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_numero_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("Operação falhou. Valor excedeu o limite de saque")
            return False

        elif excedeu_numero_saques:
            print("Operação falhou. Número máximo de saques diarios excedido")
            return False

        else:
            return super().sacar(valor)

    def __str__(self):
        return f"""
        Agência: {self._agencia}
        C/C: {self.numeroconta}
        Titular: {self.cliente.nome}
        """
            
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self,transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractmethod
    def adicionar(self, conta):
        pass

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.adicionar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_Fisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def adicionar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def adicionar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """

[C] Criar conta corrente
[L] Listar contas
[N] Novo usúario
[D] Depositar
[S] Sacar
[E] Extrato
[Q] Sair

=> """
    
    return input(menu)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui conta.")
        return

    return cliente.contas[0]

def deposito(clientes):
    cpf = input("Insira seu CPF: ")
    cliente = filtrar_usuario(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito((valor))

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
    
def cadastro_cliente(clientes):
    print("Cadastro - Novo Cliente \n")
    cpf = input("Insira seu cpf(Somente números): ")
    cliente = filtrar_usuario(cpf, clientes)
       
    if cliente:
        print("Usúario ja cadastrado.")
        return

    else:
        nome = input("Insira seu nome: ")
        data_nascimento = input("Insira sua data de nascimento: ")
        endereço = input("Insira seu endereço(Logradouro, numero - bairro - cidade/sigla estado): ")
        cliente = Pessoa_Fisica(endereco=endereço, cpf=cpf, nome=nome, data_nascimento=data_nascimento)

        clientes.append(cliente)
        print("Cliente criado com sucesso.")

def filtrar_usuario(cpf, clientes):
    usuarios_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def exibir_extrato(clientes):
    cpf = input("Insira seu CPF: ")
    cliente = filtrar_usuario(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return 

    print("===================== EXTRATO =====================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: R${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: R${conta.saldo:.2f}")
    print("===================================================")

def saque(clientes):
    cpf = input("Insira seu CPF: ")
    cliente = filtrar_usuario(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Informe o valor do deposito: "))
    transacao = Saque((valor))

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def criar_conta(numero_conta,clientes, contas):
    cpf = input("Insira seu CPF: ")
    cliente = filtrar_usuario(cpf,clientes)

    if not cliente:
        print("Usuário não encontrado")
        return
        
    conta = Conta_corrente.nova_conta(numero=numero_conta,cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)
    print("Conta criada com sucesso!")        
        

def listar_contas(contas):
    for conta in contas:
        print(str(conta))

def main():
    clientes = []
    contas = []


    while True:

        opcao = menu()

        if opcao == "D":
            deposito(clientes)
         
        elif opcao == "C":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta,clientes, contas)

        elif opcao == "L":
            listar_contas(contas)

        elif opcao == "N":
            cadastro_cliente(clientes)

        elif opcao == "S":
            saque(clientes)

        elif opcao == "E":
            exibir_extrato(clientes)

        elif opcao == "Q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()

