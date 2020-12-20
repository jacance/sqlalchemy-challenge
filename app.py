# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"<h1>Welcome to the Climate App!</h1><br/><br/>"
        f'<b>Available Routes:</b><br/><br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

# Precipitation page
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Dictionary with date as key and precipitation as value
    prcp_dict = {
        date: prcp
        for date, prcp in results
    }
    return jsonify(prcp_dict)

# Stations page
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    # All stations
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

# Page for temperature observations of most active station.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Calculate one year before last day of data
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year_ago

    # Query last 12 months of temperature observation data for most active station
    active_12mo = session.query(Measurement.tobs).order_by(Measurement.tobs.asc()).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    active_12mo = list(np.ravel(active_12mo))
    return jsonify(active_12mo)

# Page of minimum, average, and maximum temperature observations for a given day.
@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    # Query minimum, average, and maximum temperature observations for a given day.
    results = list(np.ravel(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()))

    session.close()

    # All dates of measurement data
    all_dates = list(np.ravel(session.query(Measurement.date).all()))

    # Return results if start date entered by user is found in data. If not, return date not found.
    for date in all_dates:
        if start == date:
            return jsonify(results)
    return jsonify({"error": f"Date {start} found."}), 404

# Page of minimum, average, and maximum temperature observations for a given start-end range.
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    # Query minimum, average, and maximum temperature observations for a given start-end range.
    results = list(np.ravel(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()))

    session.close()

    # All dates of measurement data
    all_dates = list(np.ravel(session.query(Measurement.date).all()))

    # Return results if start-end date range entered by user is found in data. If not, return date not found.
    for date in all_dates:
        if start == date:
            for date in all_dates:
                if end == date:
                    return jsonify(results)

    return jsonify({"error": f"Date {start} and/or {end} not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)