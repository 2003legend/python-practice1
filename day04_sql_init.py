"""
Day4: SQL 入门练习（SQLite）

在 PyCharm 里右键运行本文件，会创建 practice.db 并插入示例数据。
之后用 PyCharm Database 工具或再运行 day04_sql_query.py 练习查询。
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "practice.db")


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 建表
    cur.execute("""
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            city TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE scores (
            id INTEGER PRIMARY KEY,
            student_id INTEGER,
            subject TEXT,
            score INTEGER,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    # 插数据
    students = [
        (1, "李剑东", 22, "沈阳"),
        (2, "张三", 21, "深圳"),
        (3, "李四", 23, "沈阳"),
        (4, "王五", 22, "北京"),
    ]
    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?)", students)

    scores = [
        (1, 1, "数学", 95),
        (2, 1, "英语", 88),
        (3, 2, "数学", 76),
        (4, 3, "数学", 82),
        (5, 3, "英语", 90),
        (6, 4, "数学", 60),
    ]
    cur.executemany("INSERT INTO scores VALUES (?, ?, ?, ?)", scores)

    conn.commit()
    conn.close()
    print(f"数据库已创建: {DB_PATH}")
    print("students 表 4 行, scores 表 6 行")


if __name__ == "__main__":
    init_db()
