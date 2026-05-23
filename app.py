from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import database  # This connects app.py to your database.py file!

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. VIEW ALL STUDENTS
@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

# 2. ADD A STUDENT
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_number = request.form['roll_number']
    course = request.form['course']

    if name and roll_number and course:
        try:
            conn = get_db_connection()
            conn.execute('INSERT INTO students (roll_number, name, course) VALUES (?, ?, ?)',
                         (roll_number, name, course))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            return "Error: This Roll Number already exists!", 400
            
    return redirect(url_for('index'))

# 3. EDIT A STUDENT
@app.route('/edit/<roll_number>', methods=['GET', 'POST'])
def edit_student(roll_number):
    conn = get_db_connection()
    
    if request.method == 'POST':
        new_name = request.form['name']
        new_course = request.form['course']
        
        conn.execute('UPDATE students SET name = ?, course = ? WHERE roll_number = ?',
                     (new_name, new_course, roll_number))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    student = conn.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,)).fetchone()
    conn.close()
    return render_template('edit.html', student=student)

# 4. DELETE A STUDENT
@app.route('/delete/<roll_number>')
def delete_student(roll_number):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    database.init_db()  # Runs the initialization from your database.py file!
    app.run(debug=True)