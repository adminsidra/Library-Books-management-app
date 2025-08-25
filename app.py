from flask import Flask, render_template, request, redirect
import mysql.connector
from dotenv import load_dotenv
import os

# Load secrets from .env
load_dotenv()

app = Flask(__name__)

# Get DB credentials from environment
con = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cur = con.cursor()

# --- Your existing functions ---
def list_books():
    cur.execute("SELECT * FROM books")
    return cur.fetchall()

def add_book(title, author, status, rating):
    cur.execute("INSERT INTO books (title, author, status, rating) VALUES (%s, %s, %s, %s)",
                (title, author, status, rating,))
    con.commit()

def upd_book(book_id, new_title, new_author, new_status, new_rating):
    cur.execute("UPDATE books SET title=%s, author=%s, status=%s, rating=%s WHERE id=%s",
                (new_title, new_author, new_status, new_rating, book_id))
    con.commit()

def del_book(book_id):
    cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
    con.commit()

# --- Web routes ---
@app.route('/')
def home():
    books = list_books()
    return render_template("index.html", books=books)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    author = request.form['author']
    status = request.form['status']
    rating = request.form['rating']
    add_book(title, author, status, rating)
    return redirect('/')

@app.route('/update/<int:book_id>', methods=['POST'])
def update(book_id):
    title = request.form['title']
    author = request.form['author']
    status = request.form['status']
    rating = request.form['rating']
    upd_book(book_id, title, author, status, rating)
    return redirect('/')

@app.route('/delete/<int:book_id>')
def delete(book_id):
    del_book(book_id)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
