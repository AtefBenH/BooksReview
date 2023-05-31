from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user, book
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.author = data['author']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate(data):
        errorMessages = []
        if len(data['title'])<1:
            errorMessages.append("Book Must Have a Title")

        if len(data['author'])<2:
            errorMessages.append("Author must contain at least 2 characters")
        
        if len(data['description'])<5:
            errorMessages.append("Description must contain at least 5 characters")
        return errorMessages

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (user_id, title, author, description) VALUES (%(user_id)s, %(title)s, %(author)s, %(description)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM books JOIN users ON books.user_id = users.id ORDER BY title;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        books =[]
        if results:
            for row in results:
                book = cls(row)
                book.creator = f"{row['first_name']} {row['last_name']}"
                books.append(book)
        else:
            books = 'No Books Yet'
        return books
    
    # - GET ONE BY ID
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM books WHERE id = %(id)s; 
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_books_by_user(cls, data):
        query = """
            SELECT * FROM books JOIN users ON books.user_id = users.id WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        posted_books = []
        for row_from_db in results:
            book_data = {
                "id" : row_from_db["id"],
                "user_id" : row_from_db["users.id"],
                "title" : row_from_db["title"],
                "author" : row_from_db["author"],
                "description" : row_from_db["description"],
                "created_at" : row_from_db["created_at"],
                "updated_at" : row_from_db["updated_at"]
            }
            posted_books.append(book.Book(book_data))
        return posted_books
    
    @classmethod
    def get_books_id_by_user(cls, data):
        query = """
            SELECT books.id FROM books JOIN users ON books.user_id = users.id WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        posted_books_id = []
        if results:
            for row in results:
                posted_books_id.append(row['id'])
        return posted_books_id

    @classmethod
    def update(cls, data):
        query = """
            UPDATE books SET 
            user_id = %(user_id)s, title = %(title)s, author = %(author)s, description = %(description)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_book_with_fav(cls, data):
        query = "SELECT * FROM books JOIN likes ON likes.book_id = books.id LEFT JOIN users ON likes.user_id = users.id WHERE books.id = %(id)s ORDER BY users.first_name;"
        results = connectToMySQL(DATABASE).query_db(query , data)
        lovers = []
        if (len(results)>0):
            for row_from_db in results:
                user_data = {
                    "id" : row_from_db["users.id"],
                    "first_name" : row_from_db["first_name"],
                    "last_name" : row_from_db["last_name"],
                    "email" : row_from_db["email"],
                    "password" : row_from_db["password"],
                    "warning" : row_from_db["warning"],
                    "created_at" : row_from_db["users.created_at"],
                    "updated_at" : row_from_db["users.updated_at"]
                }
                lovers.append(user.User(user_data))
        return lovers
    
    #Add user to the list that favored the Book
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO likes (book_id, user_id) VALUES (%(book_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #Get the unfavorite books for that specific user
    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM likes WHERE user_id = %(id)s );"
        results = connectToMySQL(DATABASE).query_db(query,data)
        unfav_books = []
        for row in results:
            unfav_books.append(cls(row))
        return unfav_books
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #DELETE A BOOK SINCE POSTER IS DELETED
    @classmethod
    def deleteByUser(cls, data):
        query = "DELETE FROM books WHERE user_id = %(user_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #SEARCH BOOK BY FILTER (TITLE, AUTHOR, DESCRIPTION)
    @classmethod
    def search(cls, data):
        query = "SELECT * FROM books WHERE {filter} LIKE %(search)s;"
        results = connectToMySQL(DATABASE).query_db(query.format(filter=data['filter']), data)
        books = []
        for row in results:
            book = cls(row)
            books.append(book)
        return books
    
    #SEARCH BOOK BY POSTER
    @classmethod
    def searchByPoster(cls, data):
        query = """SELECT * FROM books 
            JOIN users ON books.user_id = users.id 
            WHERE users.first_name LIKE %(search)s OR users.last_name LIKE %(search)s;
            """
        results = connectToMySQL(DATABASE).query_db(query, data)
        books = []
        for row in results:
            book = cls(row)
            books.append(book)
        return books
