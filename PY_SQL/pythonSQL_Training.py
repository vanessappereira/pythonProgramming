# ========== Imports ==========
from errno import errorcode
import getpass
import subprocess
import mysql.connector
import os
from dotenv import load_dotenv

# Load values from the .env file into the script
load_dotenv()
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")


# Connect to server
def connect_server():
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
            cursor = cnx.cursor()  # Create a cursor object
            return cnx, cursor
        
    except mysql.connector.Error as err:
        print(f"Error at MySQL connection: {err}")
        return None  # Return None if connection fails


# Verify if exists tables, if not, create one
def create_table(cursor):
    # Create a columns array
    columns = []
    try:
        # Request user to create variables for table_name and quantity of columns
        table_name = input("Please write the name of the table: ")
        columns_qty = int(input("How many columns will it have? "))

        for i in range(columns_qty):
            # Create column
            column_name = input(f"Write the name of column {i+1}: ")

            # Choose datatype
            print(
                "Choose the data type for this column: \n"
                + "1. INT \n"
                + "2. VARCHAR(255) \n"
                + "3. DATE \n"
                + "4. Other datatype"
            )
            datatype = int(input("Choose the number of the data type: "))
            if datatype == 1:
                column_datatype = "INT"
            elif datatype == 2:
                column_datatype = "VARCHAR(255)"
            elif datatype == 3:
                column_datatype = "DATE"
            elif datatype == 4:
                column_datatype = input("Write the datatype: ")
            else:
                print("Invalid option, please choose again")
                continue

            # Save data on previous table
            columns.append((column_name, column_datatype))

        formatted_columns = ", ".join(
            [f"{column[0]} {column[1]}" for column in columns]
        )

        # Create table with previous values
        query_create = f"""CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, {formatted_columns})"""

        # Execute query
        cursor.execute(query_create)
        print(f"Table {table_name} created sucessfully!")

    except ValueError as err:
        print(f"Error creating table: {err}")


# List datatable
def list_datatables(cursor):
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found")
            return None
        
        print("Select a database: ")
        
        for i, table in enumerate(tables, start=1):
            print(f"{i}. {table[0]}")
        
        while True:
            try:
                table_index = int(input("Select the table number: "))
                table_name = tables[table_index - 1][0]
                print(f"Selected table: {table_name}")
                return table_name
            except IndexError:
                print("Invalid table number. Please try again.")
    
    except Exception as err:
        print(f"Error listing tables: {err}")


