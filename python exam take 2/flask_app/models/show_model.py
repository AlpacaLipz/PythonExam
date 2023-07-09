from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import login_model
from flask import flash

from flask import flash

class Show:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']


        # Create Meth

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO shows (title, network, release_date, description, users_id) VALUES (%(title)s , %(network)s , %(release_date)s,%(description)s , %(users_id)s);'
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # get all join method
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM shows JOIN users ON users.id = shows.users_id;'
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_shows = []
        if results:
            for row in results:
                this_show = cls(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = login_model.User(user_data)
                this_show.poster = this_user
                all_shows.append(this_show)
        return all_shows
    

    # get one method

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM shows JOIN users ON users.id = shows.users_id WHERE shows.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            that_show = cls(results[0])
            row = results[0]
            user_data = {
                **row,
                'id' : row['users_id'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            this_user = login_model.User(user_data)
            that_show.poster = this_user
            return that_show
        return False

    # update method

    @classmethod
    def update_show(cls, data):
        query = 'UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query,data)
    
    # ==================  Delete =========================

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM shows WHERE id = %(id)s;'
        return connectToMySQL(DATABASE).query_db(query,data)


    # Validator 
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['title']) < 2:
            is_valid = False
            flash('This show Needs a title......')

        if len(form_data['network']) < 2:
            is_valid = False
            flash('What Network is it on?')

        if len(form_data['description']) < 2:
            is_valid = False
            flash('Describe your Show or Else')
        return is_valid

