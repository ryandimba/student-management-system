print("sytem starting...")
import sqlite3
from tkinter import Menu

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS students (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   age INTEGER,
                   course TEXT
                   )                  
               """)
conn.commit()

def add_student():
    name = input("Enter student name: ")
    age = input("Enter student age: ")
    course = input("Enter student course: ")
    
    cursor.execute(
        "INSERT INTO STUDENTS (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()
    print("student added successfully!")

def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("\n--- students Lists ---")
    for student in students:
        print(student)

def search_student():
    name = input("Enter student name to search: ")
    
    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + name + '%',)
    )
    results = cursor.fetchall()
    if results:
        for student in results:
            print(student)
    else:
        print("Student not found.")

def delete_student():
    student_id = input("Enter student ID to delete: ")
    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    conn.commit()
    print("student deleted (if ID existed)")
                 
def main():
    while True:
        print("\n---- student management system ----")
        print("1. Add student")
        print("2. View students")
        print("3. Search student")
        print("4. Delete student")
        print("5. Exit")
        
        choice = input("Choose option: ")
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")
            
            
if __name__ == "__main__":
    print("starting menu now...")     
    main()
conn.close()

                         
      
