import sqlite3
import tkinter as tk
from tkinter import messagebox

# ================= DATABASE =================
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# ================= FUNCTIONS =================

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showerror("Error", "All fields required")
        return

    cursor.execute(
        "INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
        (name, age, course)
    )
    conn.commit()

    messagebox.showinfo("Success", "Student Added")

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    output.delete("1.0", tk.END)

    for student in students:
        output.insert(tk.END, str(student) + "\n")


def delete_student():
    student_id = id_entry.get()

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()

    messagebox.showinfo("Success", "Student Deleted")


# ================= GUI WINDOW =================

root = tk.Tk()
root.title("Student Management System")
root.geometry("500x500")

# Labels + Entries
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Course").pack()
course_entry = tk.Entry(root)
course_entry.pack()

tk.Label(root, text="Student ID (for Delete)").pack()
id_entry = tk.Entry(root)
id_entry.pack()

# Buttons
tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="View Students", command=view_students).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)

# Output Box
output = tk.Text(root, height=10)
output.pack()

# Run App
root.mainloop()

conn.close()