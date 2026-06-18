"""
Day6: FastAPI + SQLite

先确保有数据库（没有就运行一次 day04_sql_init.py），再启动：

    uvicorn day06_fastapi_db:app --reload

然后访问：
    http://127.0.0.1:8000/docs
"""

import os
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="学生管理 API")

DB_PATH = os.path.join(os.path.dirname(__file__), "practice.db")


def get_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=500,
            detail="数据库不存在，请先运行 day04_sql_init.py",
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class StudentCreate(BaseModel):
    name: str
    age: int
    city: str


class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    city: str


@app.get("/")
def read_root():
    return {"message": "学生管理 API", "docs": "/docs"}


@app.get("/students", response_model=list[StudentOut])
def list_students():
    conn = get_db()
    rows = conn.execute("SELECT id, name, age, city FROM students").fetchall()
    conn.close()
    return [dict(row) for row in rows]


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT id, name, age, city FROM students WHERE id = ?",
        (student_id,),
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="学生不存在")
    return dict(row)


@app.post("/students", response_model=StudentOut)
def create_student(student: StudentCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
        (student.name, student.age, student.city),
    )
    conn.commit()
    new_id = cur.lastrowid
    row = conn.execute(
        "SELECT id, name, age, city FROM students WHERE id = ?",
        (new_id,),
    ).fetchone()
    conn.close()
    return dict(row)
