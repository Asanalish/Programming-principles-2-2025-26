import psycopg
import csv

# Connecting to database
def connect():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="260708"
    )

# Creating table "phonebook"
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table phonebook created successfully.")

# Inserting data
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
        (username, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from console.")

# Uploading data from CSV file
def insert_from_csv(file_path):
    conn = connect()
    cur = conn.cursor()

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # skip header, because first string is just "username and phone"

        for row in reader:
            username, phone = row
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                (username, phone)
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from CSV.")

# Updating data
def update_user():
    old_username = input("Enter username to update: ")
    new_username = input("Enter new username: ")
    new_phone = input("Enter new phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE phonebook
        SET username = %s, phone = %s
        WHERE username = %s
        """,
        (new_username, new_phone, old_username)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("User updated.")

# Requesting(query-запрос) all data/ Or just printing the data
def query_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()

    print("\nAll contacts:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

# Search by name
def query_by_name():
    name = input("Enter name to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE username = %s",
        (name,) # <- that's very important, without comma -> (name) <- is incorrect. Потому что нужен tuple из одного элемента.

    )
    rows = cur.fetchall()

    print("\nSearch by name:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

# Searching by phone number
def query_by_phone():
    phone = input("Enter phone to search: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE phone = %s",
        (phone,)
    )
    rows = cur.fetchall()

    print("\nSearch by phone:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

# Deleting by name
def delete_by_name():
    name = input("Enter name to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE username = %s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("User deleted by name.")

# Deleting by phone number
def delete_by_phone():
    phone = input("Enter phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE phone = %s",
        (phone,)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("User deleted by phone.")

# Menu of the program, to make calling functions comfortable
def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Insert from console")
        print("3. Insert from CSV")
        print("4. Update user")
        print("5. Show all contacts")
        print("6. Search by name")
        print("7. Search by phone")
        print("8. Delete by name")
        print("9. Delete by phone")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == "4":
            update_user()
        elif choice == "5":
            query_all()
        elif choice == "6":
            query_by_name()
        elif choice == "7":
            query_by_phone()
        elif choice == "8":
            delete_by_name()
        elif choice == "9":
            delete_by_phone()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


menu()