# Student Management System (Web Version)

This is a **Student Management System** built using **Python Flask** and **SQLite**, based on a previously created Tkinter GUI desktop application.  
It allows administrators to **manage student records** through a web browser, with functionality similar to the original desktop version.

---

## **Features**

- **Admin Login:** Secure login system using the `admin` table in SQLite.
- **Add Students:** Add new students with `name`, `age`, and `course`.
- **View Students:** Display all students in a table format.
- **Update Students:** Edit existing student details.
- **Delete Students:** Remove students from the database.
- **Logout:** Return to the login page.
- **Inline Web Pages:** All pages are generated dynamically in Flask (no separate HTML templates required).

---

## **How It Works**

- The **Flask app** is contained in a single Python file: `student_web_inline.py`.
- The app uses **SQLite (`students.db`)** to store admin credentials and student records.
- Routes and functionality:

1. **Login (`/`)**  
   - Handles GET (show login form) and POST (verify credentials).  
   - Redirects to dashboard on successful login.

2. **Dashboard (`/dashboard`)**  
   - Displays a table of all students.  
   - Provides a form to add a new student.  
   - Includes links to update or delete each student.

3. **Add Student (`/add`)**  
   - Handles form submission from the dashboard.  
   - Inserts a new student into the `students` table.

4. **Delete Student (`/delete/<id>`)**  
   - Deletes a student by ID.

5. **Update Student (`/update/<id>`)**  
   - GET: Displays a form pre-filled with the student’s current info.  
   - POST: Saves the updated student information.

---

## **Getting Started**

1. **Clone the repository:**

```bash
git clone https://github.com/YourUsername/student-management-web.git
cd student-management-web
