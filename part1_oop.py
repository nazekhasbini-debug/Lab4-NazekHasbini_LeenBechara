"""
Object-Oriented Programming module for the School Management System.

This module defines the Person, Student, Instructor, and Course classes.
It also provides functions for saving and loading school data using JSON.
"""

import json


class Person:
    """
    Represent a person in the school management system.

    :param name: The person's name.
    :type name: str
    :param age: The person's age.
    :type age: int
    :param email: The person's email address.
    :type email: str
    """

    def __init__(self, name, age, email):
        """Initialize a Person object and validate its information."""

        # Name validation
        if not name.replace(" ", "").isalpha():
            raise ValueError("Name must contain letters only.")

        # Age validation
        if age < 0:
            raise ValueError("Age cannot be negative.")

        # Email validation
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format.")

        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        Return an introduction containing the person's name and age.

        :return: A short introduction.
        :rtype: str
        """
        return f"My name is {self.name} and I am {self.age} years old."


class Student(Person):
    """
    Represent a student in the school management system.

    The Student class inherits from Person and stores a student ID
    and the courses registered by the student.

    :param name: The student's name.
    :type name: str
    :param age: The student's age.
    :type age: int
    :param email: The student's email address.
    :type email: str
    :param student_id: The student's unique ID.
    :type student_id: str
    """

    def __init__(self, name, age, email, student_id):
        """Initialize a Student object."""
        super().__init__(name, age, email)

        if not student_id.isdigit():
            raise ValueError("Student ID must contain numbers only.")

        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """
        Register the student in a course.

        :param course: Course to register.
        :type course: Course
        """
        self.registered_courses.append(course)

    def introduce(self):
        """
        Return an introduction containing the student's name and ID.

        :return: A short student introduction.
        :rtype: str
        """
        return f"I am {self.name}, student ID: {self.student_id}."


class Instructor(Person):
    """
    Represent an instructor in the school management system.

    The Instructor class inherits from Person and stores the instructor's
    ID and assigned courses.

    :param name: The instructor's name.
    :type name: str
    :param age: The instructor's age.
    :type age: int
    :param email: The instructor's email address.
    :type email: str
    :param instructor_id: The instructor's unique ID.
    :type instructor_id: str
    """

    def __init__(self, name, age, email, instructor_id):
        """Initialize an Instructor object."""
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """
        Assign a course to the instructor.

        :param course: Course to assign.
        :type course: Course
        """
        self.assigned_courses.append(course)

    def introduce(self):
        """
        Return an introduction containing the instructor's name and ID.

        :return: A short instructor introduction.
        :rtype: str
        """
        return f"I am {self.name}, instructor ID: {self.instructor_id}."


class Course:
    """
    Represent a course in the school management system.

    :param course_id: The unique course ID.
    :type course_id: str
    :param course_name: The course name.
    :type course_name: str
    """

    def __init__(self, course_id, course_name):
        """Initialize a Course object."""
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = None
        self.enrolled_students = []

    def add_student(self, student):
        """
        Add a student to the course.

        :param student: Student to enroll.
        :type student: Student
        """
        self.enrolled_students.append(student)

    def __str__(self):
        """
        Return the course name.

        :return: The course name.
        :rtype: str
        """
        return self.course_name


def save_data(students, instructors, courses, filename="school_data.json"):
    """
    Save students, instructors, and courses to a JSON file.

    :param students: List of students to save.
    :param instructors: List of instructors to save.
    :param courses: List of courses to save.
    :param filename: Name of the JSON file.
    :type filename: str
    """

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

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully.")


def load_data(filename="school_data.json"):
    """
    Load school data from a JSON file.

    :param filename: Name of the JSON file to load.
    :type filename: str
    :return: Loaded school data.
    :rtype: dict
    """

    with open(filename, "r") as file:
        data = json.load(file)

    print("Data loaded successfully.")
    return data


# TEST CASES
if __name__ == "__main__":

    print("----- Testing Person -----")
    person1 = Person("Sara", 25, "sara@email.com")
    print(person1.introduce())

    print("\n----- Testing Student -----")
    student1 = Student("Mira", 21, "mira@email.com", "20260001")
    print(student1.introduce())

    print("\n----- Testing Instructor -----")
    instructor1 = Instructor(
        "Dr John",
        40,
        "john@aub.edu.lb",
        "I001"
    )
    print(instructor1.introduce())

    print("\n----- Testing Course -----")
    course1 = Course("EECE435", "Software Tools Lab")
    print("Course ID:", course1.course_id)
    print("Course Name:", course1.course_name)

    print("\n----- Testing Course Registration -----")
    student1.register_course(course1)
    course1.add_student(student1)

    print(
        student1.name,
        "registered for",
        student1.registered_courses[0].course_name
    )

    print(
        "Student enrolled in course:",
        course1.enrolled_students[0].name
    )

    print("\n----- Testing Instructor Assignment -----")
    instructor1.assign_course(course1)
    course1.instructor = instructor1

    print(
        instructor1.name,
        "assigned to",
        instructor1.assigned_courses[0].course_name
    )

    print("Course instructor:", course1.instructor.name)

    print("\n----- Testing Validation -----")

    try:
        Person("66", 21, "test@email.com")
    except ValueError as error:
        print("Name validation:", error)

    try:
        Person("Mira", -5, "mira@email.com")
    except ValueError as error:
        print("Age validation:", error)

    try:
        Person("Mira", 21, "invalidemail")
    except ValueError as error:
        print("Email validation:", error)

    try:
        Student("Mira", 21, "mira@email.com", "hi")
    except ValueError as error:
        print("Student ID validation:", error)

    print("\n----- Testing Save and Load -----")

    save_data(
        [student1],
        [instructor1],
        [course1]
    )

    loaded_data = load_data()

    print(loaded_data)