"""
SQLite database module for the School Management System.

This module provides a PyQt5 graphical interface connected to an SQLite
database. It supports managing students, instructors, courses, enrollments,
and instructor assignments. It also provides searching, editing, deleting,
database backup, and database restore functionality.
"""
import sys
import sqlite3
import shutil
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QMessageBox, QComboBox, QHeaderView
)


DATABASE = "school.db"

def connect_database():
    """
    Connect to the School Management System SQLite database.

    :return: Connection to the SQLite database.
    :rtype: sqlite3.Connection
    """
    return sqlite3.connect(DATABASE)


def create_database():
    """
    Create the required database tables if they do not already exist.

    The database contains tables for students, instructors, courses,
    and student enrollments.
    """
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            instructor_id TEXT,
            FOREIGN KEY (instructor_id)
                REFERENCES instructors(instructor_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id TEXT,
            course_id TEXT,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id)
                REFERENCES students(student_id),
            FOREIGN KEY (course_id)
                REFERENCES courses(course_id)
        )
    """)

    conn.commit()
    conn.close()



class DatabaseApp(QMainWindow):
    """
    Main window for the database-based School Management System.

    This class provides a PyQt5 interface for interacting with the SQLite
    database, including adding, editing, deleting, searching, registering,
    assigning, backing up, and restoring school records.
    """

    def __init__(self):
        """Initialize the database application and graphical interface."""
        super().__init__()

        create_database()

        self.setWindowTitle(
            "School Management System - Database"
        )
        self.resize(1150, 800)

        self.editing_type = None
        self.editing_id = None

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        
        title = QLabel(
            "School Management System - SQLite Database"
        )
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )
        main_layout.addWidget(title)

        forms_layout = QHBoxLayout()

        student_group = QGroupBox("Student")
        student_form = QFormLayout()

        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        student_form.addRow(
            "Name:",
            self.student_name
        )
        student_form.addRow(
            "Age:",
            self.student_age
        )
        student_form.addRow(
            "Email:",
            self.student_email
        )
        student_form.addRow(
            "Student ID:",
            self.student_id
        )

        add_student_btn = QPushButton(
            "Add Student"
        )
        add_student_btn.clicked.connect(
            self.add_student
        )

        student_form.addRow(add_student_btn)

        student_group.setLayout(student_form)
        forms_layout.addWidget(student_group)


        instructor_group = QGroupBox("Instructor")
        instructor_form = QFormLayout()

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        instructor_form.addRow(
            "Name:",
            self.instructor_name
        )
        instructor_form.addRow(
            "Age:",
            self.instructor_age
        )
        instructor_form.addRow(
            "Email:",
            self.instructor_email
        )
        instructor_form.addRow(
            "Instructor ID:",
            self.instructor_id
        )

        add_instructor_btn = QPushButton(
            "Add Instructor"
        )
        add_instructor_btn.clicked.connect(
            self.add_instructor
        )

        instructor_form.addRow(
            add_instructor_btn
        )

        instructor_group.setLayout(
            instructor_form
        )
        forms_layout.addWidget(
            instructor_group
        )

        course_group = QGroupBox("Course")
        course_form = QFormLayout()

        self.course_id = QLineEdit()
        self.course_name = QLineEdit()

        course_form.addRow(
            "Course ID:",
            self.course_id
        )
        course_form.addRow(
            "Course Name:",
            self.course_name
        )

        add_course_btn = QPushButton(
            "Add Course"
        )
        add_course_btn.clicked.connect(
            self.add_course
        )

        course_form.addRow(add_course_btn)

        course_group.setLayout(course_form)
        forms_layout.addWidget(course_group)

        main_layout.addLayout(forms_layout)


        registration_group = QGroupBox(
            "Student Registration"
        )

        registration_layout = QHBoxLayout()

        self.student_combo = QComboBox()
        self.course_combo = QComboBox()

        register_btn = QPushButton(
            "Register Student"
        )
        register_btn.clicked.connect(
            self.register_student
        )

        registration_layout.addWidget(
            QLabel("Student:")
        )
        registration_layout.addWidget(
            self.student_combo
        )

        registration_layout.addWidget(
            QLabel("Course:")
        )
        registration_layout.addWidget(
            self.course_combo
        )

        registration_layout.addWidget(
            register_btn
        )

        registration_group.setLayout(
            registration_layout
        )

        main_layout.addWidget(
            registration_group
        )

        assignment_group = QGroupBox(
            "Instructor Assignment"
        )

        assignment_layout = QHBoxLayout()

        self.instructor_combo = QComboBox()
        self.assignment_course_combo = QComboBox()

        assign_btn = QPushButton(
            "Assign Instructor"
        )
        assign_btn.clicked.connect(
            self.assign_instructor
        )

        assignment_layout.addWidget(
            QLabel("Instructor:")
        )
        assignment_layout.addWidget(
            self.instructor_combo
        )

        assignment_layout.addWidget(
            QLabel("Course:")
        )
        assignment_layout.addWidget(
            self.assignment_course_combo
        )

        assignment_layout.addWidget(
            assign_btn
        )

        assignment_group.setLayout(
            assignment_layout
        )

        main_layout.addWidget(
            assignment_group
        )

        search_layout = QHBoxLayout()

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText(
            "Search by name, ID, or course..."
        )

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(
            self.search_records
        )

        clear_search_btn = QPushButton(
            "Clear"
        )
        clear_search_btn.clicked.connect(
            self.load_records
        )

        search_layout.addWidget(
            QLabel("Search:")
        )
        search_layout.addWidget(
            self.search_entry
        )
        search_layout.addWidget(
            search_btn
        )
        search_layout.addWidget(
            clear_search_btn
        )

        main_layout.addLayout(
            search_layout
        )

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "Type",
            "ID",
            "Name / Course",
            "Email"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        main_layout.addWidget(self.table)

        buttons_layout = QHBoxLayout()

        edit_btn = QPushButton(
            "Edit Selected"
        )
        edit_btn.clicked.connect(
            self.edit_record
        )

        save_changes_btn = QPushButton(
            "Save Changes"
        )
        save_changes_btn.clicked.connect(
            self.save_changes
        )

        delete_btn = QPushButton(
            "Delete Selected"
        )
        delete_btn.clicked.connect(
            self.delete_record
        )

        backup_btn = QPushButton(
            "Backup Database"
        )
        backup_btn.clicked.connect(
            self.backup_database
        )

        restore_btn = QPushButton(
            "Restore Database"
        )
        restore_btn.clicked.connect(
            self.restore_database
        )

        buttons_layout.addWidget(
            edit_btn
        )
        buttons_layout.addWidget(
            save_changes_btn
        )
        buttons_layout.addWidget(
            delete_btn
        )
        buttons_layout.addWidget(
            backup_btn
        )
        buttons_layout.addWidget(
            restore_btn
        )

        main_layout.addLayout(
            buttons_layout
        )

        self.load_records()
        self.update_dropdowns()

def validate_person(self, name, age_text, email):
        """
        Validate a person's name, age, and email address.

        :param name: Person's name.
        :param age_text: Person's age entered as text.
        :param email: Person's email address.
        :return: Validated age as an integer.
        :rtype: int
        :raises ValueError: If any entered information is invalid.
        """

        if not name.replace(" ", "").isalpha():
            raise ValueError(
                "Name must contain letters only."
            )

        if not age_text:
            raise ValueError(
                "Age cannot be empty."
            )

        age = int(age_text)

        if age < 0:
            raise ValueError(
                "Age cannot be negative."
            )

        if "@" not in email or "." not in email:
            raise ValueError(
                "Invalid email format."
            )

        return age

def add_student(self):
        """Validate and add a new student to the database."""

        try:
            name = (
                self.student_name.text().strip()
            )
            age_text = (
                self.student_age.text().strip()
            )
            email = (
                self.student_email.text().strip()
            )
            student_id = (
                self.student_id.text().strip()
            )

            age = self.validate_person(
                name,
                age_text,
                email
            )

            if not student_id.isdigit():
                raise ValueError(
                    "Student ID must contain numbers only."
                )

            conn = connect_database()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO students
                (student_id, name, age, email)
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    name,
                    age,
                    email
                )
            )

            conn.commit()
            conn.close()

            self.clear_student()
            self.load_records()
            self.update_dropdowns()

            QMessageBox.information(
                self,
                "Success",
                "Student added to database!"
            )

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Error",
                "Student ID already exists."
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Input Error",
                str(error)
            )

def add_instructor(self):
        """Validate and add a new instructor to the database."""

        try:
            name = (
                self.instructor_name.text().strip()
            )
            age_text = (
                self.instructor_age.text().strip()
            )
            email = (
                self.instructor_email.text().strip()
            )
            instructor_id = (
                self.instructor_id.text().strip()
            )

            age = self.validate_person(
                name,
                age_text,
                email
            )

            if not instructor_id:
                raise ValueError(
                    "Instructor ID cannot be empty."
                )

            conn = connect_database()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO instructors
                (instructor_id, name, age, email)
                VALUES (?, ?, ?, ?)
                """,
                (
                    instructor_id,
                    name,
                    age,
                    email
                )
            )

            conn.commit()
            conn.close()

            self.clear_instructor()
            self.load_records()
            self.update_dropdowns()

            QMessageBox.information(
                self,
                "Success",
                "Instructor added to database!"
            )

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Error",
                "Instructor ID already exists."
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Input Error",
                str(error)
            )

