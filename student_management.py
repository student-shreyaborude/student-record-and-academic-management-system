#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Student Record and Academic Management System
Data Organization using Python Collections

Author : PRN 2126UDSF1089
Collections used
  * str   -> names, departments, addresses, e-mail IDs
  * list  -> all student records, subjects, marks, attendance
  * tuple -> identity data (roll number, registration number, date of birth)
  * set   -> departments, subjects, student clubs (unique values only)
  * dict  -> complete profile of one student
"""

import re

# ----------------------------------------------------------------------
# Global data (SETS + LIST)
# ----------------------------------------------------------------------
DEPARTMENTS = {"CSE", "IT", "ECE", "MECH", "CIVIL"}                 # set
SUBJECTS = {"Python", "Maths", "Physics", "English", "DBMS"}        # set
CLUBS = {"Coding", "Robotics", "Music", "Sports", "Drama"}          # set

students = []   # list of dictionaries -> every dictionary is one student profile


# ----------------------------------------------------------------------
# Validation helpers
# ----------------------------------------------------------------------
def is_valid_name(name):
    """Name must be a non-empty string with letters and spaces only."""
    return isinstance(name, str) and bool(re.fullmatch(r"[A-Za-z ]+", name.strip()))


def is_valid_email(email):
    return isinstance(email, str) and bool(re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.]+", email.strip()))


def is_valid_phone(phone):
    return isinstance(phone, str) and phone.isdigit() and len(phone) == 10


def is_valid_percent(value):
    """Marks / attendance must be a number between 0 and 100 (boundaries included)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 100


# ----------------------------------------------------------------------
# Core operations
# ----------------------------------------------------------------------
def find_student(roll_no):
    """Return the student dictionary with the given roll number, else None."""
    for s in students:
        if s["identity"][0] == roll_no:
            return s
    return None


def add_student(roll_no, reg_no, dob, name, department, address, email, phone,
                subjects, marks, attendance, clubs=()):
    """
    Add a new student record.
    Returns (True, message) on success or (False, reason) on failure.
    """
    if not isinstance(roll_no, int) or roll_no <= 0:
        return False, "Roll number must be a positive integer."
    if find_student(roll_no) is not None:
        return False, f"Duplicate record: roll number {roll_no} already exists."
    if any(s["identity"][1] == reg_no for s in students):
        return False, f"Duplicate record: registration number {reg_no} already exists."
    if not is_valid_name(name):
        return False, "Invalid name (letters and spaces only, cannot be empty)."
    department = department.strip().upper()
    if department not in DEPARTMENTS:
        return False, f"Unknown department. Choose from {sorted(DEPARTMENTS)}."
    if not is_valid_email(email):
        return False, "Invalid e-mail ID."
    if not is_valid_phone(phone):
        return False, "Phone number must contain exactly 10 digits."
    if not (isinstance(dob, tuple) and len(dob) == 3):
        return False, "Date of birth must be a tuple (year, month, day)."
    if not subjects or len(set(subjects)) != len(subjects):
        return False, "Subject list is empty or has duplicates."
    if not set(subjects) <= SUBJECTS:
        return False, f"Unknown subject. Allowed: {sorted(SUBJECTS)}."
    if len(marks) != len(subjects) or len(attendance) != len(subjects):
        return False, "Marks and attendance must match the number of subjects."
    if not all(is_valid_percent(m) for m in marks):
        return False, "Marks must be between 0 and 100."
    if not all(is_valid_percent(a) for a in attendance):
        return False, "Attendance must be between 0 and 100."
    if not set(clubs) <= CLUBS:
        return False, f"Unknown club. Allowed: {sorted(CLUBS)}."

    student = {                                              # DICTIONARY (profile)
        "identity": (roll_no, reg_no, dob),                  # TUPLE
        "name": name.strip().title(),                        # STRING
        "department": department,                            # STRING
        "subjects": list(subjects),                          # LIST
        "marks": list(marks),                                # LIST
        "attendance": list(attendance),                      # LIST
        "clubs": set(clubs),                                 # SET
        "contact": {"address": address.strip(),              # nested DICTIONARY
                    "email": email.strip().lower(),
                    "phone": phone},
    }
    students.append(student)
    return True, f"Student {student['name']} (Roll {roll_no}) added successfully."


def search_student(roll_no):
    """Search by roll number. Returns the student dict or None."""
    return find_student(roll_no)


