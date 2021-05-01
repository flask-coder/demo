from flask import Flask
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    drink = getRandomDrink()
    return formatResults(drink)

def getRandomDrink():
    response = requests.get("http://www.thecocktaildb.com/api/json/v1/1/random.php")
    json_object = json.loads(response.text)
    return json_object["drinks"][0]

def formatResults(drink):
    name = drink["strDrink"]
    formatted = "<H1>Glenn's next drink: " + name + "</H1>"
    formatted += '<p><img src=' + drink["strDrinkThumb"] + '/preview>'
    formatted += '<ul>'
    count = 1
    while str(drink["strIngredient" + str(count)]) != "None":
        formatted += '<li>' + drink["strIngredient" + str(count)] + '</li>'
        count += 1
    formatted += '</ul>'
    formatted += '<p><button onClick="window.location.reload();">Give Me Another!</button>'
    return formatted

port = int(os.environ.get('PORT', 84))
app.run(host='0.0.0.0', port=port)
