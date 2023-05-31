from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.book_id = data['book_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(data):
        if len(data['content'])<2:
            return False
        return True
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO comments (user_id, book_id, content)
            VALUES (%(user_id)s, %(book_id)s, %(content)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def getAllByBook(cls, data):
        query = """
            SELECT * FROM users
            JOIN comments ON users.id = comments.user_id 
            WHERE comments.book_id = %(book_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #DELETE A LIKE SINCE USER DELETED
    @classmethod
    def deleteByUser(cls, data):
        query = "DELETE FROM comments WHERE user_id = %(user_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #DELETE A LIKE SINCE BOOK DELETED
    @classmethod
    def deleteByBook(cls, data):
        query = "DELETE FROM comments WHERE book_id = %(book_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)