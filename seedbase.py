from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, time
#import datetime as dtime
import json
import pprint
 
from makebase import Offer, Base
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
# Insert an Offer in the person table
nowDate = datetime(2012,3,3,10,10,10)

with open("offer.json") as f:
    content = f.read()
parsed = json.loads(content)

print(json.dumps(parsed, indent=4, sort_keys=True))
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(parsed)
start_coord = parsed["start_location"]
end_coord = parsed["end_location"]
parsed.pop("start_location", None)
parsed.pop("end_location", None)

parsed["time_end"] =   time(*list(map(int, parsed["time_end"  ].split(":"))))
parsed["time_start"] = time(*list(map(int, parsed["time_start"].split(":"))))
print(parsed["time_end"])
parsed["start_lat"] = start_coord["lat"]
parsed["start_long"] = start_coord["long"]
parsed["end_lat"] = end_coord["lat"]
parsed["end_long"] = end_coord["long"]


new_offer = Offer(**parsed)
session.add(new_offer)
session.commit()

print(session.query(Offer).first())