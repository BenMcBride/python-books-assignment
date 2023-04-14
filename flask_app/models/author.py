from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app.models import book

class Author:
    DB = "books_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.favorite_books = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL(cls.DB).query_db(query)
        authors = []
        for i in results:
            authors.append( cls(i) )
        return authors

    @classmethod
    def add_favorite_book(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def save(cls, data ): 
        query = "INSERT INTO authors ( name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result

    @classmethod
    def get_author_fav_books(cls, data):
        query  = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(author_id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        author = cls(results[0])
        for row_from_db in results:
            book_data = {
                'id': row_from_db["id"],
                'title': row_from_db["title"],
                'num_of_pages': row_from_db["num_of_pages"],
                'created_at': row_from_db["created_at"],
                'updated_at': row_from_db["updated_at"]
            }
            author.favorite_books.append( book.Book( book_data ) )
        return author

    @classmethod
    def get_other_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT authors.id FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id WHERE favorites.book_id = %(book_id)s);"
        results = connectToMySQL(cls.DB).query_db(query, data)
        other_authors = []
        for i in results:
            other_authors.append(i)
        return other_authors

    @classmethod
    def update(cls,data):
        query = "UPDATE authors SET name=%(name)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, author_id):
        query  = "DELETE FROM authors WHERE id = %(id)s;"
        data = {"id": author_id}
        return connectToMySQL(cls.DB).query_db(query,data)