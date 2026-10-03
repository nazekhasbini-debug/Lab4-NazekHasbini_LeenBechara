# Lab 4 - School Management System

This project is a School Management System developed using Python. It includes both Tkinter and PyQt graphical user interfaces.

## Team Members

- Leen Bechara
- Nazek Hasbini

## Project Files

- `part1_oop.py` - OOP classes for Student, Instructor, and Course
- `part2_tkinter.py` - Tkinter implementation
- `part3_pyqt.py` - PyQt implementation
- `part4_database.py` - Database implementation
- `docs/` - Sphinx documentation

## Requirements

- Python 3
- PyQt5

Install PyQt5 using:

```bash
pip install PyQt5
```

## Run the Tkinter Application

```bash
python part2_tkinter.py
```

## Run the PyQt Application

```bash
python part3_pyqt.py
```

## Features

- Add students
- Add instructors
- Add courses
- Register students in courses
- Assign instructors to courses
- Search records
- Edit and delete records
- Save and load data
- Export data to CSV

## Documentation

Sphinx documentation is available in the `docs` folder.

To build it on Windows:

```bash
cd docs
make.bat html
```

## Team Contributions

- **Leen Bechara:** Worked on the Tkinter implementation, integration, testing, and documentation.
- **Nazek Hasbini:** Worked on the PyQt implementation, testing, and Git/GitHub workflow.
- Both used branches and pull requests to integrate their work into the `main` branch.
