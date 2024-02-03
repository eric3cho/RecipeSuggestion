from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

app = Flask(RecipeFinder)
API_KEY = '7a5c500411dc4f1989d2a217f34ff498'


# route for home button
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html', recipes=[], search_query='')


# main route for app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':    # if form submitted
        query = request.form.get('search_query', '')
        recipes = search_recipes('query')   # perform search for recipes with query

        return render_template('index.html', recipes=recipes, search_query=query)

    search_query = request.args.get('search_query', '')     # no form submitted
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('index.html', recipes=recipes, search_query=decoded_search_query)

def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': API_KEY,
        'query': query
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation'
    }