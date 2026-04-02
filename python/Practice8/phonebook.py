from connect import get_connection


def setup(cur, conn):
    cur.execute("DROP TABLE IF EXISTS pb_contacts CASCADE;")

    cur.execute("""
    CREATE TABLE pb_contacts (
        id SERIAL PRIMARY KEY,
        person_name TEXT UNIQUE,
        phone TEXT
    );
    """)

    # загружаем SQL файлы
    with open("functions.sql", "r") as f:
        cur.execute(f.read())

    with open("procedures.sql", "r") as f:
        cur.execute(f.read())

    conn.commit()
    print("Setup complete.")


def show_all(cur):
    cur.execute("SELECT * FROM pb_contacts;")
    for row in cur.fetchall():
        print(row)


def search(cur):
    text = input("Search: ")
    cur.execute("SELECT * FROM pb_search(%s);", (text,))
    for row in cur.fetchall():
        print(row)


def add_one(cur, conn):
    name = input("Name: ")
    phone = input("Phone: ")

    cur.execute("CALL pb_add_or_update(%s, %s);", (name, phone))
    conn.commit()


def add_many(cur, conn):
    n = int(input("How many: "))
    names, phones = [], []

    for i in range(n):
        names.append(input("Name: "))
        phones.append(input("Phone: "))

    cur.execute("CALL pb_add_many(%s, %s);", (names, phones))
    conn.commit()

    cur.execute("SELECT * FROM pb_invalid_data;")
    print("Invalid:")
    for row in cur.fetchall():
        print(row)


def pagination(cur):
    lim = int(input("Limit: "))
    off = int(input("Offset: "))

    cur.execute("SELECT * FROM pb_get_page(%s, %s);", (lim, off))
    for row in cur.fetchall():
        print(row)


def delete_name(cur, conn):
    name = input("Name: ")
    cur.execute("CALL pb_delete(%s, %s);", (name, None))
    conn.commit()


def delete_phone(cur, conn):
    phone = input("Phone: ")
    cur.execute("CALL pb_delete(%s, %s);", (None, phone))
    conn.commit()


def menu():
    print("\n1 Show")
    print("2 Search")
    print("3 Add")
    print("4 Add many")
    print("5 Pagination")
    print("6 Delete name")
    print("7 Delete phone")
    print("0 Exit")


def main():
    conn = get_connection()
    cur = conn.cursor()

    setup(cur, conn)

    while True:
        menu()
        c = input("Choice: ")

        if c == "1":
            show_all(cur)
        elif c == "2":
            search(cur)
        elif c == "3":
            add_one(cur, conn)
        elif c == "4":
            add_many(cur, conn)
        elif c == "5":
            pagination(cur)
        elif c == "6":
            delete_name(cur, conn)
        elif c == "7":
            delete_phone(cur, conn)
        elif c == "0":
            break

    cur.close()
    conn.close()


main()