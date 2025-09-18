from flask import Flask, request, jsonify
from app.orderbook import Orderbook, BookWithQuantity, Order
import json
import uuid

app = Flask(__name__)
orderbook = Orderbook()
book_with_quantity = BookWithQuantity()
GLOBAL_TRADE_ID = 0

def js_style_orderbook_dump():
    bids = [vars(o) for o in orderbook.bids]
    asks = [vars(o) for o in orderbook.asks]
    print("orderbook:\n")
    print(json.dumps({"bids": bids, "asks": asks}, indent=2))
    bids_by_price = {str(k): v for k, v in book_with_quantity.bids.items()}
    asks_by_price = {str(k): v for k, v in book_with_quantity.asks.items()}
    print(json.dumps({"bids": bids_by_price, "asks": asks_by_price}, indent=2))

def fill_order(order_id, price, quantity, side, kind=None):
    global GLOBAL_TRADE_ID
    fills = []
    executed_qty = 0
    remaining_qty = quantity

    if side == "buy":
        # Sort asks by price ascending
        for o in sorted(orderbook.asks, key=lambda x: x.price):
            if o.price <= price and remaining_qty > 0:
                filled_quantity = min(remaining_qty, o.quantity)
                o.quantity -= filled_quantity
                book_with_quantity.asks[o.price] = book_with_quantity.asks.get(o.price, 0) - filled_quantity
                fills.append({
                    "price": o.price,
                    "qty": filled_quantity,
                    "tradeId": GLOBAL_TRADE_ID
                })
                GLOBAL_TRADE_ID += 1
                executed_qty += filled_quantity
                remaining_qty -= filled_quantity
                if o.quantity == 0:
                    orderbook.asks.remove(o)
                if book_with_quantity.asks.get(o.price, 0) == 0:
                    book_with_quantity.asks.pop(o.price, None)
        # Place remaining on the book
        if remaining_qty > 0:
            order = Order(order_id, price, remaining_qty, "bid")
            orderbook.bids.append(order)
            book_with_quantity.bids[price] = book_with_quantity.bids.get(price, 0) + remaining_qty
    else:
        # Sort bids by price descending
        for o in sorted(orderbook.bids, key=lambda x: -x.price):
            if o.price >= price and remaining_qty > 0:
                filled_quantity = min(remaining_qty, o.quantity)
                o.quantity -= filled_quantity
                book_with_quantity.bids[o.price] = book_with_quantity.bids.get(o.price, 0) - filled_quantity
                fills.append({
                    "price": o.price,
                    "qty": filled_quantity,
                    "tradeId": GLOBAL_TRADE_ID
                })
                GLOBAL_TRADE_ID += 1
                executed_qty += filled_quantity
                remaining_qty -= filled_quantity
                if o.quantity == 0:
                    orderbook.bids.remove(o)
                if book_with_quantity.bids.get(o.price, 0) == 0:
                    book_with_quantity.bids.pop(o.price, None)
        # Place remaining on the book
        if remaining_qty > 0:
            order = Order(order_id, price, remaining_qty, "ask")
            orderbook.asks.append(order)
            book_with_quantity.asks[price] = book_with_quantity.asks.get(price, 0) + remaining_qty

    return {
        "executedQty": executed_qty,
        "fills": fills
    }

@app.route("/api/v1/order", methods=["POST"])
def create_order():
    data = request.json
    required_fields = ["base_asset", "quote_asset", "price", "quantity", "side"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if data["base_asset"] != "BTC" or data["quote_asset"] != "USD":
        return jsonify({"error": "Invalid base or quote asset"}), 400

    order_id = str(uuid.uuid4())
    side = "buy" if data["side"] == "buy" else "sell"
    kind = data.get("type")

    result = fill_order(order_id, data["price"], data["quantity"], side, kind)
    js_style_orderbook_dump()
    return jsonify({
        "orderId": order_id,
        "executedQty": result["executedQty"],
        "fills": result["fills"]
    }), 200

@app.route("/api/v1/orderbook", methods=["GET"])
def get_orderbook():
    return jsonify({
        "bids": [vars(o) for o in orderbook.bids],
        "asks": [vars(o) for o in orderbook.asks],
        "bids_by_price": book_with_quantity.bids,
        "asks_by_price": book_with_quantity.asks
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)