# list table columns
def list_table_columns(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
    return [desc[0] for desc in cursor.description]


# List information from table
def list_table_info(cursor, table_name):
    try:
        # Verify if table its empty
        count = registry_count(cursor, table_name)

        if count == 0:
            print(f"The table {table_name} is empty")
            return

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Show columns titles
        column_names = [desc[0] for desc in cursor.description]
        print(f"Columns in {table_name}: {', '.join(column_names)}")

        # Show data
        for row in rows:
            print(row)

    except Exception as err:
        print("Error listing table info", err)


# Add/Update data
def add_update_data(cursor, table_name):
    try:
        list_table_info(cursor, table_name)

        id = int(input("Enter the id to update or -1 to add new data: ").strip())

        if id != -1:
            query_id = f"SELECT * FROM {table_name} WHERE id = %s"
            cursor.execute(query_id, (id,))
            result = cursor.fetchone()
            
            if result:
                print("Data found, updating...\n")
                print(result)

                column_name = input("Enter the column name to update: ")

                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                column_names = [desc[0] for desc in cursor.description]
                
                if column_name in column_names:
                    new_data = input("Enter the new data: ")
                    query_update = (
                        f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s"
                    )
                    cursor.execute(query_update, (new_data, id))
                    print(
                        f"Data has been updated in column '{column_name}' successfully!"
                    )
                else:
                    print(f"Column '{column_name}' does not exist in the table.")
            else:
                print("Data not found for the given id.")
            
        else:
            print("Adding new data...")

            
            columns = list_table_columns(cursor, table_name)
            columns.remove("id")
            new_data = []

            for column in columns:
                new_data.append(input(f"Enter the data for column {column}: "))

        
            placeholders = ", ".join(["%s"] * len(columns))
            query_insert = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            cursor.execute(query_insert, tuple(new_data))
            print("Data has been inserted successfully!")

    except Exception as err:
        print("Error adding/updating data:", err)



# Remove data from the table
def delete_data(cursor, table_name):
    try:
        list_table_info(cursor, table_name)
        # Select the id from the list to delete
        id = int(input("Enter the id to delete: "))
        query_id = f"SELECT * FROM {table_name} WHERE id = %s"
        cursor.execute(query_id, (id,))
        result = cursor.fetchone()

        if result:
            # Confirm deletion
            confirm = input("Are you sure you want to delete this data? (yes/no): ")

            if confirm.lower() == "yes":
                query_deleteData = f"DELETE FROM {table_name} WHERE id = %s"
                cursor.execute(query_deleteData, (id,))
                print(f"Data deleted successfully")
            elif confirm.lower() == "no":
                print("Data not deleted")
            else:
                print("Deletion cancelled")
                return
        else:
            print("Invalid input")

    except Exception as err:
        print(f"Error: {err}")


# Add columns to datatable
def add_columns(cursor, table_name):
    try:
        print(f"Table selected: {table_name}")

        # Show columns titles
        query_columns = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(query_columns)
        columns = [row[0] for row in cursor.fetchall()]
        columns.remove("id")

        # Appear only names separated by comma
        print(f"Current columns: {', '.join(columns)}")

        # Request a name for the new column
        column_name = input("Enter the name of the new column: ")

        # Request a datatype for the column
        column_datatype = input("Enter the data type (e.g.,VARCHAR(255), INT, DATE): ")

        # Query and execute
        query_add_column = (
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_datatype}"
        )
        cursor.execute(query_add_column)
        print(f"Column {column_name} added to the table {table_name} sucessfully!")
    except Exception as err:
        print(f"Error adding column: ", err)


# Remove columns to datatable
def remove_columns(cursor, table_name):
    try:
        print("Remove columns \n" + f"Table selected: {table_name}")

        # Show columns titles
        query_columns = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
        cursor.execute(query_columns)
        result = cursor.fetchone()

        columns = [row[0] for row in cursor.fetchall()]
        columns.remove("id")
        print(f"Current columns: {', '.join(columns)}")

        # Request the column to remove
        column_name_remove = input("Enter the name of the column to remove: ")

        if result:
            # Confirm deletion
            confirm = input("Are you sure you want to delete this data? (yes/no): ")
            if confirm.lower() == "yes":
                # Query and execute
                query_remove_column = (
                    f"ALTER TABLE {table_name} DROP COLUMN {column_name_remove}"
                )
                cursor.execute(query_remove_column)
                print(
                    f"Column {column_name_remove} removed from the table {table_name} sucessfully"
                )
                print(f"Current columns: {', '.join(columns)}")
            elif confirm.lower() == "no":
                print("Column not deleted")
            else:
                print("Deletion cancelled")
                return
        else:
            print("Invalid input")

    except Exception as err:
        print(f"Error deleting column: ", err)


# Registry information - Working
def registry_count(cursor, table_name):
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        # Print
        print(f"Number of records in the table {table_name}: {count}")

        return count
    except Exception as err:
        print(f"Error counting records in table {table_name}: {err}")


# Connecting as Admin
def connect_admin():
    try:
        # Prompt the user for their username and password
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")

        # Establish a connection to the server
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=username,
            password=password,
            database=os.getenv("MYSQL_DB"),
        )
        cursor = conn.cursor()

        print("Admin connected successfully!")
        return conn, cursor, username, password
    except mysql.connector.Error as err:
        print(f"Error connecting as admin: {err}")
        return None, None, None, None


