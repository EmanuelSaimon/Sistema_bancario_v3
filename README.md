# Sistema Bancário em Python

Este é um projeto de sistema bancário orientado a objetos desenvolvido em Python.  
Ele implementa um sistema simples de contas bancárias com suporte a depósitos, saques, criação de clientes e contas, além de um histórico de transações.

## Funcionalidades

- Cadastro de Clientes (Pessoa Física)
- Criação de Contas Correntes
- Depósitos e Saques com histórico
- Extrato de transações
- Regras de saque: limite de valor e quantidade diária
- Histórico completo de transações
- Menu de navegação interativo via terminal

## Estrutura do Projeto

- `Conta`: Classe base com operações de depósito e saque
- `Conta_corrente`: Classe que herda de `Conta`, adiciona limites
- `Cliente` e `Pessoa_Fisica`: Representam os usuários
- `Transacao`, `Deposito`, `Saque`: Interface e implementações das transações
- `Historico`: Armazena as movimentações realizadas
- Funções auxiliares: menu, cadastro, depósito, saque, extrato, etc

## Conceitos Utilizados

- Programação Orientada a Objetos (POO)
- Herança, Encapsulamento, Polimorfismo e Abstração
- Interface com `abc.ABC`
- Composição de objetos (`Conta` possui um `Historico`)
- Boas práticas de código e separação de responsabilidades

## Requisitos

- Python 3.10 ou superior (recomendado)

## Como Executar

Clone o repositório e execute o script:

```bash
git clone https://github.com/seu-usuario/sistema-bancario.git
cd sistema-bancario
python sistema_bancario.py


## Como Executar o Projeto

1. Certifique-se de ter o Python instalado em sua máquina.
2. Clone o repositório para o seu ambiente local:
   ```bash
   git clone https://github.com/EmanuelSaimon/Sistema_bancario_v3.git
