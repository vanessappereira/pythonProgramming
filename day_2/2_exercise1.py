def soma():
    try:
        num1 = float(input("Introduza o primeiro número a somar: "))
        num2 = float(input("Introduza o primeiro número a somar: "))

    except ValueError:
        print("Erro: Introduza um número real.")

    resultado = num1 + num2

    print(f"O resultado da soma {num1} e {num2} é {resultado}.")


def sub():
    try:
        num1 = float(input("Introduza o primeiro número a subtrair: "))
        num2 = float(input("Introduza o primeiro número a subtrair: "))
    except ValueError:
        print("Erro: Introduza um número real.")

    resultado = num1 - num2
    print(f"O resultado da subtração {num1} e {num2} é {resultado}.")


def multi():
    try:
        num1 = float(input("Introduza o primeiro número a multiplicar: "))
        num2 = float(input("Introduza o primeiro número a multiplicar: "))
    except ValueError:
        print("Erro: Introduza um número real.")

    resultado = num1 * num2
    print(f"O resultado da multiplicação {num1} e {num2} é {resultado}.")


def div():
    try:
        num1 = float(input("Introduza o primeiro número a dividir: "))
        num2 = float(input("Introduza o primeiro número a dividir: "))
    except ValueError:
        print("Erro: Introduza um número real.")
    try:
        resultado = num1 / num2
        print(f"O resultado da divisão {num1} e {num2} é {resultado}.")
    except ZeroDivisionError:
        print("Erro: Não é possível dividir por zero.")


# Interface
while True:
    print(
        "Bem-vindo! Escolha uma das opções abaixo: \n"
        + "1. Somar \n"
        + "2. Subtrair \n"
        + "3. Multiplicar \n"
        + "4. Divisão \n"
        + "0. Sair"
    )
    opcao = input("Introduza a opção a executar: ")
    if opcao == 1:
        soma()
    elif opcao == 2:
        sub()
    elif opcao == 3:
        multi()
    elif opcao == 4:
        div()
    elif opcao == 0:
        print("Obrigado por utilizar o programa! Até a próxima. :)")
        break
