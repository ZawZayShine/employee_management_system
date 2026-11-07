from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re
from pathlib import Path

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "employees.db"

DEPARTMENTS = ["IT", "HR", "Finance", "Marketing", "Administration"]
GENDERS = ["Male", "Female", "Other"]


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Employee (
                employee_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                gender TEXT NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL CHECK (salary > 0),
                joining_date DATE NOT NULL
            )
        """)
        conn.commit()


def validate_employee(form):
    errors = []
    data = {
        "employee_id": form.get("employee_id", "").strip(),
        "full_name": form.get("full_name", "").strip(),
        "email": form.get("email", "").strip(),
        "phone": form.get("phone", "").strip(),
        "gender": form.get("gender", "").strip(),
        "department": form.get("department", "").strip(),
        "position": form.get("position", "").strip(),
        "salary": form.get("salary", "").strip(),
        "joining_date": form.get("joining_date", "").strip()
    }

    required = ["employee_id", "full_name", "email", "phone", "gender",
                "department", "position", "salary", "joining_date"]
    for field in required:
        if not data[field]:
            errors.append(f"{field.replace('_', ' ').title()} is required.")

    if data["email"] and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", data["email"]):
        errors.append("Please enter a valid email address.")

    if data["phone"]:
        digits = re.sub(r"\D", "", data["phone"])
        if not re.fullmatch(r"[0-9+\-\s()]+", data["phone"]) or not 7 <= len(digits) <= 15:
            errors.append("Phone number must contain 7 to 15 digits and only valid phone characters.")

    if data["gender"] and data["gender"] not in GENDERS:
        errors.append("Please select a valid gender.")

    if data["department"] and data["department"] not in DEPARTMENTS:
        errors.append("Please select a valid department.")

    if data["salary"]:
        try:
            salary = float(data["salary"])
            if salary <= 0:
                errors.append("Salary must be greater than zero.")
            data["salary"] = salary
        except ValueError:
            errors.append("Salary must be a valid number.")

    return data, errors


@app.route("/")
def home():
    with get_db_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM Employee").fetchone()[0]
    return render_template("index.html", total=total)


@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        data, errors = validate_employee(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("employee_form.html", employee=data,
                                   departments=DEPARTMENTS, genders=GENDERS,
                                   page_title="Add Employee", is_edit=False)

        try:
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO Employee
                    (employee_id, full_name, email, phone, gender, department,
                     position, salary, joining_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (data["employee_id"], data["full_name"], data["email"],
                      data["phone"], data["gender"], data["department"],
                      data["position"], data["salary"], data["joining_date"]))
                conn.commit()
            flash("Employee registered successfully.", "success")
            return redirect(url_for("view_employees"))
        except sqlite3.IntegrityError:
            flash("Employee ID already exists. Please use a unique ID.", "error")
            return render_template("employee_form.html", employee=data,
                                   departments=DEPARTMENTS, genders=GENDERS,
                                   page_title="Add Employee", is_edit=False)

    return render_template("employee_form.html", employee={}, departments=DEPARTMENTS,
                           genders=GENDERS, page_title="Add Employee", is_edit=False)


@app.route("/view_employees")
def view_employees():
    with get_db_connection() as conn:
        employees = conn.execute("SELECT * FROM Employee ORDER BY employee_id").fetchall()
    return render_template("view_employees.html", employees=employees)


@app.route("/edit_employee/<id>", methods=["GET", "POST"])
def edit_employee(id):
    with get_db_connection() as conn:
        employee = conn.execute("SELECT * FROM Employee WHERE employee_id = ?", (id,)).fetchone()

    if employee is None:
        flash("Employee record was not found.", "error")
        return redirect(url_for("view_employees"))

    if request.method == "POST":
        data, errors = validate_employee(request.form)
        if errors:
            for error in errors:
                flash(error, "error")
            data["employee_id"] = id
            return render_template("employee_form.html", employee=data,
                                   departments=DEPARTMENTS, genders=GENDERS,
                                   page_title="Edit Employee", is_edit=True)

        try:
            with get_db_connection() as conn:
                conn.execute("""
                    UPDATE Employee
                    SET full_name=?, email=?, phone=?, gender=?, department=?,
                        position=?, salary=?, joining_date=?
                    WHERE employee_id=?
                """, (data["full_name"], data["email"], data["phone"],
                      data["gender"], data["department"], data["position"],
                      data["salary"], data["joining_date"], id))
                conn.commit()
            flash("Employee information updated successfully.", "success")
            return redirect(url_for("view_employees"))
        except sqlite3.Error:
            flash("Unable to update employee. Please try again.", "error")

    return render_template("employee_form.html", employee=employee,
                           departments=DEPARTMENTS, genders=GENDERS,
                           page_title="Edit Employee", is_edit=True)


@app.route("/delete_employee/<id>", methods=["POST"])
def delete_employee(id):
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM Employee WHERE employee_id = ?", (id,))
        conn.commit()
    if cursor.rowcount:
        flash("Employee deleted successfully.", "success")
    else:
        flash("Employee record was not found.", "error")
    return redirect(url_for("view_employees"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)