import csv
import json


class Student:
    def __init__(self, name, marks):
        self.name = name
        self.__marks = 0
        self.set_marks(marks)

    def set_marks(self, marks):
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100")
        self.__marks = marks

    def get_marks(self):
        return self.__marks

    def __str__(self):
        return f"{self.name}: {self.__marks}"


students = [
    Student("Chandana",54),
    Student("Aruna", 66),
    Student("Bhuvan", 42),
]

for student in students:
    print(student)

try:
    students[0].set_marks(150)
except ValueError as e:
    print("Validation:", e)

records = [{"name": s.name, "marks": s.get_marks()} for s in students]

with open("students.txt", "w", encoding="utf-8") as f:
    for row in records:
        f.write(f"{row['name']} {row['marks']} \\n ")

with open("students.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "marks"])
    writer.writeheader()
    writer.writerows(records)

with open("students.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

for filename in ["students.txt", "students.csv", "students.json"]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            print(f"--- {filename} ---")
            print(f.read())
    except FileNotFoundError:
        print("File not found:", filename)
    except ValueError:
        print("Invalid value in:", filename)
    finally:
        print("File operation finished.")