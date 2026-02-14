import sqlite3

print("System starting...")

# ================= DATABASE SETUP =================
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# ---------- Students Table ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT
)
""")

# ---------- Admin Table ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()

# ---------- Default Admin ----------
cursor.execute("SELECT * FROM admin WHERE username = ?", ("admin",))
admin_exists = cursor.fetchone()

if not admin_exists:
    cursor.execute(
        "INSERT INTO admin (username, password) VALUES (?, ?)",
        ("admin", "1234")
    )
    conn.commit()


# ================= FUNCTIONS =================

def add_student():
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    course = input("Enter student course: ")

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()
    print("✅ Student added successfully")


def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n--- Student List ---")
    for student in students:
        print(student)


def search_student():
    name = input("Enter name to search: ")

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + name + '%',)
    )

    results = cursor.fetchall()

    if results:
        for student in results:
            print(student)
    else:
        print("❌ Student not found")


def delete_student():
    student_id = input("Enter student ID to delete: ")

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    conn.commit()

    print("🗑 Student deleted (if ID existed)")


def update_student():
    student_id = input("Enter student ID to update: ")

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if student:
        print("Current Details:", student)

        new_name = input("Enter new name (leave blank to keep same): ")
        new_age = input("Enter new age (leave blank to keep same): ")
        new_course = input("Enter new course (leave blank to keep same): ")

        if new_name == "":
            new_name = student[1]
        if new_age == "":
            new_age = student[2]
        if new_course == "":
            new_course = student[3]

        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, course = ?
            WHERE id = ?
        """, (new_name, new_age, new_course, student_id))

        conn.commit()
        print("✅ Student updated successfully")

    else:
        print("❌ Student not found")


def register_admin():
    print("\n===== REGISTER NEW ADMIN =====")

    username = input("Enter new username: ")
    password = input("Enter new password: ")

    try:
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        print("✅ New admin created successfully")

    except sqlite3.IntegrityError:
        print("❌ Username already exists")


def login():
    print("\n===== LOGIN =====")

    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute(
        "SELECT * FROM admin WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        print("✅ Login successful")
        return True
    else:
        print("❌ Invalid login")
        return False


# ================= MENU =================

def menu():
    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Delete Student")
        print("5. Update Student")
        print("6. Register New Admin")
        print("7. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            update_student()
        elif choice == "6":
            register_admin()
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice")


# ================= RUN PROGRAM =================

if __name__ == "__main__":
    while True:
        if login():
            menu()
        else:
            print("Try again\n")