import json
import os
from flask import Blueprint, request, jsonify, Response

from api.utils.types import ShirtList
from api.utils.helpers import retrieve_items_from_json

item_blueprint: Blueprint = Blueprint('item_blueprint', __name__)


@item_blueprint.route('/', methods=['GET'])
def get_all_items() -> Response:
    items: ShirtList = retrieve_items_from_json()
    return jsonify(items), 200