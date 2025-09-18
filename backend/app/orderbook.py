from typing import List, Dict

class Order:
    def __init__(self, order_id: str, price: float, quantity: float, side: str):
        self.order_id = order_id
        self.price = price
        self.quantity = quantity
        self.side = side  # "bid" or "ask"

class Orderbook:
    def __init__(self):
        self.bids: List[Order] = []
        self.asks: List[Order] = []

class BookWithQuantity:
    def __init__(self):
        self.bids: Dict[float, float] = {}
        self.asks: Dict[float, float] = {}

orderbook = Orderbook()
book_with_quantity = BookWithQuantity()