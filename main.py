from flask import Flask, request
import os
from datetime import time
import json
from makebase import Base, Offer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/offer", methods=['POST'])
def offer():
    content = request.json
    parsed = json.loads(content)

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
    except:
        return json.dumps({ "offer_create_endpoint_respond_sucess" : { "success" : False }})
    return json.dumps({ "offer_create_endpoint_respond_sucess" : { "success" : True }})

if __name__ == "__main__":
    app.run()
