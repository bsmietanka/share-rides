from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
import os
 
from makebase import Offer, Base

database_url = os.environ.get('DATABASE_URL')
engine = create_engine(database_url)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
# Insert an Ofer in the person table
new_offer = Offer(name='new offer')
session.add(new_offer)
session.commit()