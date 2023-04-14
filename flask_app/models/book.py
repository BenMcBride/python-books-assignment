from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app.models import author


class Book:
    DB = "books_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.favorited_by = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM books;"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for i in results:
            books.append( cls(i) )
        return books

    @classmethod
    def get_one(cls, book_id):
        query  = "SELECT * FROM books WHERE id = %(id)s;"
        data = {'id':book_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data): 
        query = "INSERT INTO books ( title, num_of_pages , created_at, updated_at ) VALUES ( %(title)s,  %(num_of_pages)s , NOW() , NOW() );"
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result

    @classmethod
    def get_other_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT books.id FROM books LEFT JOIN favorites ON books.id = favorites.book_id WHERE favorites.author_id = %(author_id)s);"
        results = connectToMySQL(cls.DB).query_db(query, data)
        list_of_books = []
        for result in results:
            list_of_books.append(result)
        return list_of_books

    @classmethod
    def get_book_with_authors(cls, data):
        query  = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(book_id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        book = cls(results[0])
        for row_from_db in results:
            author_data = {
                'id': row_from_db["id"],
                'name': row_from_db["name"],
                'created_at': row_from_db["created_at"],
                'updated_at': row_from_db["updated_at"]
            }
            book.favorited_by.append( author.Author(author_data) )
        return book

    @classmethod
    def update(cls,data):
        query = "UPDATE books SET title=%(title)s,num_of_pages=%(num_of_pages)s, WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, book_id):
        query  = "DELETE FROM books WHERE id = %(id)s;"
        data = {"id": book_id}
        return connectToMySQL(cls.DB).query_db(query,data)