import sqlite3

def init_db():
    conn = sqlite3.connect("instance/users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        filepath TEXT,
        payload_length INTEGER,
        seed INTEGER,
        private_key TEXT
    )
    """)

    conn.commit()
    conn.close()