 
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify

# Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# Reflect Tables
Base.prepare(engine, reflect=True)

# Reference to table
Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    "Available API Routes"
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
# --------------------------------------------------------------------------------------------------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #   * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
    results =   session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()
    # similar to P2 set [], append 
    prcp_dates = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_dates.append(prcp_dict)

    session.close()
     #Return the JSON representation of your dictionary
    return jsonify(prcp_dates)
# --------------------------------------------------------------------------------------------------------------------
@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    session = Session(engine)
    stations=session.query(Station.station).all()
    session.close()
 
    return jsonify(stations)
# --------------------------------------------------------------------------------------------------------------------
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    #Query the dates and temperature observations of the most active station for the last year of data.
    
    rec_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    rec_date_dt = dt.datetime.strptime(rec_date[0], "%Y-%m-%d")
    one_year_dt = (rec_date_dt - dt.timedelta(days=365)).strftime("%Y-%m-%d")


    list_station=session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    most_active = list_station[0][0]

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= (one_year_dt)).all()

    session.close()

    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def temp_range_start(start):
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
    #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

    session = Session(engine)
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    av_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    temp_S = []
    temp_dict = {}
    temp_dict["TMAX"] = high_temp
    temp_dict["TMIN"] = low_temp
    temp_dict["TAVG"] = av_temp
    temp_S.append(temp_dict)
    session.close()    

    return jsonify(temp_S)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start,end):
    session = Session(engine)
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    av_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start, Measurement.date <= end).all()
    
    temp_SE = []
    temp_dict2 = {}
    temp_dict2["TMAX"] = high_temp
    temp_dict2["TMIN"] = low_temp
    temp_dict2["TAVG"] = av_temp
    temp_SE.append(temp_dict2)
    session.close()    

    return jsonify(temp_SE)

if __name__ == '__main__':
    app.run(debug=True)