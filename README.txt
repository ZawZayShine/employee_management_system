EMPLOYEE  MANAGEMENT SYSTEM - FLASK

1. REQUIREMENTS
- Python 3.9 or later
- Flask
- SQLite (included with Python)

2. PROJECT STRUCTURE
employee_management_system/
    app.py
    employees.db             (created automatically on first run)
    requirements.txt
    templates/
        base.html
        index.html
        employee_form.html
        view_employees.html
    static/
        css/
            style.css

3. HOW TO RUN
Open a terminal in this project folder and run:

    python -m venv venv

Windows:
    venv\Scripts\activate

Install Flask:
    pip install -r requirements.txt

Start the application:
    python app.py

Open this address in a browser:
    http://127.0.0.1:5000/

The SQLite database and Employee table are created automatically when app.py is run.

4. FLASK ROUTES
- GET / : Home page and employee count.
- GET, POST /add_employee : Display and process the registration form.
- GET /view_employees : Display all employees.
- GET, POST /edit_employee/<id> : Display and save changes to one employee.
- POST /delete_employee/<id> : Delete an employee.

5. SYSTEM ARCHITECTURE / SHORT REPORT
The system uses a three-part structure. The presentation layer consists of HTML templates
and CSS. The application layer is written in Python using Flask. It receives browser
requests, validates submitted data, runs the required operation and selects a template
to display the result. The data layer uses SQLite to store employee records in the
Employee table.

When an administrator opens a page, the browser sends an HTTP GET request to Flask.
Flask runs the matching route and returns an HTML page. When the administrator submits
the registration or edit form, the browser sends a POST request. Flask reads the submitted
values from request.form, checks required fields and validates email, phone number,
department, gender and salary. Valid information is stored using SQL INSERT or UPDATE.
The employee list is retrieved using SELECT. A delete request uses SQL DELETE.

SQL queries use placeholders (?) and parameter values to reduce SQL injection risk.
The employee_id column is the primary key, so duplicate employee IDs are rejected.
Flash messages show success and validation/error feedback to the administrator.

6. TESTING CHECKLIST
- Register an employee using valid details: should save successfully.
- Submit the form with a required field missing: should show a validation message.
- Register an existing Employee ID: should show a duplicate ID error.
- Edit an employee and save: the updated details should appear in the list.
- Delete an employee: the record should disappear from the list.
- Open View Employees: all saved records should be displayed.

7. SCREENSHOTS FOR SUBMISSION
Run the application in a browser and capture these screenshots:
- Home page
- Employee registration form
- Employee list showing at least one record
- Edit employee form
- Successful registration or update message
- Validation error (for example, submit an empty form)
- Duplicate Employee ID error

Use Windows Snipping Tool (Win + Shift + S) to capture screenshots.
Save them in a folder named screenshots before submitting.
