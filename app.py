# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/tob<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').all()

    session.close()

    precip = []
    for date, prcp in data:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        precip.append(dict)
    
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    data = session.query(Station.station).all()

    session.close()

    station_list = list(np.ravel(data))

    return jsonify(station_list)


@app.route("/api/v1.0/tob")
def tob():
    data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

    temp_list = list(np.ravel(data))

    return jsonify(temp_list)


@app.route("/api/v1.0/<start>")
def start(start_date):
    data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

    session.close()

    stats_list = list(np.ravel(data))

    return jsonify(stats_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date):
    data = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()

    session.close()

    stats_list = list(np.ravel(data))

    return jsonify(stats_list)


if __name__ == '__main__':
    app.run(debug=True)