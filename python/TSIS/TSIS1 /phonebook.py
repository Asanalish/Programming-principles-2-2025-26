import csv
import json
import os
from connect import get_connection


def run_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(BASE_DIR, filename), "r", encoding="utf-8") as file:
        sql = file.read()

    cur.execute(sql)
    conn.commit()

    cur.close()
    conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    print("Database was created successfully.")


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )

    cur.execute(
        "SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)",
        (group_name,)
    )

    row = cur.fetchone()

    if row is None:
        return None

    return row[0]


def add_contact():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday (YYYY-MM-DD): ").strip()
    group_name = input("Group: ").strip()
    phone = input("Phone: ").strip()
    phone_type = input("Phone type (home/work/mobile): ").strip()

    if phone_type not in ("home", "work", "mobile"):
        print("Wrong phone type.")
        return

    conn = get_connection()
    cur = conn.cursor()

    group_id = get_group_id(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts (name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name)
        DO UPDATE SET
            email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (name, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
        (contact_id, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Contact was saved.")


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print("-" * 60)
        print("ID:", row[0])
        print("Name:", row[1])
        print("Email:", row[2])
        print("Birthday:", row[3])
        print("Group:", row[4])

        if len(row) == 7:
            print("Date added:", row[5])
            print("Phones:", row[6])
        else:
            print("Phones:", row[5])


def show_all_contacts():
    sort_by = input("Sort by name/birthday/date_added: ").strip()

    if sort_by not in ("name", "birthday", "date_added"):
        sort_by = "name"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM get_contacts_page(%s, %s, %s)",
        (100, 0, sort_by)
    )

    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.name
        """,
        (group_name,)
    )

    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def search_contact():
    query = input("Search query: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (query,)
    )

    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def search_by_email():
    email_part = input("Email contains: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE LOWER(c.email) LIKE LOWER(%s)
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.name
        """,
        ("%" + email_part + "%",)
    )

    rows = cur.fetchall()

    print_contacts(rows)

    cur.close()
    conn.close()


def paginated_contacts():
    limit = 2
    offset = 0

    sort_by = input("Sort by name/birthday/date_added: ").strip()

    if sort_by not in ("name", "birthday", "date_added"):
        sort_by = "name"

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM get_contacts_page(%s, %s, %s)",
            (limit, offset, sort_by)
        )

        rows = cur.fetchall()

        print("\nPAGE:", offset // limit + 1)
        print_contacts(rows)

        cur.close()
        conn.close()

        command = input("\nnext / prev / quit: ").strip().lower()

        if command == "next":
            if rows:
                offset += limit
        elif command == "prev":
            offset -= limit

            if offset < 0:
                offset = 0
        elif command == "quit":
            break
        else:
            print("Unknown command.")


def add_phone_to_contact():
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = input("Type (home/work/mobile): ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL add_phone(%s, %s, %s)",
        (name, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Procedure add_phone was called.")


def move_contact_to_group():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "CALL move_to_group(%s, %s)",
        (name, group_name)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Procedure move_to_group was called.")


def export_to_json():
    filename = input("JSON filename to save: ").strip()

    if filename == "":
        filename = "contacts_export.json"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
        """
    )

    contacts = cur.fetchall()
    result = []

    for contact in contacts:
        contact_id = contact[0]

        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s ORDER BY id",
            (contact_id,)
        )

        phone_rows = cur.fetchall()

        result.append({
            "name": contact[1],
            "email": contact[2],
            "birthday": str(contact[3]) if contact[3] else None,
            "group": contact[4],
            "phones": [
                {
                    "phone": phone_row[0],
                    "type": phone_row[1]
                }
                for phone_row in phone_rows
            ]
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()

    print("Exported to", filename)


def save_contact_from_json(cur, item, overwrite):
    name = item["name"]
    email = item.get("email")
    birthday = item.get("birthday")
    group_name = item.get("group", "Other")
    phones = item.get("phones", [])

    group_id = get_group_id(cur, group_name)

    cur.execute(
        "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s)",
        (name,)
    )

    existing = cur.fetchone()

    if existing is not None and not overwrite:
        print("Skipped:", name)
        return

    if existing is not None and overwrite:
        contact_id = existing[0]

        cur.execute(
            """
            UPDATE contacts
            SET email = %s, birthday = %s, group_id = %s
            WHERE id = %s
            """,
            (email, birthday, group_id, contact_id)
        )

        cur.execute(
            "DELETE FROM phones WHERE contact_id = %s",
            (contact_id,)
        )
    else:
        cur.execute(
            """
            INSERT INTO contacts (name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (name, email, birthday, group_id)
        )

        contact_id = cur.fetchone()[0]

    for phone_item in phones:
        phone = phone_item["phone"]
        phone_type = phone_item["type"]

        if phone_type in ("home", "work", "mobile"):
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, phone, phone_type)
            )

    print("Imported:", name)


def import_from_json():
    filename = input("JSON filename to read: ").strip()

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        name = item["name"]

        cur.execute(
            "SELECT id FROM contacts WHERE LOWER(name) = LOWER(%s)",
            (name,)
        )

        existing = cur.fetchone()
        overwrite = False

        if existing is not None:
            answer = input(f"{name} already exists. skip or overwrite? ").strip().lower()

            if answer == "overwrite":
                overwrite = True

        save_contact_from_json(cur, item, overwrite)

    conn.commit()
    cur.close()
    conn.close()

    print("JSON import finished.")


def import_from_csv():
    filename = input("CSV filename: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(BASE_DIR, filename), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row["name"].strip()
            email = row["email"].strip()
            birthday = row["birthday"].strip()
            group_name = row["group"].strip()
            phone = row["phone"].strip()
            phone_type = row["type"].strip()

            if phone_type not in ("home", "work", "mobile"):
                print("Skipped wrong phone type:", name)
                continue

            group_id = get_group_id(cur, group_name)

            cur.execute(
                """
                INSERT INTO contacts (name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (name, email, birthday, group_id)
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, phone, phone_type)
            )

    conn.commit()
    cur.close()
    conn.close()

    print("CSV import finished.")


def main():
    while True:
        print("\nPHONEBOOK MENU")
        print("1. Setup database")
        print("2. Add contact")
        print("3. Show all contacts")
        print("4. Filter by group")
        print("5. Search by name/email/group/phone")
        print("6. Search by email")
        print("7. Paginated contacts")
        print("8. Add phone to existing contact")
        print("9. Move contact to group")
        print("10. Export to JSON")
        print("11. Import from JSON")
        print("12. Import from CSV")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            setup_database()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            show_all_contacts()
        elif choice == "4":
            filter_by_group()
        elif choice == "5":
            search_contact()
        elif choice == "6":
            search_by_email()
        elif choice == "7":
            paginated_contacts()
        elif choice == "8":
            add_phone_to_contact()
        elif choice == "9":
            move_contact_to_group()
        elif choice == "10":
            export_to_json()
        elif choice == "11":
            import_from_json()
        elif choice == "12":
            import_from_csv()
        elif choice == "0":
            break
        else:
            print("Wrong choice.")


if __name__ == "__main__":
    main()