def add_course(self):
        """Add a new course to the database."""

        course_id = (
            self.course_id.text().strip()
        )
        course_name = (
            self.course_name.text().strip()
        )

        if not course_id or not course_name:
            QMessageBox.warning(
                self,
                "Error",
                "Course ID and Course Name cannot be empty."
            )
            return

        try:
            conn = connect_database()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO courses
                (course_id, course_name)
                VALUES (?, ?)
                """,
                (
                    course_id,
                    course_name
                )
            )

            conn.commit()
            conn.close()

            self.clear_course()
            self.load_records()
            self.update_dropdowns()

            QMessageBox.information(
                self,
                "Success",
                "Course added to database!"
            )

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Error",
                "Course ID already exists."
            )

def load_records(self):
        """Load all student, instructor, and course records from the database."""

        self.table.setRowCount(0)

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT student_id, name, email FROM students"
        )

        for student_id, name, email in cursor.fetchall():
            self.add_row(
                "Student",
                student_id,
                name,
                email
            )

        cursor.execute(
            """
            SELECT instructor_id, name, email
            FROM instructors
            """
        )

        for instructor_id, name, email in cursor.fetchall():
            self.add_row(
                "Instructor",
                instructor_id,
                name,
                email
            )

        cursor.execute(
            """
            SELECT course_id, course_name
            FROM courses
            """
        )

        for course_id, course_name in cursor.fetchall():
            self.add_row(
                "Course",
                course_id,
                course_name,
                "-"
            )

        conn.close()

def add_row(
    self,
    record_type,
    record_id,
    name,
    email
):
        """
        Add a database record to the records table.

        :param record_type: Type of record being displayed.
        :param record_id: ID of the record.
        :param name: Name of the person or course.
        :param email: Email associated with the record.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)

        values = [
            record_type,
            record_id,
            name,
            email
        ]

        for column, value in enumerate(values):
            self.table.setItem(
                row,
                column,
                QTableWidgetItem(
                    str(value)
                )
            )

