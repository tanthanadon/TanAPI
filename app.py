from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import session, redirect, url_for

from pymongo import MongoClient


import os
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pprint


from bson.json_util import dumps
from bson import ObjectId

from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__)

app.secret_key = "sertis"

client = MongoClient("mongodb+srv://thanadon:tan@cluster0-ngydt.mongodb.net/sertis?retryWrites=true&w=majority")

# database
db = client.sertis

# Created or Switched to collection names: card
cards = db.card 

# Created or Switched to collection names: card
users = db.user

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = {"username": username, "password": password}

    if(users.find_one(user) != None):
        session['username'] = username
        # Retunr the results from MongoDB to index.html (cards is a name of variable in index.html page)
        return redirect(url_for('index'))
    else:
        return "<h1>Login Failed!. Please check your username or password</h1>"

@app.route("/index")
def index():
    username = session['username']
    # Find the current cards of user
    results = cards.find({"author": username})
    session['username'] = username
    # Retunr the results from MongoDB to index.html (cards is a name of variable in index.html page)
    return render_template("index.html", cards=results, user=session['username'])

@app.route("/register")

def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    user = {"username": username, "password": password}
    
    if(users.find_one({"username": username}) == None):
        users.insert_one(user)
        print(user)
        print("{0},{1}".format(username, password))
        return render_template('index.html')
    else:
        return "<h1>Registeration Failed!. This account is already existed</h1>"


@app.route("/addCard")

def addCard():
    return render_template("add.html", user=session['username'])

@app.route('/addCard', methods=['POST'])
def addCard_post():
    name = request.form['name']
    status = request.form['status']
    content = request.form['content']
    category = request.form['category']
    author = session['username']

    card = {"name": name, 
            "status": status, 
            "content": content,
            "category": category,
            "author": author}
        
    if(cards.find_one({'name': card['name']}) == None):
        cards.insert_one(card)
        return render_template('add_status.html', add_status=True)
    else:
        return render_template('add_status.html', add_status=False)

@app.route('/update', methods=['POST'])
def update():
    card_name = request.form['card_name']
    if(cards.find_one({'name': card_name}) != None):
        # print(cards['_id'])
        card = cards.find_one({'name': card_name})
        return render_template("update.html", user=session['username'], card=card, card_id=card.get('_id'), check=True)
    else:
        return render_template("update.html", user=session['username'], card=card, card_id=card.get('_id'), check=False)

@app.route('/updateCard', methods=['POST'])
def updateCard():

    card_name = request.form['card_name']
    # card_id = request.form['card_id']

    name = request.form['name']
    status = request.form['status']
    content = request.form['content']
    category = request.form['category']
    author = session['username']

    new_card = {"name": name, 
        "status": status, 
        "content": content,
        "category": category,
        "author": author}
    
    # return old_card_name
    result = cards.replace_one({"name": card_name}, new_card)
    
    if(result.matched_count>0):
        return render_template("update_status.html", user=session['username'], card=new_card, update_status=True)
    else:
        return render_template("update_status.html", user=session['username'], card=new_card, update_status=False)

@app.route('/delete', methods=['POST'])
def delete():
    card_name = request.form['card_name']
    
     # return old_card_name
    result = cards.delete_one({"name": card_name})
    
    if(result.deleted_count==1):
        return render_template("delete_status.html", delete_status=True)
    else:
        return render_template("delete_status.html", delete_status=False)


if __name__ == "__main__":
    app.run(debug=True)


