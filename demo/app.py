# IMPORT
from flask import Flask, render_template
import requests
import json
import os

# CREATE APP
app = Flask(__name__)

# SPINNER ROUTE
@app.route('/spinner')
# this is a method!
def spinner():
    drink_data = getRandomDrink()
    drink_obj = extractDrinkData(drink_data)
    # display html to the user
    return render_template('spinner.html', drink_obj=drink_obj)

def getRandomDrink():
    random_drink_data = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    # tell python the data is in json
    json_object = json.loads(random_drink_data.text)
    # extract 1st drink in the list
    data = json_object["drinks"][0]
    return data

def extractDrinkData(data):
    # get name
    name = data["strDrink"]
    instructions = data["strInstructions"]
    ingredient_1 = data['strIngredient1']
    image = data['strDrinkThumb'] + '/preview'
    # create a drink objects
    drink_object = {'drink_name': name, 'drink_img': image, 'instructions': instructions, 'ingredient': ingredient_1}
    return drink_object

# RUN APP
# run the flask application - we can specify a port number
port = int(os.environ.get('PORT', 82))
app.run(host='0.0.0.0', port=port)