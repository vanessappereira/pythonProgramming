import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # loads values from the .env file into the script

sql_host = os.getenv("MYSQL_HOST")
sql_user = os.getenv("MYSQL_USER")
sql_psswd = os.getenv("MYSQL_PASSWORD")
sql_db = os.getenv("MYSQL_DB")

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

# Listar dados
def listData(cursor):
    # List all data from the table
    select_query = "SELECT * FROM utilizadores"
    cursor.execute(select_query)
    results = cursor.fetchall()
    for result in results:
        print(result)
        
# Menu
def menu():
    connect = connectDB()
    if connect.is_connected():
        cursor = connect.cursor()
        while True:
            print("1 - Criar tabela de dados")
            print("2 - Adicionar dados na tabela")
            print("3 - Listar dados da tabela")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                createTable(cursor)
            elif opcao == "2":
                addData(cursor)
            elif opcao == "3":
                listData(cursor)
            elif opcao == "0":
                cursor.close()
                connect.close()
                print("Programa terminado. Obrigado por usar este programa!")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida!")

            connect.commit()

menu()