# Backup DB
def backup_db():
    try:
        conn, cursor, username, password = connect_admin()
        if conn and cursor:
            # Backup path
            backup_dir = input("Write the file destination: ")

            # To restore, only CSV and JSON
            backup_file = input("Write the name of the backup file and extension: ")

            # Combine directory and the bckp file
            backup_path = os.path.join(backup_dir, backup_file)

            # Validate directory and path
            if not os.path.exists(os.path.dirname(backup_path)):
                os.makedirs(os.path.dirname(backup_path))
                print(f"Backup directory created at {backup_path}")

            # Validate permissions
            if not os.access(os.path.dirname(backup_path), os.W_OK):
                print(f"Permission denied to write in {backup_path}")
                return

            # Create the backup file
            query_backup = f"mysqldump -u {username} -p{password} {conn.database}"

            with open(backup_path, "w") as f:
                process = subprocess.run(
                    query_backup, shell=True, stdout=f, stderr=subprocess.PIPE
                )

            if process.returncode == 0:
                print(f"Backup created successfully at {backup_path}")
            else:
                print(f"Error creating backup: {process.stderr.decode()}")

            conn.close()

    except Exception as err:
        print(f"Error creating backup: {err}")


# Restore DB
def restore_db():
    try:
        conn, cursor, _, _ = connect_admin()
        if conn and cursor:
            # Path where is the restore backup
            restore_path = input("Write the full path of the backup file: ")

            # Verify the file location
            if not os.path.exists(restore_path):
                print("File not found. Please check the path.")
                return

            # Read the backup file and execute the SQL commands
            with open(restore_path, "r") as f:
                sql_commands = f.read().split(";")

            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)

            conn.commit()
            cursor.close()
            conn.close()

            print("Database restore completed successfully!")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
    except IOError as err:
        print(f"Error reading the file: {err}")
    except Exception as e:
        print(f"Error restoring the database: {e}")


# Menu
def main():
    try:
        result = connect_server()
        if result is None:
            print("Connection failed. Check your credentials and try again.")
            return
        
        # Unpack the connection and cursor
        cnx,cursor = result 
        
        if cnx and cursor:
            # Initialize an empty string to store the table name
            table_name = ""

            while True:
                print(
                    "======================================\n"
                    + "1 - Create datatable \n"
                    + "2 - Select datatable \n"
                    + "3 - List information from datatable \n"
                    + "4 - Add/Update data to datatable \n"
                    + "5 - Remove data from the table \n"
                    + "6 - Add columns to datatable \n"
                    + "7 - Remove columns from datatable \n"
                    + "8 - Registry information \n"
                    + "9 - Backup DB \n"
                    + "10 - Restore DB \n"
                    + "0 - Exit \n"
                    + "======================================"
                )
                option = int(input("Please choose an option: "))

                if option == 1:
                    create_table(cursor)

                elif option == 2:
                    # Select table
                    table_name = list_datatables(cursor)

                elif option == 3:
                    if table_name:
                        list_table_info(cursor, table_name)
                    else:
                        print("Please select a table first.")

                elif option == 4:
                    if table_name:
                        add_update_data(cursor, table_name)
                    else:
                        print("Please select a table first.")

                elif option == 5:
                    if table_name:
                        delete_data(cursor, table_name)
                    else:
                        print("Please select a table first.")

                elif option == 6:
                    if table_name:
                        add_columns(cursor, table_name)
                    else:
                        print("Please select a table first.")

                elif option == 7:
                    if table_name:
                        remove_columns(cursor, table_name)
                    else:
                        print("Please select a table first.")
                elif option == 8:
                    if table_name:
                        registry_count(cursor, table_name)
                    else:
                        print("Please select a table first.")

                elif option == 9:
                    backup_db()

                elif option == 10:
                    restore_db()

                elif option == 0:
                    print("Thank you for using this program. \nTerminated")
                    break
                else:
                    print("Invalid option. Please choose a valid option.")
                
                cnx.commit()

            if cnx and cursor is not None:
                cursor.close()
                cnx.close()

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
    except ValueError:
        print("Error: Please enter a valid option.")
    except KeyboardInterrupt:
        print("\nTerminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
