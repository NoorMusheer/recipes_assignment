from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile (r'^(?=.*[A-Z])(?=.*[a-z])(?=.*?[0-9]).{8,}$')


class User:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(cls.DB).query_db(query)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result == ():
            return False
        else:
            return result[0]


    @classmethod
    def create_user(cls,user_data):
        data = {
            "first_name" : user_data['first_name'],
            "last_name" : user_data['last_name'],
            "email":user_data['email'],
            "password":bcrypt.generate_password_hash(user_data['password'])
        }
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(), NOW() );"
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_reg(data, user):
        is_valid = True
        if user:
            flash("*E-mail is already registered. Please use a different e-mail address or login. ", 'register')
            is_valid = False
        if len(data['first_name'])<2 or len(data['last_name'])<2 or len(data['email']) <2:
            flash("* A minimum of two characters are required for the first name, last name and e-mail. ", 'register')
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("E-mail format is incorrect. ", 'register')
            is_valid=False
        if not PASSWORD_REGEX.match(data['password']):
            flash("* At least one number, one Upper Case letter, one Lower case letter is required  ", 'register')
            is_valid = False
        if data['password'] != data['password2']:
            flash("*Passwords do not match. ", 'register')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(login_data, user):
        is_valid = True
        if not user:
            flash("*E-mail not found. Please try again, or  register <a href='/'>HERE</a>.", "login")
            is_valid = False
        
        elif not bcrypt.check_password_hash(user['password'], login_data['password']):
            flash("*E-mail and password combination do not match our records. Please try again, or register <a href='/'>HERE</a>.", "login")
            is_valid = False

        return is_valid
