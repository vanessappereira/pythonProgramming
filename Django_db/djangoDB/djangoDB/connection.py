# ========== Imports ==========
import mysql.connector
import os
from dotenv import load_dotenv

# Load values from the .env file into the script
load_dotenv()
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")


# Connect to server
def connect_server(user, password):
    try:
        # Establish a connection to the database
        cnx = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=user,
            password=password,
            db=os.getenv("MYSQL_DB"),
        )
        if cnx.is_connected:
            print("\n Connection established! \n")
            return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting at MySQL: {err}")