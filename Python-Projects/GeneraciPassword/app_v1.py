import sqlite3
from flask import Flask, request

app = Flask(__name__)
db_name = 'test.db'

@app.route('/')
def index():
    return 'Welcome to version 1 - Plain Text Passwords! <br>'

# Signup endpoint
@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN
              (username TEXT PRIMARY KEY NOT NULL,
              password TEXT NOT NULL);''')
    conn.commit()
    try:
        c.execute('INSERT INTO USER_PLAIN (username, password) VALUES (?, ?)', 
                  (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return 'Username has been registered!'
    return 'Signup success!'

# Login endpoint
def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = 'SELECT password FROM USER_PLAIN WHERE username = ?'
    c.execute(query, (username,))
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == password

@app.route('/login/v1', methods=['POST'])
def login_v1():
    if verify_plain(request.form['username'], request.form['password']):
        return 'Login success!'
    return 'Invalid username/password!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')

