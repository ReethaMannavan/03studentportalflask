import sqlite3

def init_db():
    conn = sqlite3.connect("student_portal.db")
    cur = conn.cursor()

    # ---- Students Table ----
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        course TEXT NOT NULL,
        address TEXT NOT NULL,
        status TEXT DEFAULT 'Pending'
    )''')

    # ---- Admin Table ----
    cur.execute('''CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    # Default admin
    cur.execute("SELECT * FROM admin WHERE username = ?", ("admin",))
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin123"))

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_db()
