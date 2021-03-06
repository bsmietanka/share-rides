from flask import Flask, request, jsonify
import os
from datetime import time
import json
from makebase import Base, Offer
from datetime import time
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
import logging
from flask_cors import CORS

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
database_url = os.environ.get('DATABASE_URL')
engine = create_engine(database_url)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/offer", methods=['POST'])
def offer():
    parsed = request.json

    parsed["time_end"] =   time(*list(map(int, parsed["time_end"].split(":"))))
    parsed["time_start"] = time(*list(map(int, parsed["time_start"].split(":"))))

    new_offer = Offer(**parsed)

    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    try:
        session.add(new_offer)
        session.commit()
        session.close()
    except Exception as e:
        session.close()
        logger.exception("I got you")
        return json.dumps({ "success" : False, "error_message" : str(e) }), 400
    return json.dumps({ "success" : True }), 200

@app.route("/search", methods=['POST'])
def search():
    parsed = request.json

    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    lat_scale_factor = 0.009032
    long_scale_factor = 0.0146867
    max_distance = 1

    try:
        results = session.query(Offer).filter(and_(
            Offer.start_distance(parsed["start_lat"], parsed["start_long"]) <= max_distance,
            Offer.end_distance(parsed["end_lat"], parsed["end_long"]) <= max_distance,
            Offer.time_end <= time(*list(map(int, parsed["time_end"].split(":")))),
            Offer.time_start >= time(*list(map(int, parsed["time_start"].split(":"))))
            )).order_by(Offer.time_end, Offer.time_start).all()
        session.close()
    except Exception as e:
        session.close()
        logger.exception("[ERROR] [Search]")
        return json.dumps({ "success" : False, "error_message" : str(e) }), 400
    return json.dumps({ "success" : True, "offers" : [r.as_dict() for r in results] }), 200

@app.route("/drop_database", methods=["GET"])
def drop_database():
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    rows_deleted = session.query(Offer).delete()
    session.commit()
    session.close()
    return "DATABASE DROPPED, ROWS DELETED: " + str(rows_deleted)

@app.route("/show_all", methods=["GET"])
def show_all():
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    res = session.query(Offer).all()
    session.close()
    return json.dumps({ "offers" : [r.as_dict() for r in res] }), 200


if __name__ == "__main__":
    app.run()
