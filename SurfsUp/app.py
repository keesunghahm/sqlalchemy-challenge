import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
          f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    Oneyearago=dt.datetime(2017,8,23)-dt.timedelta(days=366)
    Queryresult=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=Oneyearago).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date,prcp in Queryresult:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
    
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    Oneyearago=dt.datetime(2017,8,23)-dt.timedelta(days=366)
    Queryresult=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=Oneyearago).filter(Measurement.station=='USC00519281').all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for date,tobs in Queryresult:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
    
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(temp))

    return jsonify(all_names)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=start).\
          filter(Measurement.date<=end).all()
    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(temp))

    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)