def update_dropdowns(self):
        """Update student, instructor, and course dropdown menus from the database."""

        self.student_combo.clear()
        self.course_combo.clear()
        self.instructor_combo.clear()
        self.assignment_course_combo.clear()

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT student_id FROM students"
        )

        self.student_combo.addItems(
            [
                row[0]
                for row in cursor.fetchall()
            ]
        )

        cursor.execute(
            "SELECT instructor_id FROM instructors"
        )

        self.instructor_combo.addItems(
            [
                row[0]
                for row in cursor.fetchall()
            ]
        )

        cursor.execute(
            "SELECT course_id FROM courses"
        )

        courses = [
            row[0]
            for row in cursor.fetchall()
        ]

        self.course_combo.addItems(courses)
        self.assignment_course_combo.addItems(
            courses
        )

        conn.close()

def register_student(self):
        """Register the selected student in the selected course."""

        student_id = (
            self.student_combo.currentText()
        )
        course_id = (
            self.course_combo.currentText()
        )

        if not student_id or not course_id:
            QMessageBox.warning(
                self,
                "Error",
                "Select a student and course."
            )
            return

        try:
            conn = connect_database()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO enrollments
                (student_id, course_id)
                VALUES (?, ?)
                """,
                (
                    student_id,
                    course_id
                )
            )

            conn.commit()
            conn.close()

            QMessageBox.information(
                self,
                "Success",
                "Student registered successfully!"
            )

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Error",
                "Student is already registered."
            )

def assign_instructor(self):
        """Assign the selected instructor to the selected course."""

        instructor_id = (
            self.instructor_combo.currentText()
        )

        course_id = (
            self.assignment_course_combo.currentText()
        )

        if not instructor_id or not course_id:
            QMessageBox.warning(
                self,
                "Error",
                "Select an instructor and course."
            )
            return

        conn = connect_database()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE courses
            SET instructor_id = ?
            WHERE course_id = ?
            """,
            (
                instructor_id,
                course_id
            )
        )

        conn.commit()
        conn.close()

        QMessageBox.information(
            self,
            "Success",
            "Instructor assigned successfully!"
        )

