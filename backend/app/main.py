from flask import Flask, request, jsonify
from app.orderbook import OrderbookManager
import json

app = Flask(__name__)
orderbook_manager = OrderbookManager()

def js_style_orderbook_dump(orderbook_manager):
    # Prepare bids and asks as list of dicts
    bids = [o.to_dict() for o in orderbook_manager.bids]
    asks = [o.to_dict() for o in orderbook_manager.asks]
    # Print orderbook
    print("orderbook:\n")
    print(json.dumps({"bids": bids, "asks": asks}, indent=2))
    # Print book_with_quantity with string keys
    bids_by_price = {str(k): v for k, v in orderbook_manager.bids_by_price.items()}
    asks_by_price = {str(k): v for k, v in orderbook_manager.asks_by_price.items()}
    print(json.dumps({"bids": bids_by_price, "asks": asks_by_price}, indent=2))

@app.route("/api/v1/order", methods=["POST"])
def create_order():
    data = request.json
    required_fields = ["base_asset", "quote_asset", "price", "quantity", "side"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if data["base_asset"] != "BTC" or data["quote_asset"] != "USD":
        return jsonify({"error": "Invalid base or quote asset"}), 400

    result = orderbook_manager.fill_order(
        price=data["price"],
        quantity=data["quantity"],
        side=data["side"],
        kind=data.get("kind")
    )
    js_style_orderbook_dump(orderbook_manager)
    return jsonify(result.to_dict()), 200

@app.route("/api/v1/orderbook", methods=["GET"])
def get_orderbook():
    # Optionally implement orderbook snapshot endpoint here
    return jsonify({
        "bids": [o.to_dict() for o in orderbook_manager.bids],
        "asks": [o.to_dict() for o in orderbook_manager.asks],
        "bids_by_price": orderbook_manager.bids_by_price,
        "asks_by_price": orderbook_manager.asks_by_price
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)