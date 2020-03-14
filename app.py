import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template, redirect, request, jsonify
from config import postgres_pw

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data.sqlite'
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#################################################
# Database Setup
#################################################
# engine = create_engine(f'postgresql://postgres:{postgres_pw}@localhost:5432/city_transit_db')
engine = create_engine(f'postgres://aqspxgjztkrwou:231ae060d1b99f6902564e284dc3e92cce3211701743150d56804e2b932be2a0@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d16mlrnprqss9t')
# engine = create_engine(f'sqlite:///data.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Base.metadata.create_all(engine)

# Save reference to the table
# Cities = Base.classes.cities
# Tracks = Base.classes.tracks

# Main.__table__.create(bind = engine, checkfirst = True)
# MainJSON.__table__.create(bind = engine, checkfirst = True)


# Base.metadata.create_all(engine)

# def recreate_database():
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)

#################################################
# Global Functions
#################################################

def table_join():
    """Return a list of transit system data including the city name, country, and track length"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Join the tables in a query
    sel = [Cities.city_id, Cities.city_name, Cities.country, Tracks.length]
    results = session.query(*sel).join(Tracks, Cities.city_id == Tracks.city_id).order_by(Tracks.length.desc())

    # Return a query object
    return results

def json_dict(results):
    """JSONify results with keys"""
    city_list = []

    # Create a dictionary from each result and append to a list
    for city_id, city_name, country, length in results:
        city_dict = {}
        city_dict["city_id"] = city_id
        city_dict["city_name"] = city_name
        city_dict["country"] = country
        city_dict["track_length"] = length
        city_list.append(city_dict)

    return jsonify(city_list)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    return render_template("index.html")
# def welcome():
#     """List all available api routes"""
#     return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/transit_systems<br/>"
#         f"/api/v1.0/transit_systems/London<br/>"
#         f"/api/v1.0/transit_systems/New York<br/>"
#         f"/api/v1.0/transit_systems/Stockholm<br/>"
#         f"..."
#     )

@app.route("/api/v1.0/transit_systems")
def transit_systems():
    """Display all transit system data"""
    # Query db for all results
    results = table_join()
    results = results.all()

    # Return JSON results
    json_results = json_dict(results)
    return json_results

@app.route("/api/v1.0/transit_systems/<city_name>")
def city(city_name):
    """Filter transit system data based on the searched city"""

    # Make sure the city is in title case
    city_name = city_name.title()

    # Query db and filter
    results = table_join()
    results = results.filter(Cities.city_name==city_name).all()

    # If the city is found, return JSON results:
    if results:
        json_results = json_dict(results)
        return json_results

    # Else 404 error
    else:
        return jsonify({"error": f"Your search term {city_name} was not found."}), 404


# Preview on http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
