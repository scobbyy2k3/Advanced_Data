# 1. import Flask
import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# Database Setup
#_______________________________________________________________
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
#_______________________________________________________
app = Flask(__name__)

# Flask Routes

#### Home page
""" List all routes that are available."""
@app.route("/")
def home():
   print("Server received request for 'Home' page...")
   return (
       f"Welcome to my 'Trip to Hawaii' page!</br>"
       f"Available Routes:<br/>"
       f"/v1/stations<br/>"
       f"/v1/precipitation<br/>"
       f"/v1/tobs<br/>"
       f"/v1/start_date(YYYY-MM-DD)<br/>"
       f"/v1/start_date(YYYY-MM-DD)/end_date(YYYY-MM-DD)<br/>"
   )
#________________________________________
# stations
"""* Return a JSON list of stations from the dataset."""
@app.route("/v1/stations")
def stations():
   stations = session.query(Station.name,Station.station).order_by(Station.name.desc()).all()
   return jsonify(stations)
#________________________________________
# PRECIPITATION #
@app.route("/v1/precipitation")
def precipitation():
       precipitation_df = session.query(Measurement.date,Measurement.prcp).order_by(Measurement.date.desc()).all()
       precipitation = []
       for date, prcp in precipitation_df:
               precip_dict ={}
               precip_dict["date"] = date
               precip_dict["prcp"] = prcp
               precipitation.append(precip_dict)
       return jsonify(precipitation)
#________________________________________
# tobs_results
"""Query for the dates and temperature observations from a year from the last data point."""
"""Return a JSON list of Temperature Observations (tobs) for the previous year.   """
@app.route("/v1/tobs")
def tobs():
       temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > "2016-08-23").order_by(Measurement.date.desc())
       temperatures = []
       for date, tobs in temps:
               calc_temps ={}
               calc_temps["date"] = date
               calc_temps["tobs"] = tobs
               temperatures.append(calc_temps)
       print(temperatures)
       return jsonify(temperatures)
#________________________________________
# START DATE #
@app.route("/v1/<start_date>")
def start(start_date):
       start_values = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= start_date).all()
       start_temps = {"minT": start_values[0][0],
                       "avgT": start_values[0][1],
                       "maxT": start_values[0][2]
       }
       return jsonify(start_temps)
#________________________________________
# START DATE TO END DATE 
@app.route("/v1/<start_date>/<end_date>")
def start_end(start_date, end_date):
       start_end_values = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
       temps = {"minT": start_end_values[0][0],
               "avgT": start_end_values[0][1],
               "maxT": start_end_values[0][2]
       }
       return jsonify (temps)
#________________________________________
if __name__ == "__main__":
       app.run(debug=True)