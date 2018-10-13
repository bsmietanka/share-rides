from flask import Flask, request, jsonify
from flask.ext.api import status
import os
from datetime import time
import json
from makebase import Base, Offer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
import socket
from logging.handlers import SysLogHandler
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/offer", methods=['POST'])
def offer():
    parsed = request.json
    # parsed = json.loads(content)

    start_coord = parsed["start_location"]
    end_coord = parsed["end_location"]
    parsed.pop("start_location", None)
    parsed.pop("end_location", None)
    parsed["start_lat"] = start_coord["lat"]
    parsed["start_long"] = start_coord["long"]
    parsed["end_lat"] = end_coord["lat"]
    parsed["end_long"] = end_coord["long"]

    parsed["time_end"] =   time(*list(map(int, parsed["time_end"  ].split(":"))))
    parsed["time_start"] = time(*list(map(int, parsed["time_start"].split(":"))))

    parsed["phone_number"] = str(parsed["phone_number"])

    new_offer = Offer(**parsed)

    database_url = os.environ.get('DATABASE_URL')
    engine = create_engine(database_url)
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    try:
        session.add(new_offer)
        session.commit()
    except Exception as e:
        logger.exception("I got you")
        return json.dumps({ "success" : False, "error_message" : str(e) }), status.HTTP_400_BAD_REQUEST
    return json.dumps({ "success" : True }), status.HTTP_200_OKs

if __name__ == "__main__":
    app.run()
