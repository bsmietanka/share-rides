import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Offer(Base):
    __tablename__ = 'offers'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phone_number = Column(String(15), nullable=False)
    time_start = Column(Time(), nullable=False)
    time_end = Column(Time(), nullable=False)
    start_lat = Column(DECIMAL(), nullable=False)
    start_long = Column(DECIMAL(), nullable=False)
    end_lat = Column(DECIMAL(), nullable=False)
    end_long = Column(DECIMAL(), nullable=False)
    price = Column(DECIMAL(), nullable=True)
    seats_available = Column(Integer, nullable=False)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
database_url = os.environ.get('DATABASE_URL')
engine = create_engine(database_url)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)