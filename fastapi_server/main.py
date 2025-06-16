from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

app = FastAPI()
DB_NAME = "tasks.db"

class TaskCreate(BaseModel):
    name: str
    deadline: str  # ДД.ММ.ГГГГ

class Task(TaskCreate):
    id: int

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                deadline TEXT NOT NULL
            )
        ''')

@app.on_event("startup")
def startup():
    init_db()

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("SELECT id, name, deadline FROM tasks").fetchall()
        return [Task(id=row[0], name=row[1], deadline=row[2]) for row in rows]

@app.post("/tasks", response_model=Task)
def add_task(task: TaskCreate):
    try:
        datetime.strptime(task.deadline, "%d.%m.%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты.")
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (name, deadline) VALUES (?, ?)", (task.name, task.deadline))
        return Task(id=cur.lastrowid, **task.dict())

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return {"detail": "Удалено"}
