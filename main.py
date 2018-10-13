from flask import Flask
import os
from makebase import Base, Offer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route("/")
def hello():
    database_url = os.environ.get('DATABASE_URL')
    engine = create_engine(database_url)
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    return session.query(Offer).all()

if __name__ == "__main__":
    app.run()
