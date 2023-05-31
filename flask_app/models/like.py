from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Like:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.book_id = data['book_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #CREATE A LIKE
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO likes (user_id, book_id)
            VALUES (%(user_id)s, %(book_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #! GET ALL THE BOOKS ID'S LIKED BY ONE USER
    @classmethod
    def get_books_id_for_user(cls, data):
        liked_books_id = []
        query = """SELECT books.id FROM books 
        JOIN likes 
        ON books.id = likes.book_id
        JOIN users
        ON likes.user_id = users.id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        for row in results:
            liked_books_id.append(row['id'])
        return liked_books_id
    
    #DELETE A LIKE SINCE BOOK DELETED
    @classmethod
    def deleteByBook(cls, data):
        query = "DELETE FROM likes WHERE book_id = %(book_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #DELETE A LIKE SINCE USER DELETED
    @classmethod
    def deleteByUser(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #DELETE A LIKE
    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND book_id = %(book_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #COUNT OF LIKES FOR ONE BOOK
    @classmethod
    def count_for_book(cls, data):
        query = "SELECT count(*) AS likes FROM likes WHERE book_id = %(book_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    #COUNT OF LIKES FOR ONE USER
    @classmethod
    def count_for_user(cls, data):
        query = "SELECT count(*) AS likes FROM likes WHERE user_id = %(user_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result
    
    
