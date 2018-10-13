from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
 
from makebase import Offer, Base
 
engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
# Insert an Ofer in the person table
new_offer = Offer(name='new offer')
session.add(new_offer)
session.commit()