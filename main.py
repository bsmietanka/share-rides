from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return os.environ.get('DATABASE_URL')

if __name__ == "__main__":
    app.run()
