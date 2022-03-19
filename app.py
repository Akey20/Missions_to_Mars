from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
# 127.0.0.1:5000
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)
# Route to render index.html template using data from Mongo

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_info_data = scrape_mars.scrape_info()

    # Insert the record
    mongo.db.mars.update_one({}, {"$set": mars_info_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
