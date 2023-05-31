from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Blacklist:
    def __init__(self, data):
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO blacklist (email)
            VALUES (%(email)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM blacklist WHERE email = %(email)s; 
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])