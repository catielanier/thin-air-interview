import json
import os


def retrieve_items_from_json():
    with open(
            os.path.join(
                os.path.realpath(''),
                'data/items.json'
            )
    ) as f:
        return json.loads(f.read())