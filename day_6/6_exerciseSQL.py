import mysql.connector

# importing os module for environment variables
import os

# importing necessary functions from dotenv library
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv()

sql_host = os.getenv("MYSQL_HOST")
sql_user = os.getenv("MYSQL_USER")
sql_psswd = os.getenv("MYSQL_PASSWORD")
sql_db = os.getenv("db")

try:
    # Establish a connection to the database
    connection = mysql.connector.connect(
        host=sql_host,
        user=sql_user,
        password=sql_psswd,
        database=sql_db,
    )

    print("\n Ligação feita com sucesso! \n")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS utilizadores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255),
            idade INT
        )
    """
    cursor.execute(create_table_query)

    # Insert data into the table
    insert_query = """INSERT INTO utilizadores (nome, idade) VALUES (%s, %s)"""
    data_to_insert = [("João", 25), ("Maria", 30), ("Pedro", 35), ("Ana", 40)]
    cursor.executemany(insert_query, data_to_insert)

    connection.commit()

    # Define the SQL command
    comando_sql = """SELECT * FROM utilizadores"""

    # Execute the SQL command and fetch all results
    cursor.execute(comando_sql)
    resultados = cursor.fetchall()
    # Print each result
    for resultado in resultados:
        print(resultado)

except mysql.connector.Error as error:
    print("Erro ao conectar ao MySQL", error)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
