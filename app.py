from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for the homepage (showing the reading list)
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Route to add a book to the reading list
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, status) VALUES (?, ?, ?)',
                     (title, author, 'Not Read'))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Route to mark a book as read
@app.route('/mark_read/<int:book_id>')
def mark_read(book_id):
    conn = get_db_connection()
    conn.execute('UPDATE books SET status = ? WHERE id = ?', ('Read', book_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
