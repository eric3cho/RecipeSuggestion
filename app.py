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
    if request.method == 'POST':
        query = request.form.get('search_query', '')