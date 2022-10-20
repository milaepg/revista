from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class User:
    db_name = 'magazine_subscriptions'


    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        return cls(connectToMySQL(cls.db_name).query_db(query, data)[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        all_users = []
        for u in results:
            all_users.append(cls(u))
        return all_users

    @staticmethod
    def validate_registration(user):
        is_valid = True  
        if len(user['first_name']) < 3:
            flash("The first name must be at least 3 characters.", "danger")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("The last name must be at least 3 characters.", "danger")
            is_valid = False
        if len(user['email']) < 3:
            flash("The email must be at least 3 characters.", "danger")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            "email": user['email']
            }
        email_result = connectToMySQL('magazine_subscriptions').query_db(query, data)
        
        if len(email_result) >= 1:
            flash("Email is already used. Please sign in or register with different email.", "danger")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", "danger")
            is_valid = False
            
        if not user['password'] == user['password2']:
            flash("The password must match and be at least 8 characters long, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
            is_valid = False
        if not re.match(password_pattern, user['password']):
            flash("The password must match and be at least 8 characters long, and contain at least one each of the following: one upper, one lower, one digit and one special character.", "danger")
            is_valid = False
        return is_valid 
    @staticmethod
    def validate_account(user):
        is_valid = True 
        if len(user['first_name']) < 3:
            flash("The first name must be at least 3 characters.", "danger")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("The last name must be at least 3 characters.", "danger")
            is_valid = False
        if len(user['email']) < 3:
            flash("The email must be at least 3 characters.", "danger")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is not valid!", "danger")
            is_valid = False
            return is_valid
        return is_valid 
   
        