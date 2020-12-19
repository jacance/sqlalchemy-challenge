import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

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

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year_ago

    active_12mo = session.query(Measurement.tobs).order_by(Measurement.tobs.asc()).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()

    active_12mo = list(np.ravel(active_12mo))
    return jsonify(active_12mo)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).all()

    session.close()

    all_temp = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temp.append(temp_dict)
    
   
    for x in all_temp:
        search_term = x["date"]
        if search_term == start:
            return jsonify(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).all())


    return jsonify({"error": "Date not found."}), 404

# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start_end):

#     session = Session(engine)
#     results = session.query(Measurement.date, Measurement.tobs).all()

#     session.close()

#     all_temp = []
#     for date, tobs in results:
#         temp_dict = {}
#         temp_dict["date"] = date
#         temp_dict["tobs"] = tobs
#         all_temp.append(temp_dict)
    
#    canonicalized = real_name.replace("/", "Measurement.date <= ")
#     for x in all_temp:
#         search_term = x["date"]
#         if search_term == start_end:
#             return jsonify(session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
#                 filter(Measurement.date >= start_end).all())

if __name__ == "__main__":
    app.run(debug=True)