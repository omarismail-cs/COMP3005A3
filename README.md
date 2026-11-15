# PostgreSQL Student Database CRUD Application

A Python CLI application that connects to a PostgreSQL database to perform Create, Read, Update, and Delete (CRUD) operations on a `students` table.

## Video Demonstration
[Watch the Demo Video Here](https://youtu.be/UPHyk3TGE6k)

## Project Structure
- `db/schema.sql`: SQL script to create the `students` table and insert initial records.
- `app/main.py`: Python application implementing the database connection and CRUD functions.
- `requirements.txt`: Required Python packages.

## Prerequisites
- PostgreSQL and pgAdmin 4 installed
- Python 3.8 or higher

## Database Setup
1. Open pgAdmin 4 and create a database named `school_db`.
2. Open the Query Tool on `school_db` and run the contents of `db/schema.sql`.

## Application Setup & Execution
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your PostgreSQL credentials as environment variables (or edit the defaults in `get_connection()` in `app/main.py`):
   ```bash
   export DB_NAME=school_db
   export DB_USER=postgres
   export DB_PASSWORD=your_password
   export DB_HOST=localhost
   export DB_PORT=5432
   ```
   *(On Windows Command Prompt, use `set DB_PASSWORD=your_password` instead of `export`.)*
3. Run the application:
   ```bash
   python app/main.py
   ```

## Implemented Functions
- `getAllStudents()`: Queries and displays all student rows ordered by `student_id`.
- `addStudent(first_name, last_name, email, enrollment_date)`: Inserts a new student record and prints the generated `student_id`.
- `updateStudentEmail(student_id, new_email)`: Updates the email of the student matching `student_id`.
- `deleteStudent(student_id)`: Deletes the student record matching `student_id`.
