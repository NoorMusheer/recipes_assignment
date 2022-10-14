from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/recipes/new')
def create_new_recipe():
    if not session:
        return redirect('/')
    return render_template('create_recipe.html')

@app.route('/recipe_saved', methods=['POST'])
def recipe_saved():
    if not session:
        return redirect('/')
    data={
            "name":request.form['name'],
            "user_id": session['id'],
            "description":request.form['description'],
            "instructions":request.form['instructions'],
            "date_made":request.form['date_made'],
            "under_thirty":request.form['under_thirty']
        }
    Recipe.new_recipe(data)
    return redirect('/recipes')

@app.route('/recipe_edited', methods=['POST'])
def recipe_edited():
    if not session:
        return redirect('/')
    data={
            "id":request.form['id'],
            "name":request.form['name'],
            "description":request.form['description'],
            "instructions":request.form['instructions'],
            "date_made":request.form['date_made'],
            "under_thirty":request.form['under_thirty']
        }
    Recipe.edit_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>')
def get_recipe_details_page(id):
    if not session:
        return redirect('/')
    chosen_recipe = Recipe.get_recipe_by_id(id)
    return render_template("recipe_details.html", recipe = chosen_recipe)

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if not session:
        return redirect('/')
    recipe_to_edit = Recipe.get_recipe_by_id(id)
    return render_template('edit_recipe.html', recipe = recipe_to_edit)

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    if not session:
        return redirect('/')

    Recipe.delete_recipe(id)
    return redirect('/recipes')
