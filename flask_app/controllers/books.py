from flask_app import app
from flask import render_template,redirect,request
from flask_app.models.book import Book
from flask_app.models.author import Author

@app.route('/books')
def new_book():
    books = Book.get_all()
    return render_template("books.html", all_books = books)

@app.route('/books/add_favorite/<int:book_id>', methods=['POST'])
def add_author_favorite_to_book(book_id):
    favBook = {
        'book_id': book_id,
        'author_id': request.form['author_id']
    }
    Author.add_favorite_book(favBook)
    return redirect(f'/books/{book_id}')

@app.route('/create_book', methods=["POST"])
def create_book():
    data = {
        "title": request.form["title"],
        "num_of_pages" : request.form["num_of_pages"],
    }
    Book.save(data)
    return redirect('/books')


@app.route('/books/<int:book_id>')
def show(book_id):
    book = {
        'book_id': book_id,
        }
    book_obj = Book.get_book_with_authors(book)
    other_authors = Author.get_other_authors(book)
    return render_template("show_book.html", book_id = book, book_title = book_obj.title, other_authors = other_authors, fav_authors = book_obj.favorited_by)