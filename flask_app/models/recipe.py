from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Recipe:
    DB = "recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.user_id = data['user_id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        return connectToMySQL(cls.DB).query_db(query)

    @classmethod
    def get_recipe_by_id(cls,id):
        data={"id":id}
        query ="SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result[0]

    @classmethod
    def get_basic_recipe_info(cls):
        query = "Select users.id, recipes.id as recipeID, name, under_thirty, first_name, last_name FROM recipes JOIN users ON recipes.user_id = users.id;"
        return connectToMySQL(cls.DB).query_db(query)

    @classmethod
    def new_recipe(cls,data):
        query = "INSERT INTO recipes (name, user_id, description, instructions, date_made, under_thirty) VALUES (%(name)s,%(user_id)s, %(description)s, %(instructions)s, %(date_made)s, %(under_thirty)s); "
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def edit_recipe(cls,data):
        query = """
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made =%(date_made)s, under_thirty=%(under_thirty)s 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_recipe(cls, id):
        data={"id": id}
        query ="DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)