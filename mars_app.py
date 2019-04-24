from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_update
import ssl

# Create an instance of Flask
app = Flask(__name__)
uri = 'mongodb://localhost:27017/mars_app'
# uri = 'mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/<database>?retryWrites=true'

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri=uri)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mars_update.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
