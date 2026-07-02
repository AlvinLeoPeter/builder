import sqlite3

def init_db():
    conn = sqlite3.connect('explanations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS explanations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            explanation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_explanation(code, explanation):
    conn = sqlite3.connect('explanations.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO explanations (code, explanation) VALUES (?, ?)',
                   (code, explanation))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('explanations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, code, explanation, timestamp FROM explanations ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows