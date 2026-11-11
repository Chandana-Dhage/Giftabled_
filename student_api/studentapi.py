
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import csv,os


app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    course: str


students={
  1: {"name": "Manisha", "course": "Python"},
  2: {"name": "Shanthi", "course": "Java"},
  3: {"name": "Fardeen", "course": "DBMS"}  
}

# For this local classroom demo.
# here setting the rules so other threat can't interact with our data CORS POLICY MAKES US ALLOW PARTICULAR METHODS, IP'S
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST","DELETE","PUT"],
    allow_headers=["Content-Type"],
)

def save_students():
    with open("students.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["studentId", "name", "course"])

        for student_id, details in students.items():
            writer.writerow([
                student_id,
                details["name"],
                details["course"]
            ])
if os.path.getsize("students.csv") == 0:
    save_students()

def load_students():
    loaded_students = {}

    with open("students.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            student_id = int(row["studentId"])

            loaded_students[student_id] = {
                "name": row["name"],
                "course": row["course"]
            }

    return loaded_students


students = load_students()


@app.get("/students")
def get_students():
    return students


@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"id": student_id, **students[student_id]}


@app.post("/students")
def add_student(student: Student):
    if student.id in students:
        raise HTTPException(
            status_code=400,
            detail="Student ID already exists"
        )
    
    students[student.id] = {
        "name": student.name,
        "course": student.course
    }
    
    save_students()
    print("******I am")
    return {"message":"Student added succesfully","Student":student}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    removed = students.pop(student_id)
    save_students()
    return {
        "message": "Student deleted successfully",
        "deleted": {"id": student_id, **removed}
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    

    students[student_id] = {
        "name": student.name,
        "course": student.course
    }
    save_students()
    return student
