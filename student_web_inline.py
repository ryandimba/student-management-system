from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)
DB = "students.db"

# ================= HELPER FUNCTIONS =================
def get_students():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect("/dashboard")
        else:
            error = "<p style='color:red;'>Invalid login</p>"
    return f"""
    <h2>Admin Login</h2>
    <form method='POST'>
        Username: <input type='text' name='username'><br>
        Password: <input type='password' name='password'><br>
        <input type='submit' value='Login'>
    </form>
    {error}
    """

# ================= DASHBOARD =================
@app.route("/dashboard", methods=["GET"])
def dashboard():
    students = get_students()
    student_rows = ""
    for s in students:
        student_rows += f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td>" \
                        f"<td><a href='/update/{s[0]}'>Update</a> | <a href='/delete/{s[0]}'>Delete</a></td></tr>"
    return f"""
    <h2>Student Dashboard</h2>
    <form method='POST' action='/add'>
        Name: <input type='text' name='name'>
        Age: <input type='number' name='age'>
        Course: <input type='text' name='course'>
        <input type='submit' value='Add Student'>
    </form>
    <br>
    <table border='1'>
    <tr><th>ID</th><th>Name</th><th>Age</th><th>Course</th><th>Actions</th></tr>
    {student_rows}
    </table>
    <br>
    <a href='/'>Logout</a>
    """

# ================= ADD STUDENT =================
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name")
    age = request.form.get("age")
    course = request.form.get("course")
    if name and age and course:
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
        conn.commit()
        conn.close()
    return redirect("/dashboard")

# ================= DELETE STUDENT =================
@app.route("/delete/<int:id>")
def delete_student(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ================= UPDATE STUDENT =================
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        course = request.form.get("course")
        cursor.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?", (name, age, course, id))
        conn.commit()
        conn.close()
        return redirect("/dashboard")
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return f"""
    <h2>Update Student</h2>
    <form method='POST'>
        Name: <input type='text' name='name' value='{student[1]}'><br>
        Age: <input type='number' name='age' value='{student[2]}'><br>
        Course: <input type='text' name='course' value='{student[3]}'><br>
        <input type='submit' value='Save'>
    </form>
    <br>
    <a href='/dashboard'>Back</a>
    """

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)