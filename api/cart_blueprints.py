from flask import Blueprint, request, jsonify, Response
from collections import Counter
from api.utils.helpers import retrieve_items_from_json
from api.utils.types import CartList, Cart, ShirtList

cart_blueprint: Blueprint = Blueprint('cart_blueprint', __name__)

# Will need items across both functions, better to define globally
items: ShirtList = retrieve_items_from_json()


# Helper for calculating price with discounts algorithmically
def calculate_cart_total_price(cart: CartList) -> float:
    # Map item IDs to their prices
    id_to_price = {item["id"]: item["price"] for item in items}

    # Flatten the cart into a list of item IDs, taking quantities into account
    all_items = []
    for entry in cart:
        all_items.extend([entry["id"]] * entry["quantity"])

    # Count the occurrences of each shirt ID
    counts = Counter(all_items)

    total_price = 0.0
    discounts = {1: 0, 2: 0.05, 3: 0.10, 4: 0.15, 5: 0.20}

    # Apply discounts in sets
    while len(counts) > 0:
        # Get the size of the largest possible set of unique items
        num_unique = len(counts)
        if num_unique > 5:
            num_unique = 5

        # Create a set of unique items
        set_items = [shirt_id for shirt_id, _ in counts.most_common(num_unique)]

        # Calculate the discount for this set
        set_price = sum(id_to_price[shirt_id] for shirt_id in set_items)
        discount = discounts[len(set_items)]
        total_price += set_price * (1 - discount)

        # Deduct one of each shirt in the set
        for shirt_id in set_items:
            counts[shirt_id] -= 1
            if counts[shirt_id] == 0:
                del counts[shirt_id]

    return total_price


@cart_blueprint.route("/update", methods=["POST"])
def add_to_cart() -> Response:
    # Retrieve data from the frontend
    put_data = request.get_json()
    cart: CartList = put_data.get("cart")
    new_item: Cart = put_data.get("newItem")

    # Check to see if the item is actually in the library (Prevent abuse)
    item_in_library: bool = False
    for item in items:
        if item['id'] == new_item['id']:
            item_in_library = True
            break
    # If item doesn't exist, send an error to the frontend
    if not item_in_library:
        return jsonify({"message": "Item not found"}), 401

    # Check to see if the item is in cart already; if so, mutate the quantity
    item_already_in_cart = False
    for item in cart:
        if item['id'] == new_item['id']:
            item_already_in_cart = True
            item['quantity'] += new_item['quantity']
            break
    # If item is not in cart, append it to cart
    if not item_already_in_cart:
        cart.append(new_item)

    # Pass cart forward to calculate the price (Do this on backend so that user can't name their own price)
    price_of_cart: float = calculate_cart_total_price(cart)

    # Return updated cart and subtotal to frontend
    return jsonify({"cart": cart, "price_of_cart": price_of_cart}), 201