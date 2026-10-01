"""
Tkinter graphical user interface for the School Management System.

This module provides a Tkinter-based interface for managing students,
instructors, and courses. It supports adding, editing, deleting, searching,
saving, and loading school records, as well as course registration and
instructor assignment.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from part1_oop import Student, Instructor, Course 

root = tk.Tk()
root.title("School Management System")
root.geometry("1000x650")

title_label = tk.Label(
    root,
    text="School Management System",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=20)

students = []
instructors = []
courses = []

editing_type = None
editing_object = None

def add_student():
    """Add a new student using the information entered in the GUI."""
    try:
        name = student_name_entry.get()
        age = int(student_age_entry.get())
        email = student_email_entry.get()
        student_id = student_id_entry.get()

        student = Student(name, age, email, student_id)
        students.append(student)
        refresh_table()
        student_dropdown["values"] = [
            s.student_id for s in students
        ]
        

        messagebox.showinfo(
            "Success",
            f"Student {name} added successfully!"
        )

       
        student_name_entry.delete(0, tk.END)
        student_age_entry.delete(0, tk.END)
        student_email_entry.delete(0, tk.END)
        student_id_entry.delete(0, tk.END)

    except ValueError as error:
        messagebox.showerror("Error", str(error))

def add_instructor():
    """Add a new instructor using the information entered in the GUI."""
    try:
        name = instructor_name_entry.get()
        age = int(instructor_age_entry.get())
        email = instructor_email_entry.get()
        instructor_id = instructor_id_entry.get()

        instructor = Instructor(
            name,
            age,
            email,
            instructor_id
        )

        instructors.append(instructor)
        refresh_table()
        instructor_dropdown["values"] = [
            i.instructor_id for i in instructors
        ]

        messagebox.showinfo(
            "Success",
            f"Instructor {name} added successfully!"
        )

       
        instructor_name_entry.delete(0, tk.END)
        instructor_age_entry.delete(0, tk.END)
        instructor_email_entry.delete(0, tk.END)
        instructor_id_entry.delete(0, tk.END)

    except ValueError as error:
        messagebox.showerror("Error", str(error))

def add_course():
    """Add a new course using the course information entered in the GUI."""
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()

    if course_id == "" or course_name == "":
        messagebox.showerror(
            "Error",
            "Course ID and Course Name cannot be empty."
        )
        return

    course = Course(course_id, course_name)
    courses.append(course)
    refresh_table()
    course_dropdown["values"] = [
        c.course_id for c in courses
    ]
    instructor_course_dropdown["values"] = [
        c.course_id for c in courses
    ]
    messagebox.showinfo(
        "Success",
        f"Course {course_name} added successfully!"
    )

    course_id_entry.delete(0, tk.END)
    course_name_entry.delete(0, tk.END)

def register_student():
    """Register the selected student in the selected course."""
    selected_student = student_dropdown.get()
    selected_course = course_dropdown.get()

    if selected_student == "" or selected_course == "":
        messagebox.showerror(
            "Error",
            "Please select a student and a course."
        )
        return

    student = next(
        (s for s in students if s.student_id == selected_student),
        None
    )

    course = next(
        (c for c in courses if c.course_id == selected_course),
        None
    )

    if student and course:
        student.register_course(course)
        course.add_student(student)

        messagebox.showinfo(
            "Success",
            f"{student.name} registered for {course.course_name}!"
        )
        refresh_table()
def assign_instructor():
    """Assign the selected instructor to the selected course."""
    selected_instructor = instructor_dropdown.get()
    selected_course = instructor_course_dropdown.get()

    if selected_instructor == "" or selected_course == "":
        messagebox.showerror(
            "Error",
            "Please select an instructor and a course."
        )
        return

    instructor = next(
        (i for i in instructors if i.instructor_id == selected_instructor),
        None
    )

    course = next(
        (c for c in courses if c.course_id == selected_course),
        None
    )

    if instructor and course:
        instructor.assign_course(course)
        course.instructor = instructor

        messagebox.showinfo(
            "Success",
            f"{instructor.name} assigned to {course.course_name}!"
        )
def refresh_table():
    """Refresh the records table with the current school data."""
    for row in records_tree.get_children():
        records_tree.delete(row)

    for student in students:
        records_tree.insert(
            "",
            tk.END,
            values=(
                "Student",
                student.student_id,
                student.name,
                student._email
            )
        )

    for instructor in instructors:
        records_tree.insert(
            "",
            tk.END,
            values=(
                "Instructor",
                instructor.instructor_id,
                instructor.name,
                instructor._email
            )
        )

    for course in courses:
        records_tree.insert(
            "",
            tk.END,
            values=(
                "Course",
                course.course_id,
                course.course_name,
                "-"
            )
        )
def search_records():
    """Search student, instructor, and course records."""
    search_text = search_entry.get().lower().strip()

    for row in records_tree.get_children():
        records_tree.delete(row)

    if search_text == "":
        refresh_table()
        return

    for student in students:
        if (
            search_text in student.name.lower()
            or search_text in student.student_id.lower()
        ):
            records_tree.insert(
                "",
                tk.END,
                values=(
                    "Student",
                    student.student_id,
                    student.name,
                    student._email
                )
            )

    for instructor in instructors:
        if (
            search_text in instructor.name.lower()
            or search_text in instructor.instructor_id.lower()
        ):
            records_tree.insert(
                "",
                tk.END,
                values=(
                    "Instructor",
                    instructor.instructor_id,
                    instructor.name,
                    instructor._email
                )
            )

    for course in courses:
        if (
            search_text in course.course_id.lower()
            or search_text in course.course_name.lower()
        ):
            records_tree.insert(
                "",
                tk.END,
                values=(
                    "Course",
                    course.course_id,
                    course.course_name,
                    "-"
                )
            )

def clear_search():
    """Clear the search field and display all records."""
    search_entry.delete(0, tk.END)
    refresh_table()
def update_dropdowns():
    """Update the student, instructor, and course dropdown menus."""
    student_dropdown["values"] = [
        student.student_id for student in students
    ]

    instructor_dropdown["values"] = [
        instructor.instructor_id for instructor in instructors
    ]

    course_dropdown["values"] = [
        course.course_id for course in courses
    ]

    instructor_course_dropdown["values"] = [
        course.course_id for course in courses
    ]
def delete_record():
    """Delete the currently selected record from the system."""
    selected = records_tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a record to delete."
        )
        return

    item = records_tree.item(selected[0])
    values = item["values"]

    record_type = values[0]
    record_id = str(values[1])

    if record_type == "Student":
        for student in students:
            if student.student_id == record_id:
                students.remove(student)
                break

    elif record_type == "Instructor":
        for instructor in instructors:
            if instructor.instructor_id == record_id:
                instructors.remove(instructor)
                break

    elif record_type == "Course":
        for course in courses:
            if course.course_id == record_id:
                courses.remove(course)
                break

    refresh_table()
    update_dropdowns()

    messagebox.showinfo(
        "Success",
        "Record deleted successfully!"
    )
def edit_record():
    """Load the selected record into the form for editing."""
    global editing_type, editing_object

    selected = records_tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select a record to edit."
        )
        return

    item = records_tree.item(selected[0])
    values = item["values"]

    record_type = values[0]
    record_id = str(values[1])

    if record_type == "Student":
        student = next(
            (s for s in students if s.student_id == record_id),
            None
        )

        if student:
            editing_type = "Student"
            editing_object = student

            student_name_entry.delete(0, tk.END)
            student_name_entry.insert(0, student.name)

            student_age_entry.delete(0, tk.END)
            student_age_entry.insert(0, student.age)

            student_email_entry.delete(0, tk.END)
            student_email_entry.insert(0, student._email)

            student_id_entry.delete(0, tk.END)
            student_id_entry.insert(0, student.student_id)

    elif record_type == "Instructor":
        instructor = next(
            (i for i in instructors if i.instructor_id == record_id),
            None
        )

        if instructor:
            editing_type = "Instructor"
            editing_object = instructor

            instructor_name_entry.delete(0, tk.END)
            instructor_name_entry.insert(0, instructor.name)

            instructor_age_entry.delete(0, tk.END)
            instructor_age_entry.insert(0, instructor.age)

            instructor_email_entry.delete(0, tk.END)
            instructor_email_entry.insert(0, instructor._email)

            instructor_id_entry.delete(0, tk.END)
            instructor_id_entry.insert(0, instructor.instructor_id)

    elif record_type == "Course":
        course = next(
            (c for c in courses if c.course_id == record_id),
            None
        )

        if course:
            editing_type = "Course"
            editing_object = course

            course_id_entry.delete(0, tk.END)
            course_id_entry.insert(0, course.course_id)

            course_name_entry.delete(0, tk.END)
            course_name_entry.insert(0, course.course_name)

    messagebox.showinfo(
        "Edit",
        "Modify the information above, then click Save Changes."
    )

def save_changes():
    """Validate and save changes made to the selected record."""
    global editing_type, editing_object

    if editing_object is None:
        messagebox.showerror(
            "Error",
            "Please select a record to edit first."
        )
        return

    try:
        if editing_type == "Student":
            name = student_name_entry.get()
            age = int(student_age_entry.get())
            email = student_email_entry.get()
            student_id = student_id_entry.get()

            Student(name, age, email, student_id)

            editing_object.name = name
            editing_object.age = age
            editing_object._email = email
            editing_object.student_id = student_id

        elif editing_type == "Instructor":
            name = instructor_name_entry.get()
            age = int(instructor_age_entry.get())
            email = instructor_email_entry.get()
            instructor_id = instructor_id_entry.get()

            Instructor(name, age, email, instructor_id)

            editing_object.name = name
            editing_object.age = age
            editing_object._email = email
            editing_object.instructor_id = instructor_id

        elif editing_type == "Course":
            course_id = course_id_entry.get()
            course_name = course_name_entry.get()

            if course_id == "" or course_name == "":
                raise ValueError(
                    "Course ID and Course Name cannot be empty."
                )

            editing_object.course_id = course_id
            editing_object.course_name = course_name

        refresh_table()
        update_dropdowns()

        editing_type = None
        editing_object = None

        messagebox.showinfo(
            "Success",
            "Record updated successfully!"
        )

    except ValueError as error:
        messagebox.showerror(
            "Error",
            str(error)
        )
def save_data():
    """Save the current school records to a JSON file."""
    data = {
        "students": [
            {
                "name": student.name,
                "age": student.age,
                "email": student._email,
                "student_id": student.student_id
            }
            for student in students
        ],

        "instructors": [
            {
                "name": instructor.name,
                "age": instructor.age,
                "email": instructor._email,
                "instructor_id": instructor.instructor_id
            }
            for instructor in instructors
        ],

        "courses": [
            {
                "course_id": course.course_id,
                "course_name": course.course_name
            }
            for course in courses
        ]
    }

    with open("tkinter_data.json", "w") as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo(
        "Success",
        "Data saved successfully!"
    )
def load_data():
    """Load previously saved school records from a JSON file."""
    try:
        with open("tkinter_data.json", "r") as file:
            data = json.load(file)

        students.clear()
        instructors.clear()
        courses.clear()

        for student_data in data["students"]:
            student = Student(
                student_data["name"],
                student_data["age"],
                student_data["email"],
                student_data["student_id"]
            )
            students.append(student)

        for instructor_data in data["instructors"]:
            instructor = Instructor(
                instructor_data["name"],
                instructor_data["age"],
                instructor_data["email"],
                instructor_data["instructor_id"]
            )
            instructors.append(instructor)

        for course_data in data["courses"]:
            course = Course(
                course_data["course_id"],
                course_data["course_name"]
            )
            courses.append(course)

        refresh_table()
        update_dropdowns()

        messagebox.showinfo(
            "Success",
            "Data loaded successfully!"
        )

    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "No saved data file found."
        )


student_frame = tk.LabelFrame(
    root,
    text="Add Student",
    padx=10,
    pady=10
)
student_frame.pack(padx=20, pady=10, fill="x")

tk.Label(student_frame, text="Name:").grid(
    row=0, column=0, padx=5, pady=5
)
student_name_entry = tk.Entry(student_frame)
student_name_entry.grid(
    row=0, column=1, padx=5, pady=5
)
add_student_button = tk.Button(
    student_frame,
    text="Add Student",
    command=add_student
)

add_student_button.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=10
)

tk.Label(student_frame, text="Age:").grid(
    row=0, column=2, padx=5, pady=5
)
student_age_entry = tk.Entry(student_frame)
student_age_entry.grid(
    row=0, column=3, padx=5, pady=5
)


tk.Label(student_frame, text="Email:").grid(
    row=1, column=0, padx=5, pady=5
)
student_email_entry = tk.Entry(student_frame)
student_email_entry.grid(
    row=1, column=1, padx=5, pady=5
)

tk.Label(student_frame, text="Student ID:").grid(
    row=1, column=2, padx=5, pady=5
)
student_id_entry = tk.Entry(student_frame)
student_id_entry.grid(
    row=1, column=3, padx=5, pady=5
)


instructor_frame = tk.LabelFrame(
    root,
    text="Add Instructor",
    padx=10,
    pady=10
)
instructor_frame.pack(padx=20, pady=10, fill="x")

tk.Label(instructor_frame, text="Name:").grid(
    row=0, column=0, padx=5, pady=5
)
instructor_name_entry = tk.Entry(instructor_frame)
instructor_name_entry.grid(
    row=0, column=1, padx=5, pady=5
)

tk.Label(instructor_frame, text="Age:").grid(
    row=0, column=2, padx=5, pady=5
)
instructor_age_entry = tk.Entry(instructor_frame)
instructor_age_entry.grid(
    row=0, column=3, padx=5, pady=5
)

tk.Label(instructor_frame, text="Email:").grid(
    row=1, column=0, padx=5, pady=5
)
instructor_email_entry = tk.Entry(instructor_frame)
instructor_email_entry.grid(
    row=1, column=1, padx=5, pady=5
)

tk.Label(instructor_frame, text="Instructor ID:").grid(
    row=1, column=2, padx=5, pady=5
)
instructor_id_entry = tk.Entry(instructor_frame)
instructor_id_entry.grid(
    row=1, column=3, padx=5, pady=5
)

add_instructor_button = tk.Button(
    instructor_frame,
    text="Add Instructor",
    command=add_instructor
)
add_instructor_button.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=10
)


course_frame = tk.LabelFrame(
    root,
    text="Add Course",
    padx=10,
    pady=10
)
course_frame.pack(padx=20, pady=10, fill="x")

tk.Label(course_frame, text="Course ID:").grid(
    row=0, column=0, padx=5, pady=5
)
course_id_entry = tk.Entry(course_frame)
course_id_entry.grid(
    row=0, column=1, padx=5, pady=5
)

tk.Label(course_frame, text="Course Name:").grid(
    row=0, column=2, padx=5, pady=5
)
course_name_entry = tk.Entry(course_frame)
course_name_entry.grid(
    row=0, column=3, padx=5, pady=5
)

add_course_button = tk.Button(
    course_frame,
    text="Add Course",
    command=add_course
)
add_course_button.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=10
)


registration_frame = tk.LabelFrame(
    root,
    text="Student Registration",
    padx=10,
    pady=10
)
registration_frame.pack(padx=20, pady=10, fill="x")

tk.Label(
    registration_frame,
    text="Student:"
).grid(row=0, column=0, padx=5, pady=5)

student_dropdown = ttk.Combobox(
    registration_frame,
    state="readonly"
)
student_dropdown.grid(row=0, column=1, padx=5, pady=5)


tk.Label(
    registration_frame,
    text="Course:"
).grid(row=0, column=2, padx=5, pady=5)

course_dropdown = ttk.Combobox(
    registration_frame,
    state="readonly"
)
course_dropdown.grid(row=0, column=3, padx=5, pady=5)


register_button = tk.Button(
    registration_frame,
    text="Register Student",
    command=register_student
)
register_button.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=10
)


assignment_frame = tk.LabelFrame(
    root,
    text="Instructor Assignment",
    padx=10,
    pady=10
)
assignment_frame.pack(padx=20, pady=10, fill="x")

tk.Label(
    assignment_frame,
    text="Instructor:"
).grid(row=0, column=0, padx=5, pady=5)

instructor_dropdown = ttk.Combobox(
    assignment_frame,
    state="readonly"
)
instructor_dropdown.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)

tk.Label(
    assignment_frame,
    text="Course:"
).grid(row=0, column=2, padx=5, pady=5)

instructor_course_dropdown = ttk.Combobox(
    assignment_frame,
    state="readonly"
)
instructor_course_dropdown.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)

assign_button = tk.Button(
    assignment_frame,
    text="Assign Instructor",
    command=assign_instructor
)
assign_button.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=10
)


search_frame = tk.Frame(root)
search_frame.pack(padx=20, pady=5, fill="x")

tk.Label(
    search_frame,
    text="Search:"
).pack(side="left", padx=5)

search_entry = tk.Entry(
    search_frame,
    width=40
)
search_entry.pack(side="left", padx=5)

search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_records
)
search_button.pack(side="left", padx=5)

clear_button = tk.Button(
    search_frame,
    text="Clear",
    command=clear_search
)
clear_button.pack(side="left", padx=5)


records_frame = tk.LabelFrame(
    root,
    text="All Records",
    padx=10,
    pady=10
)
records_frame.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

records_tree = ttk.Treeview(
    records_frame,
    columns=("Type", "ID", "Name", "Email"),
    show="headings"
)

records_tree.heading("Type", text="Type")
records_tree.heading("ID", text="ID")
records_tree.heading("Name", text="Name / Course")
records_tree.heading("Email", text="Email")

records_tree.column("Type", width=100)
records_tree.column("ID", width=120)
records_tree.column("Name", width=220)
records_tree.column("Email", width=220)

records_tree.pack(
    fill="both",
    expand=True
)
delete_button = tk.Button(
    records_frame,
    text="Delete Selected",
    command=delete_record
)

delete_button.pack(pady=5)
root.mainloop()