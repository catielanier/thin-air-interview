from flask import Flask
from flask_cors import CORS

DEBUG: bool = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run(debug=DEBUG)