import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("summaries.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT,
            summary TEXT,
            created_at TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_summary(input_text: str, summary: str) -> int:
    conn = sqlite3.connect("summaries.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO summaries (input_text, summary, created_at) VALUES (?, ?, ?)",
        (input_text, summary, datetime.now())
    )
    conn.commit()
    summary_id = c.lastrowid
    conn.close()
    return summary_id

def get_summaries():
    conn = sqlite3.connect("summaries.db")
    c = conn.cursor()
    c.execute("SELECT id, input_text, summary, created_at FROM summaries")
    summaries = [{"id": row[0], "input_text": row[1], "summary": row[2], "created_at": row[3]} for row in c.fetchall()]
    conn.close()
    return summaries

init_db()