import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CURRENCY_CONVERSION = {
    "USD": {"rate": 1.0, "sign": "$"},
    "EUR": {"rate": 0.85, "sign": "€"},
    "GBP": {"rate": 0.75, "sign": "£"},
}

class OrderItem:
    def __init__(self, name: str, price: float, quantity: int):
        if price < 0 or quantity < 1:
            logging.error("Invalid price or quantity for OrderItem.")
            raise ValueError("Price must be non-negative and quantity must be at least 1.")
        
        self.name = name
        self.price = price
        self.quantity = quantity
        logging.info(f"OrderItem created: {self}")
    
    def total_price(self) -> float:
        return self.price * self.quantity
    
    def __repr__(self):
        return f"OrderItem(name={self.name}, price={self.price}, quantity={self.quantity})"


class Order:
    def __init__(self, order_id: int, customer: str, items: List[OrderItem], discount_code: Optional[str] = None, currency: str = "USD"):
        if not items:
            logging.error("An order must contain at least one item.")
            raise ValueError("An order must contain at least one item.")
        
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.discount_code = discount_code
        self.currency = currency if currency in CURRENCY_CONVERSION else "USD"
        logging.info(f"Order created: {self}")
    
    def total_before_discount(self) -> float:
        return sum(item.total_price() for item in self.items) * CURRENCY_CONVERSION[self.currency]["rate"]
    
    def apply_discount(self, discount_dict: dict) -> float:
        discount_percentage = discount_dict.get(self.discount_code, 0)
        discount_amount = (self.total_before_discount() * discount_percentage) / 100
        if discount_amount != 0:
            logging.info(f"Discount Applied: {discount_percentage} % Code:{self.discount_code}")
        return self.total_before_discount() - discount_amount
    
    def order_summary(self, discount_dict: dict) -> str:
        total_before = self.total_before_discount()
        total_after = self.apply_discount(discount_dict)
        currency_sign = CURRENCY_CONVERSION[self.currency]["sign"]
        return f"Order ID: {self.order_id} | Customer: {self.customer} | Total Before Discount: {currency_sign}{total_before:.2f} | Total After Discount: {currency_sign}{total_after:.2f}"
    
    def __repr__(self):
        return f"Order(order_id={self.order_id}, customer={self.customer}, items={self.items}, discount_code={self.discount_code}, currency={self.currency})"
