lista_livros = []


def addLivros():
    global lista_livros
    nome = input("Nome do livro: ")
    autor = input("Autor: ")
    ano = input("Ano: ")
    lista_livros.append([nome, autor, ano])
    print(f"{nome} adicionado com sucesso!")


def listarLivros():
    global lista_livros
    if not lista_livros:
        print("Nenhum livro foi adicionado")
    else:
        print("A lista contém os seguintes livros: \n")
        for i, nome in enumerate(lista_livros, start=1):
            print(f"{i} - {nome} \n")


def removerLivros():
    if not lista_livros:
        print("Nenhum livro foi adicionado")
    else:
        listarLivros()
        try:
            id = int(input("Escolha o livro que deseja remover: "))
            if 1 <= id <= len(listarLivros):
                livro_removido = lista_livros.pop(id - 1)
                print(f"{livro_removido} eliminado com sucesso!")
            else:
                print("ID incorreto, por favor selecione um id correto")

        except ValueError:
            print("Valor inválido")


def atualizarLivro():
    if not lista_livros:
        print("Nenhum livro foi adicionado")
    else:
        listarLivros()
        try:
            id = int(input("Escolha o livro que deseja atualizar: "))
            if 1 <= id <= len(listarLivros):
                nome = input("Nome do livro: ")
                autor = input("Autor: ")
                ano = input("Ano: ")
                lista_livros[id - 1] = [nome, autor, ano]
                print(f"{nome} atualizado com sucesso!")
            else:
                print("ID incorreto, por favor selecione um id correto")
        except ValueError:
            print("Valor inválido")


while True:
    print(
        "Lista \n"
        + "1 - Adicionar livro \n"
        + "2 - Listar livros \n"
        + "3 - Remover livros \n"
        + "4 - Atualizar livros \n"
        + "0. Sair \n"
    )

    selecao = int(input("Selecione a opção desejada: "))
    if selecao == 1:
        addLivros()
    elif selecao == 2:
        listarLivros()
    elif selecao == 3:
        removerLivros()
    elif selecao == 4:
        atualizarLivro()
    elif selecao == 0:
        print("Programa terminado.")
        break
    else:
        print("Opção inválida. Tente novamente.")
