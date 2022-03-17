from flask import Flask, render_template, redirect, url_for 
import scrape_mars
from flask_pymongo import PyMongo
import json


app  = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/" 
mongo = PyMongo(app)  

@app.route("/")
def index():
    return "index route"

@app.route("/scrape")
def scrape():
    marsTable = mongo.db.marsData  
    # mongo.db.marsData.drop()  
    # test to call scrape_mars.py
    mars_data = scrape_mars.scrape_all() 
    # mars_d = json.dumps(mars_data)
    # print(mars_data)  
    # return mars_data

    marsTable.insert_one(mars_data)
    return mars_data  
    

    
if __name__ == "__main__":
    app.run(port=8000)   