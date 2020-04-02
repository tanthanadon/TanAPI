from flask import Flask
from flask import request, render_template
from flask import jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient

import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pprint

from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

try:
    client = MongoClient("mongodb+srv://thanadon:tan@cluster0-ngydt.mongodb.net/sertis?retryWrites=true&w=majority")
except:   
    print("Could not connect to MongoDB") 

# database
db = client.sertis

# Created or Switched to collection names: card
cards = db.card 

#test to insert data to the data base
@app.route("/")
def test():
    # Print the new record 
    cursor = cards.find() 
    for record in cursor: 
        print(record)
    return "Good Bye"

@app.route('/addCard')
def add_card():
    username = request.args.get('username')
    password = request.args.get('password')

    name = request.args.get('name')
    status = request.args.get('status')
    content = request.args.get('content')
    category = request.args.get('category')
    author = request.args.get('author')

    user = {"username": username,
        "password": password}
    
    card = {"card": name, 
            "status": status, 
            "content": content,
            "category": category,
            "author": author}

    temp = []
    
    with open("card.json", mode="a") as f:
        f.write(json.dumps(card, indent=2))

    return card

@app.route('/updateCard')
def update_card():
    
    username = request.args.get('username')
    password = request.args.get('password')

    name = request.args.get('name')
    status = request.args.get('status')
    content = request.args.get('content')
    category = request.args.get('category')
    author = request.args.get('author')

    user = {"username": username,
        "password": password}
    
    card = {"name": name, 
            "status": status, 
            "content": content,
            "category": category,
            "author": author}

    update_status = "You are not authorized to update card"

    filename = Path('/home/thanadon/TanAPI/data.json')
    data = json.loads(filename.read_text())

    for i in data:
        if(user["name"] == i["author"] and card['name'] == i["name"]):
            i = card
            update_status = "Update success!"
    
    return update_status

@app.route('/deleteCard')
def deleteCard():
    
    username = request.args.get('username')
    password = request.args.get('password')

    name = request.args.get('name')
    status = request.args.get('status')
    content = request.args.get('content')
    category = request.args.get('category')
    author = request.args.get('author')

    user = {"username": username,
        "password": password}
    
    card = {"name": name, 
            "status": status, 
            "content": content,
            "category": category,
            "author": author}

    delete_status = "You are not authorized to deleted card"

    filename = Path('/home/thanadon/TanAPI/data.json')
    data = json.loads(filename.read_text())

    for i in data:
        if(user["name"] == i["author"] and card['name'] == i["name"]):
            delete_status = "Delete success!"
    
    return delete_status

if __name__ == "__main__":
    app.run(debug=True)


