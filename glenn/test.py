from flask import Flask
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Yay! Heroku works!!"

port = int(os.environ.get('PORT', 84))
app.run(host='0.0.0.0', port=port)
