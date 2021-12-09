from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
mars_db = mongo.db.mars

# Rout to render index.html template using data from Mongo
@app.route("/")
def index():
    mars = mars_db.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    # run the scrape function
    mars_database = mongo.db.marsdata
    mars_information = scrape_mars.scrape()
    # update the Mongo database using update and upsert=true
    mars_database.update({}, mars_information, upsert=True)
    return redirect('/')

# Redirect back to home page
    # return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)