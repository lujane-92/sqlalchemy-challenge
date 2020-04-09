from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
import sqlite3
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

database_path = "/Users/lujan/Desktop/sqlalchemy-challenge/Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

last_12 = dt.date(2017, 8, 23) - dt.timedelta(days=365)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List of available api routes."""
    return (
        f"Welcome! The available API routes are<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp_q = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
    return jsonify(prcp_q)

@app.route("/api/v1.0/stations")
def stations():
    query = session.query(Measurement.station)
    station_act = query.group_by(Measurement.station).all()
    return jsonify(station_act)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > '2016-08-23').all()
    return jsonify(tobs)    


@app.route('/api/v1.0/<date>/')
def given_date(date):
    """Return the average temp, max temp, and min temp for the date"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    # creates JSONified list of dictionaries
    data_list = []
    for result in results:
        row = {}
        row['Start Date'] = date
        row['End Date'] = '2017-08-23'
        row['Average Temperature'] = float(result[0])
        row['Highest Temperature'] = float(result[1])
        row['Lowest Temperature'] = float(result[2])
        data_list.append(row)

    return jsonify(data_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    """Return the avg, max, min, temp over a specific time period"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    # creates JSONified list of dictionaries
    data_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = float(result[0])
        row["Highest Temperature"] = float(result[1])
        row["Lowest Temperature"] = float(result[2])
        data_list.append(row)
    return jsonify(data_list)



if __name__ == '__main__':
    app.run(debug=True)