from flask import Flask
from flask_cors import CORS

from api.item_blueprint import item_blueprint

DEBUG: bool = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(item_blueprint, url_prefix='/api/v1/items')

if __name__ == '__main__':
    app.run(debug=DEBUG)