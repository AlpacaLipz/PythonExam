from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# =========== Create User ==================

    @classmethod
    def create(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(DATABASE).query_db(query, data)
    
#=============== Get One  - get by id -===================== 
# any time you have a select you have results

    @classmethod
    def get_one_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if len(results) < 1 :
            return False
        
        return User(results[0])

#=============== Get One  - get by email -===================== 

    @classmethod
    def get_one_by_email(cls, data):
        query = 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if not results:
            return False
        
        return User(results[0])
    
# =========== Form Validation =================

    @staticmethod
    def validate(data):
        is_valid = True

        if len(data['first_name']) < 1:
            is_valid = False
            flash("First Name Required")

        if len(data['last_name']) < 1:
            is_valid = False
            flash("Last Name Required")

        if len(data['email']) < 1:
            is_valid = False
            flash("Email Required")
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        else: 
            data_for_email = {
                'email' : data['email']
            }
            maybe_user = User.get_one_by_email(data_for_email)
            if maybe_user:
                is_valid = False
                flash('Email Already Exists, Better Luck Next Time')

        if len(data['password']) <  1:
            is_valid = False
        elif not data['password'] == data['confirm_password']:
            is_valid = False
            flash("Passwords Don't Match")

        return is_valid