import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# ================= DATABASE =================
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# ================= LOGIN CHECK =================
def login():
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
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
    main.geometry("600x500")

    # ---------- FUNCTIONS ----------
    def add_student():
        name = name_entry.get()
        age = age_entry.get()
        course = course_entry.get()
        if name == "" or age == "" or course == "":
            messagebox.showerror("Error", "All fields required")
            return
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
        conn.commit()
        messagebox.showinfo("Success", "Student Added")
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        course_entry.delete(0, tk.END)
        view_students()

    def view_students():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM students")
        for student in cursor.fetchall():
            tree.insert("", tk.END, values=student)

    def delete_student():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a student from table")
            return
        student_id = tree.item(selected[0])['values'][0]
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        messagebox.showinfo("Success", "Student Deleted")
        view_students()

    def update_student():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a student from table")
            return
        student = tree.item(selected[0])['values']
        # Popup window
        win = tk.Toplevel()
        win.title("Update Student")
        tk.Label(win, text="Name").pack()
        new_name = tk.Entry(win)
        new_name.insert(0, student[1])
        new_name.pack()
        tk.Label(win, text="Age").pack()
        new_age = tk.Entry(win)
        new_age.insert(0, student[2])
        new_age.pack()
        tk.Label(win, text="Course").pack()
        new_course = tk.Entry(win)
        new_course.insert(0, student[3])
        new_course.pack()

        def save_update():
            cursor.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                           (new_name.get(), new_age.get(), new_course.get(), student[0]))
            conn.commit()
            messagebox.showinfo("Success", "Student Updated")
            win.destroy()
            view_students()

        tk.Button(win, text="Save", command=save_update).pack(pady=5)

    def logout():
        main.destroy()
        start_login_window()

    # ---------- UI ----------
    frame = tk.Frame(main)
    frame.pack(pady=10)

    tk.Label(frame, text="Name").grid(row=0, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1)

    tk.Label(frame, text="Age").grid(row=1, column=0)
    age_entry = tk.Entry(frame)
    age_entry.grid(row=1, column=1)

    tk.Label(frame, text="Course").grid(row=2, column=0)
    course_entry = tk.Entry(frame)
    course_entry.grid(row=2, column=1)

    tk.Button(frame, text="Add Student", command=add_student).grid(row=3, column=0, pady=5)
    tk.Button(frame, text="Update Selected", command=update_student).grid(row=3, column=1)
    tk.Button(frame, text="Delete Selected", command=delete_student).grid(row=3, column=2)
    tk.Button(frame, text="Logout", command=logout).grid(row=3, column=3)

    # Table
    columns = ("ID", "Name", "Age", "Course")
    tree = ttk.Treeview(main, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=20)
    view_students()

    main.mainloop()


# ================= LOGIN WINDOW =================
def start_login_window():
    global login_window, username_entry, password_entry
    login_window = tk.Tk()
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=login).pack(pady=10)

    login_window.mainloop()


# ================= START APP =================
start_login_window()
conn.close()