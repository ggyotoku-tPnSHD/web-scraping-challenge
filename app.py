from flask_pymongo import PyMongo
import scrape
from flask import Flask, render_template, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_data=mars_dict)


@app.route("/scrape")
def scrape_():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape.get_featured_image()
    mars_data = scrape.get_facts()
    mars_data = scrape.get_hemispheres()
    mars_data = scrape.get_news()
    mars_dict.insert_one(mars_data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


