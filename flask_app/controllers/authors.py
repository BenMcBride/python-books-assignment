from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.book import Book
from flask_app.models.author import Author

@app.route('/')
def index():
    return redirect('/authors')

@app.route("/authors")
def authors():
    authors = Author.get_all()
    return render_template("authors.html", all_authors = authors)

@app.route('/create_author', methods=["POST"])
def create_author():
    data = {
        "name": request.form["name"],
    }
    Author.save(data)
    return redirect('/authors')

@app.route('/authors/add_favorite/<int:author_id>', methods=['POST'])
def add_favorite(author_id):
    data = {
        'book_id': request.form['book_id'],
        'author_id': author_id
    }
    Author.add_favorite_book(data)
    return redirect(f'/authors/{author_id}')

@app.route('/authors/<int:author_id>')
def show_author(author_id):
    author = {
        'author_id': author_id,
        }
    author_obj = Author.get_author_fav_books(author)
    other_books = Book.get_other_books(author)
    return render_template("show_author.html", author_id = author_id, author_name = author_obj.name, other_books = other_books, fav_books = author_obj.favorite_books)