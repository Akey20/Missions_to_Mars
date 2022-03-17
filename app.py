from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app  = Flask(__name__)

@app.route("/")
def index():
    return "index route"

@app.route("/scrape")
def scrape():
     #test to call scrape_mars.py
    mars_data = scrape_mars.scrape_all()
    #print(mars_data)  
    return mars_data
    

    
if __name__ == "__main__":
    app.run()   