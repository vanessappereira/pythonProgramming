import mysql.connector
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()  # loads values from the .env file into the script

sql_host = os.getenv("MYSQL_HOST")
sql_user = os.getenv("MYSQL_USER")
sql_psswd = os.getenv("MYSQL_PASSWORD")
sql_db = os.getenv("MYSQL_DB")


# Connect to DB
def connectDB():
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(
            host=sql_host,
            user=sql_user,
            password=sql_psswd,
            database=sql_db,
        )
        if connection.is_connected:
            print("\n Ligação feita com sucesso! \n")
            return connection

    except mysql.connector.Error as error:
        print("Erro ao conectar ao MySQL", error)
        return None


# Criar tabela
def createTable(cursor):
    # Create a table if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            idade INT
        )
    """
    cursor.execute(create_table_query)


# Adicionar dados
def addData(cursor):
    try:
        # Insert data into the table
        nome = input("Introduza o nome: ")
        idade = int(input("Introduza a idade: "))

        insert_query = """INSERT INTO utilizadores (nome, idade) VALUES (%s, %s)"""
        dados = (nome, idade)
        cursor.execute(insert_query, dados)
        print("Dados adicionados com sucesso! ")

    except ValueError:
        print("Erro ao inserir dados")


# Eliminar dados
def deleteData(cursor):
    try:
        # Delete data from the table
        id = int(input("Introduza o ID do utilizador: "))
        cursor.execute("SELECT * FROM utilizadores WHERE id = %s" "", (id,))
        result = cursor.fetchone()
        if result:
            delete_query = """DELETE FROM utilizadores WHERE id = %s"""
            dados = (id,)
            cursor.execute(delete_query, dados)
            print("Dados eliminados com sucesso!")
        else:
            print("ID não encontrado")
    except ValueError:
        print("Erro ao eliminar dados, o valor deverá ser um número inteiro!")


# Alterar dados
def alterar_dados(cursor):
    try:
        # Change table data
        id = int(input("Introduza o ID do utilizador: "))
        cursor.execute("SELECT * FROM utilizadores WHERE id = %s" "", (id,))
        result = cursor.fetchone()
        if result:
            novo_nome = input("Introduza o novo nome: ")
            nova_idade = int(input("Introduza a nova idade: "))
            alterar_query = (
                """UPDATE utilizadores SET nome = %s, idade = %s WHERE id = %s"""
            )
            dados = (novo_nome, nova_idade, id)
            cursor.execute(alterar_query, dados)
            print("Dados alterados com sucesso!")
        else:
            print("ID não encontrado")
    except ValueError:
        print("Erro ao alterar dados, o valor deverá ser um número inteiro!")


# Listar dados
def listData(cursor):
    # List all data from the table
    select_query = "SELECT * FROM utilizadores"
    cursor.execute(select_query)
    results = cursor.fetchall()
    for result in results:
        print(result)


# Filtrar por nome
def filtrar_por_nome(cursor):
    name = input("Introduza o nome do utilizador a filtrar: ")
    cursor.execute("SELECT * FROM utilizadores WHERE nome = %s", (name,))
    results = cursor.fetchall()
    if results:
        for result in results:
            print(result)


# Contagem utilizadores
def contagem_utilizador(cursor):
    cursor.execute("SELECT COUNT(*) FROM utilizadores")
    result = cursor.fetchone()
    print(f"Existem {result[0]} utilizadores na base de dados\n")


# Média de idades
def media_idades(cursor):
    cursor.execute("SELECT AVG(idade) FROM utilizadores")
    result = cursor.fetchone()
    print(f"A média de idades é de {result[0]:.2f}\n")


# Adicionar colunas à tabela
def add_colunas(cursor):
    # Request a name for the column
    col_name = input("Introduza o nome da coluna a adicionar: ")
    # Request a data type for the column
    data_type = input(
        "Introduza o tipo de dados da coluna (e.g.,VARCHAR(255), INT, DATE): "
    )
    # Create the column
    cursor.execute(f"ALTER TABLE utilizadores ADD COLUMN {col_name} {data_type}")
    print("Coluna adicionada com sucesso!")


# Função para fazer o backup da tabela
def copia_seg_bd():
    try:
        sql_user = input("Introduza nome de utilizador da BD: ")
        sql_psswd = input("Introduza a password da BD: ")
        sql_db = input("Introduza o nome da BD: ")

        # Caminho para salvar o bckp
        backup_dir = input(
            "Introduza o diretório onde pretende gerar o ficheiro de backup da BD: "
        )
        backup_file = input(
            "Introduza o nome do ficheiro de backup (por exemplo, backup.sql): "
        )

        # Combinar diretório e nome do ficheiro para obter o caminho completo do backup
        backup_path = os.path.join(backup_dir, backup_file)

        # Validar o diretório do caminho do backup
        backup_dir = os.path.dirname(backup_path)
        if not os.path.exists(backup_dir):
            print("O diretório fornecido não existe.")
            return

        if not os.access(backup_dir, os.W_OK):
            print("Não há permissões de escrita no diretório fornecido.")
            return

        # Realização de bckp
        comando_bckp = f"mysqldump -u{sql_user} -p{sql_psswd} {sql_db}"
        with open(backup_path, "w") as f:
            process = subprocess.run(comando_bckp, shell=True, stdout=f)

        if process.returncode == 0:
            print("Backup da BD realizado com sucesso!")
        else:
            print(f"Erro ao realizar o backup da BD: {process.stderr.decode()}")
    except Exception as e:
        print(f"Erro ao realizar o backup da BD: {e}")


# Função para restaurar a BD
def restauro_bd():
    try:
        sql_user = input("Introduza nome de utilizador da BD: ")
        sql_psswd = input("Introduza a password da BD: ")
        sql_db = input("Introduza o nome da BD: ")

        # Caminho para restaurar o bckp
        backup_path = input("Introduza o caminho onde pretende carregar o ficheiro: ")

        # Validar o diretório ou caminho
        backup_dir = os.path.dirname(backup_path)
        if not os.path.exists(backup_dir):
            print("O diretório fornecido não existe.")
            return

        if not os.access(backup_dir, os.W_OK):
            print("Não há permissões de escrita no diretório fornecido.")
            return

        # Realização de restauro
        comando_restaurar = f"mysql -u{sql_user} -p{sql_psswd} {sql_db}"
        with open(backup_path, "r") as f:
            process = subprocess.run(comando_restaurar, shell=True, stdin=f)

        if process.returncode == 0:
            print("Restauro da BD realizado com sucesso!")
        else:
            print(f"Erro ao realizar o restauro da BD: {process.stderr.decode()}")
    except Exception as e:
        print(f"Erro ao realizar o restauro da BD: {e}")


# Menu
def menu():
    connect = connectDB()
    if connect.is_connected():
        cursor = connect.cursor()
        while True:
            print(
                "1 - Criar tabela de dados \n"
                + "2 - Adicionar dados na tabela \n"
                + "3 - Listar dados da tabela \n"
                + "4 - Remover dados da tabela \n"
                + "5 - Alterar dados da tabela \n"
                + "6 - Filtrar por nome \n"
                + "7 - Contagem de utilizadores \n"
                + "8 - Média de idades \n"
                + "9 - Adicionar coluna à tabela \n"
                + "10 - Backup BD \n"
                + "0 - Sair"
            )

            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                createTable(cursor)
            elif opcao == "2":
                addData(cursor)
            elif opcao == "3":
                listData(cursor)
            elif opcao == "4":
                deleteData(cursor)
            elif opcao == "5":
                alterar_dados(cursor)
            elif opcao == "6":
                filtrar_por_nome(cursor)
            elif opcao == "7":
                contagem_utilizador(cursor)
            elif opcao == "8":
                media_idades(cursor)
            elif opcao == "9":
                add_colunas(cursor)
            elif opcao == "10":
                copia_seg_bd()
            elif opcao == "0":
                print("Programa terminado. Obrigado por usar este programa!")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida!")

            connect.commit()
        cursor.close()
        connect.close()


menu()
