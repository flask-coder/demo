from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

# SEARCH DRINK
@app.route('/search', methods=['GET','POST'])
def search():
    # if POST request, search for cocktail name provided by user
    if request.method == 'POST':
        # get drink provided by user
        drink_to_search = request.form['Name']
        # get drink details
        drink_details = getDrink(drink_to_search)
        # extract drink details
        drink_dictionary = extractDrinkData(drink_details)
        return render_template('displayDrink.html', drink_dictionary=drink_dictionary)
    else:
        # render search drink
        return render_template('searchDrink.html')

# RANDOM DRINK
@app.route('/random')
def random():
    drink = getRandomDrink()
    drink_dictionary = extractDrinkData(drink)
    return render_template('displayRandomDrink.html', drink_dictionary=drink_dictionary)

# API - GET RANDOM DRINK
def getRandomDrink():
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/random.php")
    json_object = json.loads(response.text)
    return json_object["drinks"][0]

# API - SEARCH DRINK
def getDrink(drinkName):
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drinkName)
    json_object = json.loads(response.text)
    return json_object["drinks"][0]

# EXTRACT DRINK DATA
def extractDrinkData(drink_data): 
    # drink_data = {
    name = drink_data["strDrink"]
    img = drink_data["strDrinkThumb"] + '/preview'
    ingredients_list = []
    count = 1
    while str(drink_data["strIngredient" + str(count)]) != "None":
        # get ingredient
        ingredient = drink_data["strIngredient" + str(count)]
        # get measurement
        measurement = drink_data["strMeasure" + str(count)] or ''
        # add measurement and ingredient to ingredients list
        ingredients_list.append(measurement + ' ' + ingredient)
        count += 1
    instructions = drink_data["strInstructions"] # Serve over ice
    # create a drink dictionary containing name, image, ingredients list and instructions
    drink_dictionary = {'name': name, 'img': img, 'ingredients_list' : ingredients_list, 'instructions': instructions }
    return drink_dictionary

port = int(os.environ.get('PORT', 82))
app.run(host='0.0.0.0', port=port)