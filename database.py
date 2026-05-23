import sqlite3

def init_db():
    # This creates/connects to students.db
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    
    # Creates the table with the correct column names
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with correct columns!")

if __name__ == '__main__':
    init_db()