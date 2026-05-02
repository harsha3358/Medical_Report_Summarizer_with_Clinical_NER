import sqlite3
import json
from datetime import datetime

# -------------------------------
# CONNECTION
# -------------------------------
conn = sqlite3.connect("db.sqlite", check_same_thread=False)
cursor = conn.cursor()

# -------------------------------
# SCHEMA
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    input_text  TEXT    NOT NULL,
    summary     TEXT    NOT NULL,
    entities    TEXT    NOT NULL,
    created_at  TEXT    NOT NULL
)
""")
conn.commit()


# -------------------------------
# SAVE A RESULT
# -------------------------------
def save_result(input_text: str, summary: str, entities: dict) -> None:
    try:
        cursor.execute(
            "INSERT INTO history (input_text, summary, entities, created_at) VALUES (?, ?, ?, ?)",
            (
                input_text[:2000],           # cap to avoid huge blobs
                summary,
                json.dumps(entities),
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
    except Exception as e:
        print("DB SAVE ERROR:", e)


# -------------------------------
# FETCH ALL HISTORY (newest first)
# -------------------------------
def get_all_history() -> list:
    try:
        cursor.execute(
            "SELECT id, input_text, summary, entities, created_at FROM history ORDER BY id DESC"
        )
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "input_text": r[1],
                "summary": r[2],
                "entities": r[3],   # still a JSON string — frontend parses it
                "created_at": r[4],
            }
            for r in rows
        ]
    except Exception as e:
        print("DB FETCH ERROR:", e)
        return []


# -------------------------------
# CLEAR ALL HISTORY
# -------------------------------
def clear_all_history() -> None:
    try:
        cursor.execute("DELETE FROM history")
        conn.commit()
    except Exception as e:
        print("DB CLEAR ERROR:", e)