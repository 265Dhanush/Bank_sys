from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def init_mysql_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database_name'
    )
    print("Opened database successfully")

    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("Table created successfully")
    conn.close()

init_mysql_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            conn = mysql.connector.connect(
                host='localhost',
                user='your_username',
                password='your_password',
                database='your_database_name'
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO entries (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
            conn.commit()
            msg = "Record successfully added."
        except Exception as e:
            conn.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            conn.close()
            return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
