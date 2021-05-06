from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

# HOME PAGE
@app.route('/')
def index():
    # render index html to user
    return render_template('index.html')

# SEARCH DRINK
@app.route('/search', methods=['GET','POST'])
def search():
    # if POST request, search for cocktail name provided by user
    if request.method == 'POST':
        # get drink provided by user
        drink_to_search = request.form['Name']
        # get drink details
        drink_details = searchDrink(drink_to_search)
        # extract drink details
        drink_dictionary = extractDrinkData(drink_details)
        return render_template('displayDrink.html', drink_dictionary=drink_dictionary)
    else:
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
def searchDrink(drinkName):
    response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drinkName)
    json_object = json.loads(response.text)
    # {"drinks":[{
    # "strDrink":"Nutty Irishman",
    # "strInstructions":"Serve over ice",
    # "strDrinkThumb":"https:\/\/www.thecocktaildb.com\/images\/media\/drink\/xspupx1441248014.jpg",
    # "strIngredient1":"Baileys irish cream","strIngredient2":"Frangelico","strIngredient3":"Milk",
    # "strMeasure1":"1 part ","strMeasure2":"1 part ","strMeasure3":"1 part "
    # ]}
    return json_object["drinks"][0]

# EXTRACT DRINK DATA
def extractDrinkData(drink_data): 
    # drink_data = {
        # "strDrink":"Nutty Irishman",
        # "strInstructions":"Serve over ice",
        # "strDrinkThumb":"https:\/\/www.thecocktaildb.com\/images\/media\/drink\/xspupx1441248014.jpg",
        # "strIngredient1":"Baileys irish cream","strIngredient2":"Frangelico","strIngredient3":"Milk",
        # "strMeasure1":"1 part ","strMeasure2":"1 part ","strMeasure3":"1 part "
    # }

    name = drink_data["strDrink"] # Nutty Irishman
    img = drink_data["strDrinkThumb"] + '/preview' # https:\/\/www.thecocktaildb.com\/images\/media\/drink\/xspupx1441248014.jpg
    ingredients_list = []
    count = 1
    while str(drink_data["strIngredient" + str(count)]) != "None":
        # get ingredient
        ingredient = drink_data["strIngredient" + str(count)]
        # get measurement
        measurement = drink_data["strMeasure" + str(count)] or ''
        # ["1 part Baileys irish cream", "1 part Frangelico", "1 park Milk"]
        ingredients_list.append(measurement + ' ' + ingredient)
        count += 1
    instructions = drink_data["strInstructions"] # Serve over ice
    # {'name': "Nutty Irishman", 'img': "https:\/\/www.thecocktaildb.com\/images\/media\/drink\/xspupx1441248014.jpg/preview", 'ingredients_list' : ["1 part Baileys irish cream", "1 part Frangelico", "1 park Milk"], 'instructions': "Serve over ice" }
    drink_dictionary = {'name': name, 'img': img, 'ingredients_list' : ingredients_list, 'instructions': instructions }
    return drink_dictionary

port = int(os.environ.get('PORT', 84))
app.run(host='0.0.0.0', port=port)