# Criação da lista vazia
numeros = []

# Função para adicionar números à lista
def addNumeros():
    try:
        numero = float(input("Adicione um número: "))
        numeros.append(numero)
        print(f"{numero} adicionado à lista com sucesso")
    except ValueError:
        print("Valor inválido")


# Função para mostrar a lista de números
def listaDeNumeros():
    print(numeros)


while True:
    print("Lista")
    print("1 - Adicionar número")
    print("2 - Listar")
    print("0. Sair")
    
    selecao = int(input("Selecione a opção desejada: "))
    if selecao == 1:
        addNumeros()
    elif selecao == 2:
        listaDeNumeros()
    elif selecao == 0:
        print("Programa terminado.")
        break
    else:
        print("Opção inválida. Tente novamente.")
     