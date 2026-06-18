"""
Day4: 在 Python 里执行 SQL 查询

先运行 day04_sql_init.py 创建数据库，再运行本文件看示例。
你也可以在 PyCharm 里打开 practice.db 自己写 SQL。
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "practice.db")


def run_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    # 1. 查全部
    print("=== 全部学生 ===")
    print(run_sql("SELECT * FROM students"))

    # 2. 条件查询
    print("\n=== 沈阳的学生 ===")
    print(run_sql("SELECT name, age FROM students WHERE city = '沈阳'"))

    # 3. 排序
    print("\n=== 按年龄降序 ===")
    print(run_sql("SELECT name, age FROM students ORDER BY age DESC"))

    # 4. JOIN 联表
    print("\n=== 学生姓名 + 成绩 ===")
    sql = """
        SELECT s.name, sc.subject, sc.score
        FROM students s
        JOIN scores sc ON s.id = sc.student_id
        ORDER BY s.name, sc.subject
    """
    print(run_sql(sql))

    # 5. 聚合
    print("\n=== 每人平均分 ===")
    sql = """
        SELECT s.name, AVG(sc.score) AS avg_score
        FROM students s
        JOIN scores sc ON s.id = sc.student_id
        GROUP BY s.id
        HAVING avg_score >= 80
    """
    print(run_sql(sql))

    ##数学成绩 > 80 的学生姓名
    #沈阳有几个学生（COUNT）
    #每人最高分
    #没有成绩的学生（LEFT JOIN）
    #哪门课平均分最高##
    sql="""
        SELECT s.name
        FROM students s
        JOIN scores sc ON s.id = sc.student_id 
        WHERE   sc.subject="数学" and sc.score>80
    """
    print(run_sql(sql))

    sql="""
        SELECT COUNT(*) 
        FROM students 
        WHERE city="沈阳"
    """
    print(run_sql(sql))

    sql="""
        SELECT s.name, MAX(sc.score) AS max_score
        FROM students s
        JOIN scores sc ON s.id=sc.student_id
        GROUP BY s.id
    """
    print(run_sql(sql))

    sql="""
        SELECT s.name
        FROM students s
        JOIN scores sc ON s.id=sc.student_id
        WHERE sc.id IS NULL
    """
    print(run_sql(sql))

    sql="""
        SELECT subject ,AVG(score) as avg_score
        FROM scores 
        GROUP BY subject
        ORDER BY avg_score DESC 
        LIMIT 1
    """
    print(run_sql(sql))