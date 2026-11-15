import os
import psycopg2
from psycopg2 import Error


# Connects to school_db. The password comes from DB_PASSWORD so it is not saved in this file.
def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "school_db"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "your_password_here"),
    )


# Reads every student and prints the rows, ordered by student_id.
def getAllStudents():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT student_id, first_name, last_name, email, enrollment_date
            FROM students
            ORDER BY student_id
        """)
        rows = cur.fetchall()
        cur.close()

        if len(rows) == 0:
            print("No students found.")
            return

        print("ID | First Name | Last Name | Email | Enrollment Date")
        for row in rows:
            student_id = row[0]
            first_name = row[1]
            last_name = row[2]
            email = row[3]
            enrollment_date = row[4]
            print(student_id, "|", first_name, "|", last_name, "|", email, "|", enrollment_date)

    except Error as e:
        print("Error getting students:", e)
    finally:
        if conn is not None:
            conn.close()


# Inserts one student and prints the new student_id.
# The %s placeholders are filled from the values tuple, not by joining text into the SQL.
def addStudent(first_name, last_name, email, enrollment_date):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id
            """,
            (first_name, last_name, email, enrollment_date),
        )

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        print("Added student with id", new_id)

    except Error as e:
        if conn is not None:
            conn.rollback()
        print("Error adding student:", e)
    finally:
        if conn is not None:
            conn.close()


# Sets a new email for one student_id. If that id is missing, nothing is changed.
def updateStudentEmail(student_id, new_email):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE students SET email = %s WHERE student_id = %s",
            (new_email, student_id),
        )

        if cur.rowcount == 0:
            print("No student found with id", student_id)
        else:
            conn.commit()
            print("Updated email for student", student_id)

        cur.close()

    except Error as e:
        if conn is not None:
            conn.rollback()
        print("Error updating email:", e)
    finally:
        if conn is not None:
            conn.close()


# Deletes the student with this student_id. If that id is missing, nothing is changed.
def deleteStudent(student_id):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM students WHERE student_id = %s",
            (student_id,),
        )

        if cur.rowcount == 0:
            print("No student found with id", student_id)
        else:
            conn.commit()
            print("Deleted student", student_id)

        cur.close()

    except Error as e:
        if conn is not None:
            conn.rollback()
        print("Error deleting student:", e)
    finally:
        if conn is not None:
            conn.close()


# Asks for a menu choice and calls one function. Repeats until the user exits.
def main():
    while True:
        print()
        print("1. Show all students")
        print("2. Add a student")
        print("3. Update a student email")
        print("4. Delete a student")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            getAllStudents()

        elif choice == "2":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(first_name, last_name, email, enrollment_date)

        elif choice == "3":
            id_text = input("Student id: ").strip()
            try:
                student_id = int(id_text)
            except ValueError:
                print("Student id must be a number.")
                continue

            new_email = input("New email: ").strip()
            updateStudentEmail(student_id, new_email)

        elif choice == "4":
            id_text = input("Student id: ").strip()
            try:
                student_id = int(id_text)
            except ValueError:
                print("Student id must be a number.")
                continue

            deleteStudent(student_id)

        elif choice == "5":
            break

        else:
            print("Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