def search_records(self):
        """Search the displayed database records using the entered text."""

        text = (
            self.search_entry.text()
            .strip()
            .lower()
        )

        self.load_records()

        if not text:
            return

        for row in reversed(
            range(self.table.rowCount())
        ):

            row_text = " ".join(
                self.table.item(
                    row,
                    column
                ).text().lower()
                for column in range(
                    self.table.columnCount()
                )
            )

            if text not in row_text:
                self.table.removeRow(row)

def delete_record(self):
        """Delete the selected record and its related database information."""

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select a record to delete."
            )
            return

        record_type = (
            self.table.item(row, 0).text()
        )
        record_id = (
            self.table.item(row, 1).text()
        )

        conn = connect_database()
        cursor = conn.cursor()

        if record_type == "Student":

            cursor.execute(
                """
                DELETE FROM enrollments
                WHERE student_id = ?
                """,
                (record_id,)
            )

            cursor.execute(
                """
                DELETE FROM students
                WHERE student_id = ?
                """,
                (record_id,)
            )

        elif record_type == "Instructor":

            cursor.execute(
                """
                UPDATE courses
                SET instructor_id = NULL
                WHERE instructor_id = ?
                """,
                (record_id,)
            )

            cursor.execute(
                """
                DELETE FROM instructors
                WHERE instructor_id = ?
                """,
                (record_id,)
            )

        elif record_type == "Course":

            cursor.execute(
                """
                DELETE FROM enrollments
                WHERE course_id = ?
                """,
                (record_id,)
            )

            cursor.execute(
                """
                DELETE FROM courses
                WHERE course_id = ?
                """,
                (record_id,)
            )

        conn.commit()
        conn.close()

        self.load_records()
        self.update_dropdowns()

        QMessageBox.information(
            self,
            "Success",
            "Record deleted successfully!"
        )

def edit_record(self):
        """Load the selected database record into its form for editing."""

        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Select a record to edit."
            )
            return

        self.editing_type = (
            self.table.item(row, 0).text()
        )

        self.editing_id = (
            self.table.item(row, 1).text()
        )

        conn = connect_database()
        cursor = conn.cursor()

        if self.editing_type == "Student":

            cursor.execute(
                """
                SELECT name, age, email, student_id
                FROM students
                WHERE student_id = ?
                """,
                (self.editing_id,)
            )

            result = cursor.fetchone()

            if result:
                name, age, email, student_id = result

                self.student_name.setText(name)
                self.student_age.setText(str(age))
                self.student_email.setText(email)
                self.student_id.setText(student_id)

        elif self.editing_type == "Instructor":

            cursor.execute(
                """
                SELECT name, age, email, instructor_id
                FROM instructors
                WHERE instructor_id = ?
                """,
                (self.editing_id,)
            )

            result = cursor.fetchone()

            if result:
                name, age, email, instructor_id = result

                self.instructor_name.setText(name)
                self.instructor_age.setText(str(age))
                self.instructor_email.setText(email)
                self.instructor_id.setText(instructor_id)

        elif self.editing_type == "Course":

            cursor.execute(
                """
                SELECT course_id, course_name
                FROM courses
                WHERE course_id = ?
                """,
                (self.editing_id,)
            )

            result = cursor.fetchone()

            if result:
                course_id, course_name = result

                self.course_id.setText(course_id)
                self.course_name.setText(course_name)

        conn.close()

        QMessageBox.information(
            self,
            "Edit",
            "Modify the form and click Save Changes."
        )

