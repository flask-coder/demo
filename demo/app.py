from flask import Flask, render_template
import os
import requests # API tool
import json

# CREATE APP
app = Flask(__name__)

# SPINNER ROUTE
@app.route('/spinner')
def spinner():
    drink_data = getRandomDrink()
    drink_object = extractDrinkData(drink_data)
    # display html with drink details
    return render_template('spinner.html', drink_dictionary=drink_object)

def getRandomDrink():
    random_drink_data = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    # tell python it's json
    json_object = json.loads(random_drink_data.text)
    # we want 1st drink in list
    drink_data = json_object["drinks"][0]
    return drink_data

def extractDrinkData(drink_data):
    # get name of drink
    name = drink_data['strDrink'] 
    # get instructions
    instructions = drink_data['strInstructions']
    # get image
    img = drink_data['strDrinkThumb'] + '/preview'
    # get ingredient
    ingredients_list = getIngredientsList(drink_data)
    # group data into a dictionary
    drink_object = {'drink_name': name, 'drink_img': img, 'instructions': instructions, 'ingredient': ingredients_list}
    return drink_object

# get ingredients list
def getIngredientsList(drink_data):
    count = 1
    ingredients_list = []
    while str(drink_data["strIngredient" + str(count)]) != "None":
        # get ingredient
        ingredient = drink_data["strIngredient" + str(count)]
        # get measurement
        measurement = drink_data["strMeasure" + str(count)] or ''
        # add measurement and ingredient to ingredients list
        ingredients_list.append(measurement + ' ' + ingredient)
        count += 1
    return ingredients_list

# RUN APP
port = int(os.environ.get('PORT', 82))
app.run(host='0.0.0.0', port=port)