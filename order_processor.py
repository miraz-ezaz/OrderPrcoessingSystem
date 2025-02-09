import json
import logging
import multiprocessing
import sys
from pathlib import Path
from typing import List
from models import Order, OrderItem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrderProcessor:
    def __init__(self, orders_file: str, discounts_file: str, output_file: str):
        self.orders_file = Path(orders_file)
        self.discounts_file = Path(discounts_file)
        self.output_file = Path(output_file)
        self.orders = []
        self.discount_dict = {}
    
    def load_json(self, file_path: Path):
        """Load JSON data from a file with error handling."""
        if not file_path.exists():
            logging.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format in {file_path}: {e}")
            raise ValueError(f"Invalid JSON format in {file_path}: {e}")
    
    def validate_order(self, order_data: dict):
        """Validate order data and raise errors for missing fields."""
        required_fields = ["order_id", "customer", "items"]
        for field in required_fields:
            if field not in order_data:
                logging.error(f"Missing required field '{field}' in order data.")
                raise ValueError(f"Missing required field '{field}' in order data.")
    
    def process_orders(self):
        """Load, validate, and process orders."""
        order_list = self.load_json(self.orders_file)
        self.discount_dict = self.load_json(self.discounts_file) or {}
        
        for order_data in order_list:
            try:
                self.validate_order(order_data)
                items = [OrderItem(item["name"], item["price"], item["quantity"]) for item in order_data["items"]]
                order = Order(order_data["order_id"], order_data["customer"], items, order_data.get("discount_code"))
                self.orders.append(order)
            except ValueError as e:
                logging.warning(f"Skipping invalid order: {e}")
    
    def process_orders_parallel(self):
        """Process orders in parallel using multiprocessing for efficiency."""
        self.discount_dict = self.load_json(self.discounts_file) or {}
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            self.orders = pool.map(self.process_single_order, self.load_json(self.orders_file))
    
    def process_single_order(self, order_data: dict):
        """Process a single order and return an Order object."""
        try:
            self.validate_order(order_data)
            items = [OrderItem(item["name"], item["price"], item["quantity"]) for item in order_data["items"]]
            return Order(order_data["order_id"], order_data["customer"], items, order_data.get("discount_code"))
        except ValueError as e:
            logging.warning(f"Skipping invalid order: {e}")
            return None
    
    def generate_invoice_summary(self):
        """Generate and save the invoice summary to a file."""
        with open(self.output_file, 'w', encoding='utf-8') as file:
            for order in self.orders:
                if order:
                    file.write(order.order_summary(self.discount_dict) + "\n")
        logging.info(f"Invoice summary saved to {self.output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python order_processor.py <orders.json> <discounts.json> <output.txt>")
        sys.exit(1)
    
    processor = OrderProcessor(sys.argv[1], sys.argv[2], sys.argv[3])
    processor.process_orders_parallel()
    processor.generate_invoice_summary()
