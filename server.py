from flask import Flask
from flask_cors import CORS

from api.cart_blueprints import cart_blueprint
from api.item_blueprint import item_blueprint

DEBUG: bool = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(item_blueprint, url_prefix='/api/v1/items')
app.register_blueprint(cart_blueprint, url_prefix='/api/v1/cart')

if __name__ == '__main__':
    app.run(debug=DEBUG)