import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, DECIMAL, Time
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, func
from sqlalchemy.ext.hybrid import hybrid_method
import logging
from decimal import Decimal
 
Base = declarative_base()

logger = logging.getLogger(__name__)
 
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

    @hybrid_method
    def start_distance(self, lat, lng):
        lat_scale_factor = 0.009032
        long_scale_factor = 0.0146867
        return (func.pow(((self.start_lat - lat)/lat_scale_factor), 2) + 
               func.pow(((self.start_long - lng)/long_scale_factor), 2))

    @hybrid_method
    def end_distance(self, lat, lng):
        lat_scale_factor = 0.009032
        long_scale_factor = 0.0146867
        return (func.pow(((self.end_lat - lat)/lat_scale_factor), 2) + 
               func.pow(((self.end_long - lng)/long_scale_factor), 2))

    def as_dict(self):
        ret = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret["time_start"] = ret["time_start"].strftime('%H:%M')
        ret["time_end"] = ret["time_end"].strftime('%H:%M')
        for key, item in ret.items():
            if type(item) == Decimal:
                ret[key] = float(item)
        return ret


 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
database_url = os.environ.get('DATABASE_URL')
engine = create_engine(database_url)

Base.metadata.create_all(engine)