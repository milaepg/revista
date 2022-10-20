from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import users_models 

class Magazine:
    db_name = 'magazine_subscriptions'
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
       
        

    @classmethod
    def create_magazine(cls,data):
        query = "INSERT INTO magazines (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def subscribe(cls,data):
        query = "INSERT INTO subscription (user_id, magazine_id) VALUES (%(user_id)s, %(id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data) 


    @classmethod
    def update_magazine(cls,data):
        query = "UPDATE magazines SET title=%(title)s, description=%(description)s, WHERE magazines.id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def delete_magazine(cls,data):
        query = "DELETE FROM magazines WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data) 

    @classmethod
    def unsubscribe(cls,data):
        query = "DELETE FROM subscription WHERE user_id=%(user_id)s AND magazine_id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_form(magazine):
        is_valid = True 
        if len(magazine['title']) < 3:
            flash("The Title must be at least 3 characters.", "danger")
            is_valid = False
        if len(magazine['description']) < 15:
            flash("The description must be at least 15 characters.", "danger")
            is_valid = False
        return is_valid 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM magazines;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_magazines = []
        for row in results:
            all_magazines.append( cls(row) )
        return all_magazines 

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM magazines WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )
    @classmethod
    def get_count(cls):
        query = "select count(distinct(user_id)) as NUMERO_SUSCRITOS, magazine_id, user_id FROM subscription  ;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_magazines = []
        for row in results:
            all_magazines.append( cls(row) )
        return all_magazines 