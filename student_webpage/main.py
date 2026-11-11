from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="Student CRUD Web Application",
    description="Full CRUD web portal for managing students (Assignment 14)",
    version="1.0.0",
)

html_file = Path(__file__).with_name("index.html")


class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=120)
    course: str = Field(..., min_length=2, max_length=80)
    marks: float = Field(..., ge=0, le=100)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, min_length=5, max_length=120)
    course: Optional[str] = Field(None, min_length=2, max_length=80)
    marks: Optional[float] = Field(None, ge=0, le=100)


class Student(StudentBase):
    id: int


# In-memory storage with seed records
STUDENTS_DB: List[Student] = [
    Student(id=1, name="Aniket Kumar", email="aniket@example.com", course="Python Fullstack", marks=92.0),
    Student(id=2, name="Priya Sharma", email="priya@example.com", course="Data Science", marks=88.5),
    Student(id=3, name="Rahul Verma", email="rahul@example.com", course="Web Development", marks=65.0),
    Student(id=4, name="Sneha Patel", email="sneha@example.com", course="Python Fullstack", marks=94.0),
    Student(id=5, name="Vikram Singh", email="vikram@example.com", course="Machine Learning", marks=46.0),
]
next_id = 6


@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse(html_file, media_type="text/html")


@app.get("/api/students", response_model=List[Student])
def get_all_students(search: Optional[str] = Query(None)):
    if search:
        q = search.lower()
        return [
            s for s in STUDENTS_DB
            if q in s.name.lower() or q in s.email.lower() or q in s.course.lower()
        ]
    return STUDENTS_DB


@app.get("/api/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for s in STUDENTS_DB:
        if s.id == student_id:
            return s
    raise HTTPException(status_code=404, detail="Student not found")


@app.post("/api/students", response_model=Student, status_code=201)
def create_student(payload: StudentCreate):
    global next_id
    new_student = Student(
        id=next_id,
        name=payload.name.strip(),
        email=payload.email.strip(),
        course=payload.course.strip(),
        marks=payload.marks,
    )
    STUDENTS_DB.append(new_student)
    next_id += 1
    return new_student


@app.put("/api/students/{student_id}", response_model=Student)
def update_student(student_id: int, payload: StudentUpdate):
    for i, s in enumerate(STUDENTS_DB):
        if s.id == student_id:
            updated_data = s.model_dump()
            if payload.name is not None:
                updated_data["name"] = payload.name.strip()
            if payload.email is not None:
                updated_data["email"] = payload.email.strip()
            if payload.course is not None:
                updated_data["course"] = payload.course.strip()
            if payload.marks is not None:
                updated_data["marks"] = payload.marks

            updated_student = Student(**updated_data)
            STUDENTS_DB[i] = updated_student
            return updated_student

    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/api/students/{student_id}", status_code=200)
def delete_student(student_id: int):
    for i, s in enumerate(STUDENTS_DB):
        if s.id == student_id:
            deleted = STUDENTS_DB.pop(i)
            return {"message": f"Student '{deleted.name}' deleted successfully", "id": student_id}
    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/api/stats")
def get_stats():
    if not STUDENTS_DB:
        return {"total": 0, "avg": 0, "pass_count": 0, "top_student": "N/A"}
    total = len(STUDENTS_DB)
    marks = [s.marks for s in STUDENTS_DB]
    avg = sum(marks) / total
    passed = sum(1 for m in marks if m >= 50.0)
    top = max(STUDENTS_DB, key=lambda s: s.marks)
    return {
        "total": total,
        "avg": round(avg, 1),
        "pass_count": passed,
        "top_student": f"{top.name} ({top.marks}%)",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)