import uuid
from typing import List, Dict, Optional, Literal
from app.types import Fill, Order, OrderResult

BASE_ASSET = "BTC"
QUOTE_ASSET = "USD"

class OrderbookManager:
    def __init__(self):
        self.bids: List[Order] = []
        self.asks: List[Order] = []
        self.bids_by_price: Dict[float, float] = {}
        self.asks_by_price: Dict[float, float] = {}
        self.global_trade_id = 0

    def _generate_order_id(self) -> str:
        return str(uuid.uuid4())

    def _get_next_trade_id(self) -> int:
        self.global_trade_id += 1
        return self.global_trade_id

    def _get_fill_amount(self, price: float, quantity: float, side: str) -> float:
        filled = 0.0
        if side == "buy":
            for order in self.asks:
                if order.price < price:
                    filled += min(quantity, order.quantity)
        else:
            for order in self.bids:
                if order.price > price:
                    filled += min(quantity, order.quantity)
        return filled

    def fill_order(self, price: float, quantity: float, side: str, kind: Optional[str] = None) -> OrderResult:
        order_id = self._generate_order_id()
        fills: List[Fill] = []
        executed_qty = 0.0
        remaining_qty = quantity

        max_fill_quantity = self._get_fill_amount(price, quantity, side)
        if kind == "ioc" and max_fill_quantity < quantity:
            return OrderResult(order_id, "rejected", max_fill_quantity, [])

        if side == "buy":
            for ask in self.asks[:]:
                if ask.price <= price and remaining_qty > 0:
                    fill_qty = min(remaining_qty, ask.quantity)
                    fills.append(Fill(ask.price, fill_qty, self._get_next_trade_id()))
                    executed_qty += fill_qty
                    remaining_qty -= fill_qty
                    ask.quantity -= fill_qty
                    self.asks_by_price[ask.price] = self.asks_by_price.get(ask.price, 0) - fill_qty
                    if ask.quantity == 0:
                        self.asks.remove(ask)
                    if self.asks_by_price.get(ask.price, 0) == 0:
                        self.asks_by_price.pop(ask.price, None)
            if remaining_qty > 0:
                bid = Order(order_id, price, remaining_qty, "bid")
                self.bids.append(bid)
                self.bids_by_price[price] = self.bids_by_price.get(price, 0) + remaining_qty
        else:
            for bid in self.bids[:]:
                if bid.price >= price and remaining_qty > 0:
                    fill_qty = min(remaining_qty, bid.quantity)
                    fills.append(Fill(bid.price, fill_qty, self._get_next_trade_id()))
                    executed_qty += fill_qty
                    remaining_qty -= fill_qty
                    bid.quantity -= fill_qty
                    self.bids_by_price[bid.price] = self.bids_by_price.get(bid.price, 0) - fill_qty
                    if bid.quantity == 0:
                        self.bids.remove(bid)
                    if self.bids_by_price.get(bid.price, 0) == 0:
                        self.bids_by_price.pop(bid.price, None)
            if remaining_qty > 0:
                ask = Order(order_id, price, remaining_qty, "ask")
                self.asks.append(ask)
                self.asks_by_price[price] = self.asks_by_price.get(price, 0) + remaining_qty

        return OrderResult(order_id, "accepted", executed_qty, fills)