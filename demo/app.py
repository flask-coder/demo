# IMPORT
from flask import Flask, render_template
import requests
import json
import os

# CREATE APP
app = Flask(__name__)

# SPINNER ROUTE
@app.route('/spinner')
# create spinner method - this will be run when you go to /spinner
def spinner():
    drink_data = getRandomDrink()
    drink_object = extractDrinkData(drink_data)
    # return text to user
    return render_template('spinner.html', drink_object=drink_object)

def getRandomDrink():
    random_drink_data = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    # load as json
    json_object = json.loads(random_drink_data.text)
    # extract 1st drink in list
    drink_data = json_object["drinks"][0]
    return drink_data

def extractDrinkData(drink_data):
    # get name
    name = drink_data["strDrink"]
    img = drink_data['strDrinkThumb'] + '/preview'
    instructions = drink_data['strInstructions']
    ingredient_1 = drink_data['strIngredient1']
    drink_object = {'name': name, 'img': img, 'instructions': instructions, 'ingredient': ingredient_1}
    return drink_object
    

# RUN APP
# run app on 82 port - binding to host 0.0.0.0
port = int(os.environ.get('PORT', 82))
app.run(host='0.0.0.0', port=port)