def save_changes(self):
        """Validate and save changes made to the selected database record."""

        if not self.editing_type:
            QMessageBox.warning(
                self,
                "Error",
                "Select a record to edit first."
            )
            return

        try:
            conn = connect_database()
            cursor = conn.cursor()

            if self.editing_type == "Student":

                name = self.student_name.text().strip()
                age_text = self.student_age.text().strip()
                email = self.student_email.text().strip()
                new_id = self.student_id.text().strip()

                age = self.validate_person(
                    name,
                    age_text,
                    email
                )

                if not new_id.isdigit():
                    raise ValueError(
                        "Student ID must contain numbers only."
                    )

                cursor.execute(
                    """
                    UPDATE students
                    SET name = ?, age = ?, email = ?,
                        student_id = ?
                    WHERE student_id = ?
                    """,
                    (
                        name,
                        age,
                        email,
                        new_id,
                        self.editing_id
                    )
                )

                self.clear_student()

            elif self.editing_type == "Instructor":

                name = self.instructor_name.text().strip()
                age_text = self.instructor_age.text().strip()
                email = self.instructor_email.text().strip()
                new_id = self.instructor_id.text().strip()

                age = self.validate_person(
                    name,
                    age_text,
                    email
                )

                if not new_id:
                    raise ValueError(
                        "Instructor ID cannot be empty."
                    )

                cursor.execute(
                    """
                    UPDATE instructors
                    SET name = ?, age = ?, email = ?,
                        instructor_id = ?
                    WHERE instructor_id = ?
                    """,
                    (
                        name,
                        age,
                        email,
                        new_id,
                        self.editing_id
                    )
                )

                self.clear_instructor()

            elif self.editing_type == "Course":

                new_id = self.course_id.text().strip()
                name = self.course_name.text().strip()

                if not new_id or not name:
                    raise ValueError(
                        "Course ID and Course Name cannot be empty."
                    )

                cursor.execute(
                    """
                    UPDATE courses
                    SET course_id = ?, course_name = ?
                    WHERE course_id = ?
                    """,
                    (
                        new_id,
                        name,
                        self.editing_id
                    )
                )

                self.clear_course()

            conn.commit()
            conn.close()

            self.editing_type = None
            self.editing_id = None

            self.load_records()
            self.update_dropdowns()

            QMessageBox.information(
                self,
                "Success",
                "Record updated successfully!"
            )

        except (
            ValueError,
            sqlite3.IntegrityError
        ) as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

def backup_database(self):
        """Create a timestamped backup copy of the SQLite database."""

        try:
            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            backup_name = (
                f"school_backup_{timestamp}.db"
            )

            shutil.copy(
                DATABASE,
                backup_name
            )

            QMessageBox.information(
                self,
                "Backup",
                f"Database backed up as:\n{backup_name}"
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

def restore_database(self):
        """Restore the SQLite database from the latest available backup."""

        import glob

        backups = glob.glob(
            "school_backup_*.db"
        )

        if not backups:
            QMessageBox.warning(
                self,
                "Error",
                "No database backup found."
            )
            return

        latest_backup = max(
            backups,
            key=lambda x: x
        )

        try:
            shutil.copy(
                latest_backup,
                DATABASE
            )

            self.load_records()
            self.update_dropdowns()

            QMessageBox.information(
                self,
                "Restore",
                f"Database restored from:\n{latest_backup}"
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error)
            )

def clear_student(self):
        """Clear all fields in the student form."""
        self.student_name.clear()
        self.student_age.clear()
        self.student_email.clear()
        self.student_id.clear()

def clear_instructor(self):
        """Clear all fields in the instructor form."""
        self.instructor_name.clear()
        self.instructor_age.clear()
        self.instructor_email.clear()
        self.instructor_id.clear()

def clear_course(self):
        """Clear all fields in the course form."""
        self.course_id.clear()
        self.course_name.clear()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = DatabaseApp()
    window.show()

    sys.exit(app.exec_())