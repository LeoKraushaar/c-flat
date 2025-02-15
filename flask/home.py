from flask import Flask, Blueprint, render_template
from mongo.mongo_manager import MongoManager
from constants import *

app = Flask(__name__)
mongo = MongoManager(DB)

@app.route("/")
def home():
    return "<p>Welcome to SmartCart!</p>"

@app.route('/pantry')
def pantry():
    items = mongo.queryCollection(ITEMS)
    return render_template(
        'pantry.html',
        n=len(items),
        items=items
    )

@app.route('/get-recipe')
def getRecipe():
    recipes = mongo.queryCollection(RECIPES)
    
