from typing import List, Dict, Optional, Literal

class Fill:
    def __init__(self, price: float, qty: float, trade_id: int):
        self.price = price
        self.qty = qty
        self.trade_id = trade_id

    def to_dict(self):
        return {
            "price": self.price,
            "qty": self.qty,
            "tradeId": self.trade_id
        }

class Order:
    def __init__(self, order_id: str, price: float, quantity: float, side: Literal["bid", "ask"]):
        self.order_id = order_id
        self.price = price
        self.quantity = quantity
        self.side = side

    def to_dict(self):
        return {
            "orderId": self.order_id,
            "price": self.price,
            "quantity": self.quantity,
            "side": self.side
        }

class OrderResult:
    def __init__(self, order_id: str, status: Literal["accepted", "rejected"], executed_qty: float, fills: List[Fill]):
        self.order_id = order_id
        self.status = status
        self.executed_qty = executed_qty
        self.fills = fills

    def to_dict(self):
        return {
            "orderId": self.order_id,
            "status": self.status,
            "executedQty": self.executed_qty,
            "fills": [f.to_dict() for f in self.fills]
        }