def update_student(roll_no, field, new_value):
    """
    Update one field of an existing student.
    Allowed fields: name, department, email, phone, address, marks, attendance, clubs
    """
    s = find_student(roll_no)
    if s is None:
        return False, f"No student found with roll number {roll_no}."

    if field == "name":
        if not is_valid_name(new_value):
            return False, "Invalid name."
        s["name"] = new_value.strip().title()
    elif field == "department":
        if new_value.strip().upper() not in DEPARTMENTS:
            return False, "Unknown department."
        s["department"] = new_value.strip().upper()
    elif field == "email":
        if not is_valid_email(new_value):
            return False, "Invalid e-mail ID."
        s["contact"]["email"] = new_value.strip().lower()
    elif field == "phone":
        if not is_valid_phone(new_value):
            return False, "Phone number must contain exactly 10 digits."
        s["contact"]["phone"] = new_value
    elif field == "address":
        if not new_value.strip():
            return False, "Address cannot be empty."
        s["contact"]["address"] = new_value.strip()
    elif field in ("marks", "attendance"):
        if len(new_value) != len(s["subjects"]) or not all(is_valid_percent(v) for v in new_value):
            return False, f"Provide {len(s['subjects'])} values between 0 and 100."
        s[field] = list(new_value)
    elif field == "clubs":
        if not set(new_value) <= CLUBS:
            return False, "Unknown club."
        s["clubs"] = set(new_value)
    else:
        return False, f"Field '{field}' cannot be updated."
    return True, f"Roll {roll_no}: '{field}' updated."


def delete_student(roll_no):
    s = find_student(roll_no)
    if s is None:
        return False, f"No student found with roll number {roll_no}."
    students.remove(s)
    return True, f"Record of roll number {roll_no} deleted."


def average_marks(student):
    """Average marks of ONE student (0 if no marks)."""
    return sum(student["marks"]) / len(student["marks"]) if student["marks"] else 0.0


def class_average():
    """Average of the per-student averages for the whole class."""
    if not students:
        return 0.0
    return sum(average_marks(s) for s in students) / len(students)


def highest_scorer():
    """Student with the highest average marks (None if no records)."""
    if not students:
        return None
    return max(students, key=average_marks)


def list_by_department(department):
    dept = department.strip().upper()
    return [s for s in students if s["department"] == dept]


def count_students():
    """Return total count and a per-department count dictionary."""
    per_dept = {}
    for s in students:
        per_dept[s["department"]] = per_dept.get(s["department"], 0) + 1
    return len(students), per_dept


def grade_of(avg):
    if avg >= 90: return "A+"
    if avg >= 80: return "A"
    if avg >= 70: return "B"
    if avg >= 60: return "C"
    if avg >= 50: return "D"
    return "F"


# ----------------------------------------------------------------------
# Display / report helpers
# ----------------------------------------------------------------------
def format_student(s):
    roll, reg, dob = s["identity"]                      # tuple unpacking
    lines = [
        f"Roll No      : {roll}",
        f"Reg. No      : {reg}",
        f"Date of Birth: {dob[2]:02d}-{dob[1]:02d}-{dob[0]}",
        f"Name         : {s['name']}",
        f"Department   : {s['department']}",
        f"Subjects     : {', '.join(s['subjects'])}",
        f"Marks        : {s['marks']}   (Average {average_marks(s):.2f}, Grade {grade_of(average_marks(s))})",
        f"Attendance % : {s['attendance']}",
        f"Clubs        : {', '.join(sorted(s['clubs'])) or 'None'}",
        f"E-mail       : {s['contact']['email']}",
        f"Phone        : {s['contact']['phone']}",
        f"Address      : {s['contact']['address']}",
    ]
    return "\n".join(lines)


def display_all():
    if not students:
        return "No student records available."
    return ("\n" + "-" * 50 + "\n").join(format_student(s) for s in students)


