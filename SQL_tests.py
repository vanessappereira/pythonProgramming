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
            print("\n Connection established! \n")
            return connection
    except mysql.connector.Error as error:
        print("Error connecting at MySQL", error)
        return None


# Create a table
def create_Table(cursor):
    try:
        # Create variables to the name of the table and quantity of columns
        table_name = input("Please write the name of the table: ")
        columns_qty = int(input("How many columns will have? "))
        columns = []
        for i in range(columns_qty):
            # Create column
            column_name = input(f"Write the name of the column {i+1}: ")

            # Select Datatype
            print("Select the data type: ")
            print("1 - INT")
            print("2 - VARCHAR(255)")
            print("3 - DATE")
            datatype = int(input("Choose the option: "))

            if datatype == 1:
                column_datatype = "INT"
            elif datatype == 2:
                column_datatype = "VARCHAR(255)"
            elif datatype == 3:
                column_datatype = "DATE"
            else:
                print("Invalid option. Please choose again.")
                return create_Table(cursor)

            # Save data on previous table
            columns.append((column_name, column_datatype))

        # Create table with previous values
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {', '.join([f'{coluna[0]} {coluna[1]}' for coluna in columns])})"
        )
        print("Table created sucessfully!")
    except ValueError as err:
        print("Error creating table!", err)


# List data
def list_tables(cursor):
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Select a table:")
        for i, table in enumerate(tables, start=1):
            print(f"{i} - {table[0]}")
        table_index = int(input("Enter the number of the table: "))
        table_name = tables[table_index - 1][0]
        print(f"Selected table: {table_name}")
        return table_name
    except Exception as e:
        print("Error listing tables", e)


# List information from table
def list_table_info(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Show column title
        column_names = [desc[0] for desc in cursor.description]
        print(f"Columns: {', '.join(column_names)}")

        # Show data
        for row in rows:
            print(row)
    except Exception as e:
        print("Error listing table info", e)


# Add Column
def add_column(cursor, table_name):
    try:
        # Request a name for the column
        column_name = input("Enter the column name: ")

        # Request a data type for the column
        data_type = input("Enter the data type (e.g.,VARCHAR(255), INT, DATE): ")

        # Create the column
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}")
        print(f"Column {column_name} added to table {table_name} successfully")

    except Exception as err:
        print("Error adding column:", err)


# Add data
def add_data(cursor, table_name):
    try:
        list_table_info(cursor, table_name)
        # Select id from list_table data
        id = int(input("Please select the id to add data: "))
        cursor.execute(
            f"SELECT * FROM {table_name} WHERE id = %s" "", (id,)
        )  # Use %s for parameterized query to prevent SQL injection
        result = cursor.fetchone()
        if result:
            print(result)
            # Request column to edit user
            column_name = input("Enter the column name to add data: ")
            # Confirm name of the column if its equal to db
            column_names = [desc[0] for desc in cursor.description]
            if column_name in column_names:
                # Request data to add
                data = input("Enter the data to add: ")
                cursor.execute(
                    f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s",
                    (data, id),
                )
                print(f"Data added to column {column_name} successfully")
            else:
                print("Column name not found")
        else:
            print("Id not found")

    except Exception as err:
        print("Error adding data:", err)


# Delete data
def delete_data(cursor, table_name):
    try:
        list_table_info(cursor, table_name)
        # Select id from list_table data
        id = int(input("Please select the id to delete data: "))
        cursor.execute(
            f"SELECT * FROM {table_name} WHERE id = %s" "", (id,)
        )  # Use %s for parameterized query to prevent SQL injection
        result = cursor.fetchone()
        if result:
            # Confirm deletion
            confirm = input("Are you sure you want to delete this data? (yes/no): ")

            if confirm.lower() == "yes":
                query_deleteData = f"DELETE FROM {table_name} WHERE id = %s"
                cursor.execute(query_deleteData, (id,))
                print(f"Data deleted successfully")
            else:
                print("Deletion cancelled")
        else:
            print("Invalid input")
    except ValueError as e:
        print(f"Error: {e}")


# Change Data - Still to implement


# Menu
def menu():
    connect = connectDB()
    if connect.is_connected():
        cursor = connect.cursor()
        # Initialize an empty string to store the table name
        table_name = ""

        while True:
            print(
                "=================================\n"
                + "1 - Create datatable \n"
                + "2 - Select datatable \n"
                + "3 - List information from datatable \n"
                + "4 - Add data to datatable \n"
                + "5 - Remove data from the table \n"
                + "0 - Sair \n"
                + "================================="
            )

            option = input("Choose an option: ")
            if option == "1":
                create_Table(cursor)
            
            elif option == "2":
                # Store the table name in the variable
                table_name = list_tables(cursor)
            
            elif option == "3":
                if table_name:
                    list_table_info(cursor, table_name)
                else:
                    print("Select a table first")
            
            elif option == "4":
                # Check if table_name is not empty
                if table_name:
                    add_data(cursor, table_name)
                else:
                    print("Please select a table first.")
            
            elif option == "5":
                if table_name:
                    delete_data(cursor, table_name)
                else:
                    print("Please select a table first.")
            
            elif option == "0":
                print("Thank you for using this program. \nTerminated")
                break
            
            else:
                print("Invalid option. Please choose a valid option.")

            connect.commit()
        cursor.close()
        connect.close()


menu()
