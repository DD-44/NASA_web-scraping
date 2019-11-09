# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import mars_scrape

# Flask Setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Flask Routes
# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    # mars = mongo.db.mars.find_one()
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = mars_scrape.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


# app Run
if __name__ == "__main__":
    app.run(debug=True)
