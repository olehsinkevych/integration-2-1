"""A tiny FastAPI application with in-memory storage."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Student API", version="0.1.0")


class Student(BaseModel):
    """Request/response model — validated automatically by Pydantic."""
    id: int
    name: str
    course: str


# In-memory "database". It lives only in the container's memory,
# so it is emptied every time the container restarts.
students: dict[int, Student] = {
    1: Student(id=1, name="Alice", course="Docker 101"),
}


@app.get("/")
def read_root() -> dict:
    """Hello / health endpoint."""
    return {"message": "Hello from FastAPI running inside Docker!"}


@app.get("/students")
def list_students() -> list[Student]:
    return list(students.values())


@app.get("/students/{student_id}")
def get_student(student_id: int) -> Student:
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]


@app.post("/students", status_code=201)
def create_student(student: Student) -> Student:
    students[student.id] = student
    return student