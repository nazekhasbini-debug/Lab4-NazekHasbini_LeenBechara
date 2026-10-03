"""
PyQt5 graphical user interface for the School Management System.

This module provides a PyQt5-based interface for managing students,
instructors, and courses. It supports adding, editing, deleting, searching,
saving, loading, and exporting records, as well as student registration
and instructor assignment.
"""
import sys
import json
import csv

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QFileDialog,
    QHeaderView
)

from part1_oop import Student, Instructor, Course

class SchoolManagementSystem(QMainWindow):
    """
    Main window for the School Management System.

    This class provides the PyQt5 graphical user interface used to manage
    students, instructors, courses, registrations, assignments, and records.
    """

    def __init__(self):
        """Initialize the School Management System user interface."""
        super().__init__()

        self.setWindowTitle("School Management System")
        self.resize(1100, 750)

        # Data
        self.students = []
        self.instructors = []
        self.courses = []

        # Used when editing
        self.editing_type = None
        self.editing_object = None

        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # =========================
        # TITLE
        # =========================

        title = QLabel("School Management System")
        title.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )
        main_layout.addWidget(title)

        # =========================
        # STUDENT FORM
        # =========================

        student_group = QGroupBox("Add Student")
        student_layout = QFormLayout()

        self.student_name = QLineEdit()
        self.student_age = QLineEdit()
        self.student_email = QLineEdit()
        self.student_id = QLineEdit()

        student_layout.addRow("Name:", self.student_name)
        student_layout.addRow("Age:", self.student_age)
        student_layout.addRow("Email:", self.student_email)
        student_layout.addRow("Student ID:", self.student_id)

        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)

        student_layout.addRow(self.add_student_button)

        student_group.setLayout(student_layout)

        # =========================
        # INSTRUCTOR FORM
        # =========================

        instructor_group = QGroupBox("Add Instructor")
        instructor_layout = QFormLayout()

        self.instructor_name = QLineEdit()
        self.instructor_age = QLineEdit()
        self.instructor_email = QLineEdit()
        self.instructor_id = QLineEdit()

        instructor_layout.addRow(
            "Name:",
            self.instructor_name
        )
        instructor_layout.addRow(
            "Age:",
            self.instructor_age
        )
        instructor_layout.addRow(
            "Email:",
            self.instructor_email
        )
        instructor_layout.addRow(
            "Instructor ID:",
            self.instructor_id
        )

        self.add_instructor_button = QPushButton(
            "Add Instructor"
        )
        self.add_instructor_button.clicked.connect(
            self.add_instructor
        )

        instructor_layout.addRow(
            self.add_instructor_button
        )

        instructor_group.setLayout(
            instructor_layout
        )

        # =========================
        # COURSE FORM
        # =========================

        course_group = QGroupBox("Add Course")
        course_layout = QFormLayout()

        self.course_id = QLineEdit()
        self.course_name = QLineEdit()

        course_layout.addRow(
            "Course ID:",
            self.course_id
        )
        course_layout.addRow(
            "Course Name:",
            self.course_name
        )

        self.add_course_button = QPushButton(
            "Add Course"
        )
        self.add_course_button.clicked.connect(
            self.add_course
        )

        course_layout.addRow(
            self.add_course_button
        )

        course_group.setLayout(course_layout)

        # Put the 3 forms beside each other
        forms_layout = QHBoxLayout()
        forms_layout.addWidget(student_group)
        forms_layout.addWidget(instructor_group)
        forms_layout.addWidget(course_group)

        main_layout.addLayout(forms_layout)

        # =========================
        # STUDENT REGISTRATION
        # =========================

        registration_group = QGroupBox(
            "Student Registration"
        )

        registration_layout = QHBoxLayout()

        self.student_dropdown = QComboBox()
        self.student_course_dropdown = QComboBox()

        self.register_button = QPushButton(
            "Register Student"
        )
        self.register_button.clicked.connect(
            self.register_student
        )

        registration_layout.addWidget(
            QLabel("Student:")
        )
        registration_layout.addWidget(
            self.student_dropdown
        )

        registration_layout.addWidget(
            QLabel("Course:")
        )
        registration_layout.addWidget(
            self.student_course_dropdown
        )

        registration_layout.addWidget(
            self.register_button
        )

        registration_group.setLayout(
            registration_layout
        )

        main_layout.addWidget(registration_group)

        # =========================
        # INSTRUCTOR ASSIGNMENT
        # =========================

        assignment_group = QGroupBox(
            "Instructor Assignment"
        )

        assignment_layout = QHBoxLayout()

        self.instructor_dropdown = QComboBox()
        self.instructor_course_dropdown = QComboBox()

        self.assign_button = QPushButton(
            "Assign Instructor"
        )
        self.assign_button.clicked.connect(
            self.assign_instructor
        )

        assignment_layout.addWidget(
            QLabel("Instructor:")
        )
        assignment_layout.addWidget(
            self.instructor_dropdown
        )

        assignment_layout.addWidget(
            QLabel("Course:")
        )
        assignment_layout.addWidget(
            self.instructor_course_dropdown
        )

        assignment_layout.addWidget(
            self.assign_button
        )

        assignment_group.setLayout(
            assignment_layout
        )

        main_layout.addWidget(assignment_group)

        # =========================
        # SEARCH
        # =========================

        search_layout = QHBoxLayout()

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText(
            "Search by name, ID, or course..."
        )

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(
            self.search_records
        )

        self.clear_search_button = QPushButton(
            "Clear Search"
        )
        self.clear_search_button.clicked.connect(
            self.clear_search
        )

        search_layout.addWidget(
            QLabel("Search:")
        )
        search_layout.addWidget(
            self.search_entry
        )
        search_layout.addWidget(
            self.search_button
        )
        search_layout.addWidget(
            self.clear_search_button
        )

        main_layout.addLayout(search_layout)

        # =========================
        # TABLE
        # =========================

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            [
                "Type",
                "ID",
                "Name / Course",
                "Email"
            ]
        )

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

        # =========================
        # ADVANCED BUTTONS
        # =========================

        button_layout = QHBoxLayout()

        self.edit_button = QPushButton(
            "Edit Selected"
        )
        self.edit_button.clicked.connect(
            self.edit_record
        )

        self.save_changes_button = QPushButton(
            "Save Changes"
        )
        self.save_changes_button.clicked.connect(
            self.save_changes
        )

        self.delete_button = QPushButton(
            "Delete Selected"
        )
        self.delete_button.clicked.connect(
            self.delete_record
        )

        self.save_button = QPushButton(
            "Save Data"
        )
        self.save_button.clicked.connect(
            self.save_data
        )

        self.load_button = QPushButton(
            "Load Data"
        )
        self.load_button.clicked.connect(
            self.load_data
        )

        self.export_button = QPushButton(
            "Export to CSV"
        )
        self.export_button.clicked.connect(
            self.export_csv
        )

        button_layout.addWidget(
            self.edit_button
        )
        button_layout.addWidget(
            self.save_changes_button
        )
        button_layout.addWidget(
            self.delete_button
        )
        button_layout.addWidget(
            self.save_button
        )
        button_layout.addWidget(
            self.load_button
        )
        button_layout.addWidget(
            self.export_button
        )

        main_layout.addLayout(button_layout)

    # ==================================================
    # ADD STUDENT
    # ==================================================

    def add_student(self):
        """
        Add a new student after validating the entered information.
        """
        try:
            name = self.student_name.text().strip()
            age_text = self.student_age.text().strip()
            email = self.student_email.text().strip()
            student_id = self.student_id.text().strip()

            if not age_text:
                raise ValueError("Age cannot be empty.")

            age = int(age_text)

            # Student class performs our validation
            student = Student(
                name,
                age,
                email,
                student_id
            )

            # Prevent duplicate IDs
            if any(
                s.student_id == student_id
                for s in self.students
            ):
                raise ValueError(
                    "Student ID already exists."
                )

            self.students.append(student)

            self.update_dropdowns()
            self.refresh_table()
            self.clear_student_form()

            QMessageBox.information(
                self,
                "Success",
                f"Student {name} added successfully!"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Input Error",
                str(error)
            )

    # ==================================================
    # ADD INSTRUCTOR
    # ==================================================

    def add_instructor(self):
        """
        Add a new instructor after validating the entered information.
        """
        try:
            name = self.instructor_name.text().strip()
            age_text = self.instructor_age.text().strip()
            email = self.instructor_email.text().strip()
            instructor_id = self.instructor_id.text().strip()

            if not age_text:
                raise ValueError("Age cannot be empty.")

            age = int(age_text)

            instructor = Instructor(
                name,
                age,
                email,
                instructor_id
            )

            if any(
                i.instructor_id == instructor_id
                for i in self.instructors
            ):
                raise ValueError(
                    "Instructor ID already exists."
                )

            self.instructors.append(instructor)

            self.update_dropdowns()
            self.refresh_table()
            self.clear_instructor_form()

            QMessageBox.information(
                self,
                "Success",
                f"Instructor {name} added successfully!"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Input Error",
                str(error)
            )

    # ==================================================
    # ADD COURSE
    # ==================================================

    def add_course(self):
        """
        Add a new course after validating the entered information.
        """
        try:
            course_id = self.course_id.text().strip()
            course_name = self.course_name.text().strip()

            if not course_id or not course_name:
                raise ValueError(
                    "Course ID and Course Name cannot be empty."
                )

            if any(
                c.course_id == course_id
                for c in self.courses
            ):
                raise ValueError(
                    "Course ID already exists."
                )

            course = Course(
                course_id,
                course_name
            )

            self.courses.append(course)

            self.update_dropdowns()
            self.refresh_table()
            self.clear_course_form()

            QMessageBox.information(
                self,
                "Success",
                f"Course {course_name} added successfully!"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Input Error",
                str(error)
            )

    # ==================================================
    # STUDENT REGISTRATION
    # ==================================================

    def register_student(self):
        """
        Register a student for a course.
        """
        student_id = self.student_dropdown.currentText()
        course_id = self.student_course_dropdown.currentText()

        if not student_id or not course_id:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a student and a course."
            )
            return

        student = next(
            (
                s for s in self.students
                if s.student_id == student_id
            ),
            None
        )

        course = next(
            (
                c for c in self.courses
                if c.course_id == course_id
            ),
            None
        )

        if student and course:

            # Prevent duplicate registration
            if course in student.registered_courses:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Student is already registered in this course."
                )
                return

            student.register_course(course)
            course.add_student(student)

            QMessageBox.information(
                self,
                "Success",
                f"{student.name} registered for "
                f"{course.course_name}!"
            )

    # ==================================================
    # INSTRUCTOR ASSIGNMENT
    # ==================================================

    def assign_instructor(self):
        """
        Assign the selected instructor to the selected course.
        """
        instructor_id = (
            self.instructor_dropdown.currentText()
        )

        course_id = (
            self.instructor_course_dropdown.currentText()
        )

        if not instructor_id or not course_id:
            QMessageBox.warning(
                self,
                "Error",
                "Please select an instructor and a course."
            )
            return

        instructor = next(
            (
                i for i in self.instructors
                if i.instructor_id == instructor_id
            ),
            None
        )

        course = next(
            (
                c for c in self.courses
                if c.course_id == course_id
            ),
            None
        )

        if instructor and course:
            instructor.assign_course(course)
            course.instructor = instructor

            QMessageBox.information(
                self,
                "Success",
                f"{instructor.name} assigned to "
                f"{course.course_name}!"
            )

    # ==================================================
    # REFRESH TABLE
    # ==================================================

    def refresh_table(self):
        """
        Refresh the table to display all current records.
        """
        self.table.setRowCount(0)

        for student in self.students:
            self.add_table_row(
                "Student",
                student.student_id,
                student.name,
                student._email
            )

        for instructor in self.instructors:
            self.add_table_row(
                "Instructor",
                instructor.instructor_id,
                instructor.name,
                instructor._email
            )

        for course in self.courses:
            self.add_table_row(
                "Course",
                course.course_id,
                course.course_name,
                "-"
            )

    def add_table_row(
    self,
    record_type,
    record_id,
    name,
    email
):
        """
        Add a record to the records table.

        :param record_type: Type of record being displayed.
        :param record_id: ID of the record.
        :param name: Name of the person or course.
        :param email: Email address associated with the record.
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
                QTableWidgetItem(str(value))
            )

    # ==================================================
    # SEARCH
    # ==================================================

    def search_records(self):
        """Search records by name, ID, email, or course information."""
        search_text = (
            self.search_entry.text().lower().strip()
        )

        self.table.setRowCount(0)

        if not search_text:
            self.refresh_table()
            return

        for student in self.students:
            if (
                search_text in student.name.lower()
                or search_text
                in student.student_id.lower()
                or search_text
                in student._email.lower()
            ):
                self.add_table_row(
                    "Student",
                    student.student_id,
                    student.name,
                    student._email
                )

        for instructor in self.instructors:
            if (
                search_text in instructor.name.lower()
                or search_text
                in instructor.instructor_id.lower()
                or search_text
                in instructor._email.lower()
            ):
                self.add_table_row(
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    instructor._email
                )

        for course in self.courses:
            if (
                search_text in course.course_id.lower()
                or search_text
                in course.course_name.lower()
            ):
                self.add_table_row(
                    "Course",
                    course.course_id,
                    course.course_name,
                    "-"
                )

    def clear_search(self):
        """Clear the search field and display all records."""
        self.search_entry.clear()
        self.refresh_table()

    # ==================================================
    # DELETE
    # ==================================================

    def delete_record(self):
        """Delete the selected student, instructor, or course record."""
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a record to delete."
            )
            return

        record_type = self.table.item(
            row,
            0
        ).text()

        record_id = self.table.item(
            row,
            1
        ).text()

        if record_type == "Student":
            self.students = [
                student
                for student in self.students
                if student.student_id != record_id
            ]

        elif record_type == "Instructor":
            self.instructors = [
                instructor
                for instructor in self.instructors
                if instructor.instructor_id != record_id
            ]

        elif record_type == "Course":
            self.courses = [
                course
                for course in self.courses
                if course.course_id != record_id
            ]

        self.update_dropdowns()
        self.refresh_table()

        QMessageBox.information(
            self,
            "Success",
            "Record deleted successfully!"
        )

    # ==================================================
    # EDIT
    # ==================================================

    def edit_record(self):
        """Load the selected record into its form for editing."""
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a record to edit."
            )
            return

        record_type = self.table.item(
            row,
            0
        ).text()

        record_id = self.table.item(
            row,
            1
        ).text()

        if record_type == "Student":

            student = next(
                (
                    s for s in self.students
                    if s.student_id == record_id
                ),
                None
            )

            if student:
                self.editing_type = "Student"
                self.editing_object = student

                self.student_name.setText(
                    student.name
                )
                self.student_age.setText(
                    str(student.age)
                )
                self.student_email.setText(
                    student._email
                )
                self.student_id.setText(
                    student.student_id
                )

        elif record_type == "Instructor":

            instructor = next(
                (
                    i for i in self.instructors
                    if i.instructor_id == record_id
                ),
                None
            )

            if instructor:
                self.editing_type = "Instructor"
                self.editing_object = instructor

                self.instructor_name.setText(
                    instructor.name
                )
                self.instructor_age.setText(
                    str(instructor.age)
                )
                self.instructor_email.setText(
                    instructor._email
                )
                self.instructor_id.setText(
                    instructor.instructor_id
                )

        elif record_type == "Course":

            course = next(
                (
                    c for c in self.courses
                    if c.course_id == record_id
                ),
                None
            )

            if course:
                self.editing_type = "Course"
                self.editing_object = course

                self.course_id.setText(
                    course.course_id
                )
                self.course_name.setText(
                    course.course_name
                )

        QMessageBox.information(
            self,
            "Edit",
            "Modify the information above and "
            "click Save Changes."
        )

    # ==================================================
    # SAVE EDITED RECORD
    # ==================================================

    def save_changes(self):
        """Validate and save changes made to the selected record."""
        if self.editing_object is None:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a record to edit first."
            )
            return

        try:
            if self.editing_type == "Student":

                name = self.student_name.text().strip()
                age = int(
                    self.student_age.text().strip()
                )
                email = self.student_email.text().strip()
                student_id = self.student_id.text().strip()

                # Validate
                Student(
                    name,
                    age,
                    email,
                    student_id
                )

                # Check duplicate ID except itself
                for student in self.students:
                    if (
                        student is not self.editing_object
                        and student.student_id == student_id
                    ):
                        raise ValueError(
                            "Student ID already exists."
                        )

                self.editing_object.name = name
                self.editing_object.age = age
                self.editing_object._email = email
                self.editing_object.student_id = student_id

                self.clear_student_form()

            elif self.editing_type == "Instructor":

                name = (
                    self.instructor_name.text().strip()
                )
                age = int(
                    self.instructor_age.text().strip()
                )
                email = (
                    self.instructor_email.text().strip()
                )
                instructor_id = (
                    self.instructor_id.text().strip()
                )

                Instructor(
                    name,
                    age,
                    email,
                    instructor_id
                )

                for instructor in self.instructors:
                    if (
                        instructor is not self.editing_object
                        and instructor.instructor_id
                        == instructor_id
                    ):
                        raise ValueError(
                            "Instructor ID already exists."
                        )

                self.editing_object.name = name
                self.editing_object.age = age
                self.editing_object._email = email
                self.editing_object.instructor_id = instructor_id

                self.clear_instructor_form()

            elif self.editing_type == "Course":

                course_id = (
                    self.course_id.text().strip()
                )
                course_name = (
                    self.course_name.text().strip()
                )

                if not course_id or not course_name:
                    raise ValueError(
                        "Course ID and Course Name "
                        "cannot be empty."
                    )

                for course in self.courses:
                    if (
                        course is not self.editing_object
                        and course.course_id == course_id
                    ):
                        raise ValueError(
                            "Course ID already exists."
                        )

                self.editing_object.course_id = course_id
                self.editing_object.course_name = course_name

                self.clear_course_form()

            self.editing_type = None
            self.editing_object = None

            self.update_dropdowns()
            self.refresh_table()

            QMessageBox.information(
                self,
                "Success",
                "Record updated successfully!"
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Input Error",
                str(error)
            )

    # ==================================================
    # SAVE DATA
    # ==================================================

    def save_data(self):
        """Save all school management data to a JSON file."""
        data = {
            "students": [
                {
                    "name": student.name,
                    "age": student.age,
                    "email": student._email,
                    "student_id": student.student_id,
                    "registered_courses": [
                        course.course_id
                        for course
                        in student.registered_courses
                    ]
                }
                for student in self.students
            ],

            "instructors": [
                {
                    "name": instructor.name,
                    "age": instructor.age,
                    "email": instructor._email,
                    "instructor_id":
                        instructor.instructor_id,
                    "assigned_courses": [
                        course.course_id
                        for course
                        in instructor.assigned_courses
                    ]
                }
                for instructor in self.instructors
            ],

            "courses": [
                {
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "instructor_id":
                        course.instructor.instructor_id
                        if course.instructor
                        else None,
                    "enrolled_students": [
                        student.student_id
                        for student
                        in course.enrolled_students
                    ]
                }
                for course in self.courses
            ]
        }

        with open(
            "pyqt_data.json",
            "w"
        ) as file:
            json.dump(
                data,
                file,
                indent=4
            )

        QMessageBox.information(
            self,
            "Success",
            "Data saved successfully!"
        )

    # ==================================================
    # LOAD DATA
    # ==================================================

    def load_data(self):
        """Load previously saved school management data from JSON."""
        try:
            with open(
                "pyqt_data.json",
                "r"
            ) as file:
                data = json.load(file)

            self.students.clear()
            self.instructors.clear()
            self.courses.clear()

            # First create courses
            for course_data in data["courses"]:
                course = Course(
                    course_data["course_id"],
                    course_data["course_name"]
                )
                self.courses.append(course)

            # Create students
            for student_data in data["students"]:
                student = Student(
                    student_data["name"],
                    student_data["age"],
                    student_data["email"],
                    student_data["student_id"]
                )
                self.students.append(student)

            # Create instructors
            for instructor_data in data["instructors"]:
                instructor = Instructor(
                    instructor_data["name"],
                    instructor_data["age"],
                    instructor_data["email"],
                    instructor_data["instructor_id"]
                )
                self.instructors.append(instructor)

            # Restore student registrations
            for student_data in data["students"]:

                student = next(
                    (
                        s for s in self.students
                        if s.student_id
                        == student_data["student_id"]
                    ),
                    None
                )

                for course_id in student_data.get(
                    "registered_courses",
                    []
                ):
                    course = next(
                        (
                            c for c in self.courses
                            if c.course_id == course_id
                        ),
                        None
                    )

                    if student and course:
                        student.register_course(course)

                        if student not in course.enrolled_students:
                            course.add_student(student)

            # Restore instructor assignments
            for instructor_data in data["instructors"]:

                instructor = next(
                    (
                        i for i in self.instructors
                        if i.instructor_id
                        == instructor_data["instructor_id"]
                    ),
                    None
                )

                for course_id in instructor_data.get(
                    "assigned_courses",
                    []
                ):
                    course = next(
                        (
                            c for c in self.courses
                            if c.course_id == course_id
                        ),
                        None
                    )

                    if instructor and course:
                        instructor.assign_course(course)
                        course.instructor = instructor

            self.update_dropdowns()
            self.refresh_table()

            QMessageBox.information(
                self,
                "Success",
                "Data loaded successfully!"
            )

        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "Error",
                "No saved PyQt data file found."
            )

        except (ValueError, KeyError, json.JSONDecodeError) as error:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not load data: {error}"
            )

    # ==================================================
    # EXPORT CSV
    # ==================================================

    def export_csv(self):
        """Export all current records to a CSV file."""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Records",
            "school_records.csv",
            "CSV Files (*.csv)"
        )

        if not filename:
            return

        try:
            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "Type",
                        "ID",
                        "Name / Course",
                        "Email"
                    ]
                )

                for student in self.students:
                    writer.writerow(
                        [
                            "Student",
                            student.student_id,
                            student.name,
                            student._email
                        ]
                    )

                for instructor in self.instructors:
                    writer.writerow(
                        [
                            "Instructor",
                            instructor.instructor_id,
                            instructor.name,
                            instructor._email
                        ]
                    )

                for course in self.courses:
                    writer.writerow(
                        [
                            "Course",
                            course.course_id,
                            course.course_name,
                            "-"
                        ]
                    )

            QMessageBox.information(
                self,
                "Success",
                "Records exported to CSV successfully!"
            )

        except OSError as error:
            QMessageBox.warning(
                self,
                "Error",
                f"Could not export CSV: {error}"
            )

    # ==================================================
    # DROPDOWNS
    # ==================================================

    def update_dropdowns(self):
        """Update all student, instructor, and course dropdown menus."""
        self.student_dropdown.clear()
        self.student_course_dropdown.clear()
        self.instructor_dropdown.clear()
        self.instructor_course_dropdown.clear()

        self.student_dropdown.addItems(
            [
                student.student_id
                for student in self.students
            ]
        )

        course_ids = [
            course.course_id
            for course in self.courses
        ]

        self.student_course_dropdown.addItems(
            course_ids
        )

        self.instructor_dropdown.addItems(
            [
                instructor.instructor_id
                for instructor in self.instructors
            ]
        )

        self.instructor_course_dropdown.addItems(
            course_ids
        )

    # ==================================================
    # CLEAR FORMS
    # ==================================================

    def clear_student_form(self):
        """Clear all fields in the student form."""
        self.student_name.clear()
        self.student_age.clear()
        self.student_email.clear()
        self.student_id.clear()

    def clear_instructor_form(self):
        """Clear all fields in the instructor form."""
        self.instructor_name.clear()
        self.instructor_age.clear()
        self.instructor_email.clear()
        self.instructor_id.clear()

    def clear_course_form(self):
        """Clear all fields in the course form."""
        self.course_id.clear()
        self.course_name.clear()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = SchoolManagementSystem()
    window.show()

    sys.exit(app.exec_())