import sqlite3
import tkinter as tk
from tkinter import messagebox

# ================= DATABASE =================
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# ================= LOGIN CHECK =================
def check_login():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute(
        "SELECT * FROM admin WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login Successful")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Invalid Login")

# ================= MAIN WINDOW =================
def open_main_window():
    main = tk.Tk()
    main.title("Student Management System")
    main.geometry("500x500")

    # ---------- FUNCTIONS ----------
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
        if student_id == "":
            messagebox.showerror("Error", "Enter ID")
            return
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student Deleted")
        id_entry.delete(0, tk.END)

    # ---------- UI ----------
    tk.Label(main, text="Name").pack()
    name_entry = tk.Entry(main)
    name_entry.pack()

    tk.Label(main, text="Age").pack()
    age_entry = tk.Entry(main)
    age_entry.pack()

    tk.Label(main, text="Course").pack()
    course_entry = tk.Entry(main)
    course_entry.pack()

    tk.Label(main, text="Student ID (Delete)").pack()
    id_entry = tk.Entry(main)
    id_entry.pack()

    tk.Button(main, text="Add Student", command=add_student).pack(pady=5)
    tk.Button(main, text="View Students", command=view_students).pack(pady=5)
    tk.Button(main, text="Delete Student", command=delete_student).pack(pady=5)

    output = tk.Text(main, height=10)
    output.pack()

    main.mainloop()

# ================= LOGIN WINDOW =================
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

login_window.mainloop()
conn.close()