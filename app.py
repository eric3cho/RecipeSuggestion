from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

app = Flask(__name__)
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
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }
    response = requests.get(url, params=params)     # send GET request to API with query params
    if response.status_code == 200:     # if API call is successful
        data = response.json()      # parse API response as JSON data
        return data['results']      # return list of recipe results
    return []

# route to view specific recipe
@app.route('/recipe/<int:recipe_id')
def view_recipe(recipe_id):
    search_query = request.args.get('search_query', '')     # get search query from URL
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'    # build url to get specific recipe
    params = {
        'apiKey': API_KEY,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe was not found", 404


if __name__ == '__main__':
    app.run(debug=True)