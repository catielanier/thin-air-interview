import json
import os
from flask import Blueprint, request, jsonify, Response

from api.utils.types import ShirtList

item_blueprint: Blueprint = Blueprint('item_blueprint', __name__)


def retrieve_items_from_json():
    with open(
        os.path.join(
            os.path.realpath(''),
            'data/items.json'
        )
    ) as f:
        return json.loads(f.read())

@item_blueprint.route('/', methods=['GET'])
def get_all_items() -> Response:
    items: ShirtList = retrieve_items_from_json()
    return jsonify(items)