def generate_report():
    total, per_dept = count_students()
    if total == 0:
        return "REPORT: no records available."
    top = highest_scorer()
    all_clubs = set()
    for s in students:
        all_clubs |= s["clubs"]                         # set union
    lines = [
        "=========== STUDENT REPORT ===========",
        f"Total students     : {total}",
        f"Department-wise    : {per_dept}",
        f"Class average      : {class_average():.2f}",
        f"Highest scorer     : {top['name']} (Roll {top['identity'][0]}, avg {average_marks(top):.2f})",
        f"Clubs in use       : {sorted(all_clubs) or 'None'}",
        "--------------------------------------",
        f"{'Roll':<6}{'Name':<18}{'Dept':<7}{'Avg':>7}  Grade",
    ]
    for s in sorted(students, key=average_marks, reverse=True):
        avg = average_marks(s)
        lines.append(f"{s['identity'][0]:<6}{s['name']:<18}{s['department']:<7}{avg:>7.2f}  {grade_of(avg)}")
    return "\n".join(lines)


# ----------------------------------------------------------------------
# Interactive (console) part
# ----------------------------------------------------------------------
def read_int(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None


def read_float_list(prompt, count):
    parts = input(prompt).replace(",", " ").split()
    try:
        values = [float(p) for p in parts]
    except ValueError:
        return None
    return values if len(values) == count else None


def ui_add():
    roll = read_int("Roll number: ")
    reg = input("Registration number: ").strip()
    try:
        y, m, d = (int(x) for x in input("Date of birth (YYYY-MM-DD): ").split("-"))
    except ValueError:
        print("Invalid date format."); return
    name = input("Name: ")
    dept = input(f"Department {sorted(DEPARTMENTS)}: ")
    address = input("Address: ")
    email = input("E-mail: ")
    phone = input("Phone (10 digits): ")
    subjects = [x.strip().title() if x.strip().lower() != "dbms" else "DBMS"
                for x in input(f"Subjects (comma separated) from {sorted(SUBJECTS)}: ").split(",") if x.strip()]
    marks = read_float_list("Marks (same order): ", len(subjects))
    attendance = read_float_list("Attendance % (same order): ", len(subjects))
    if marks is None or attendance is None:
        print("Invalid marks / attendance."); return
    clubs = {x.strip().title() for x in input(f"Clubs (optional) from {sorted(CLUBS)}: ").split(",") if x.strip()}
    ok, msg = add_student(roll, reg, (y, m, d), name, dept, address, email, phone,
                          subjects, marks, attendance, clubs)
    print(("[OK] " if ok else "[ERROR] ") + msg)


def ui_update():
    roll = read_int("Roll number to update: ")
    field = input("Field (name/department/email/phone/address/marks/attendance/clubs): ").strip().lower()
    s = find_student(roll)
    if s is None:
        print("[ERROR] Student not found."); return
    if field in ("marks", "attendance"):
        value = read_float_list(f"Enter {len(s['subjects'])} values: ", len(s["subjects"]))
        if value is None:
            print("[ERROR] Invalid values."); return
    elif field == "clubs":
        value = {x.strip().title() for x in input("Clubs (comma separated): ").split(",") if x.strip()}
    else:
        value = input("New value: ")
    ok, msg = update_student(roll, field, value)
    print(("[OK] " if ok else "[ERROR] ") + msg)


def main():
    menu = """
===== STUDENT RECORD MANAGEMENT SYSTEM =====
1. Add student            6. Highest scorer
2. Search by roll number  7. List by department
3. Update record          8. Count students
4. Delete record          9. Generate report
5. Display all records    10. Class average
0. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice: ").strip()
        if choice == "1":
            ui_add()
        elif choice == "2":
            roll = read_int("Roll number: ")
            s = search_student(roll) if roll is not None else None
            print(format_student(s) if s else "[ERROR] Student not found.")
        elif choice == "3":
            ui_update()
        elif choice == "4":
            roll = read_int("Roll number: ")
            print(delete_student(roll)[1] if roll is not None else "[ERROR] Invalid roll number.")
        elif choice == "5":
            print(display_all())
        elif choice == "6":
            t = highest_scorer()
            print(f"Highest scorer: {t['name']} (avg {average_marks(t):.2f})" if t else "No records.")
        elif choice == "7":
            found = list_by_department(input("Department: "))
            print("\n".join(f"{s['identity'][0]} - {s['name']}" for s in found) or "No students found.")
        elif choice == "8":
            total, per_dept = count_students()
            print(f"Total: {total}  |  By department: {per_dept}")
        elif choice == "9":
            print(generate_report())
        elif choice == "10":
            print(f"Class average: {class_average():.2f}")
        elif choice == "0":
            print("Goodbye!"); break
        else:
            print("[ERROR] Invalid choice. Enter a number from the menu.")


if __name__ == "__main__":
    main()


# In[ ]:




