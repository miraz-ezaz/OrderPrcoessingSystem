import unittest
import json
import os
from pathlib import Path
from order_processor import OrderProcessor

class TestOrderProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test files before running tests."""
        self.orders_file = "test_orders.json"
        self.discounts_file = "test_discounts.json"
        self.output_file = "test_invoice_summary.txt"
        
        test_orders = [
            {
                "order_id": 1,
                "customer": "John Doe",
                "items": [
                    {"name": "Laptop", "price": 1000, "quantity": 1},
                    {"name": "Mouse", "price": 50, "quantity": 2}
                ],
                "discount_code": "SUMMER10",
                "currency": "USD"
            },
            {
                "order_id": 2,
                "customer": "Jane Smith",
                "items": [
                    {"name": "Monitor", "price": 200, "quantity": 2}
                ],
                "currency": "EUR"
            }
        ]
        
        test_discounts = {
            "SUMMER10": 10,
            "WELCOME5": 5
        }
        
        with open(self.orders_file, "w") as f:
            json.dump(test_orders, f)
        
        with open(self.discounts_file, "w") as f:
            json.dump(test_discounts, f)
    
    def tearDown(self):
        """Clean up test files after tests."""
        os.remove(self.orders_file)
        os.remove(self.discounts_file)
        if Path(self.output_file).exists():
            os.remove(self.output_file)
    
    def test_load_json_valid(self):
        """Test loading valid JSON files."""
        processor = OrderProcessor(self.orders_file, self.discounts_file, self.output_file)
        orders = processor.load_json(Path(self.orders_file))
        discounts = processor.load_json(Path(self.discounts_file))
        self.assertEqual(len(orders), 2)
        self.assertEqual(discounts["SUMMER10"], 10)
    
    def test_process_orders(self):
        """Test processing orders without errors."""
        processor = OrderProcessor(self.orders_file, self.discounts_file, self.output_file)
        processor.process_orders()
        self.assertEqual(len(processor.orders), 2)
    
    def test_generate_invoice_summary(self):
        """Test invoice summary generation."""
        processor = OrderProcessor(self.orders_file, self.discounts_file, self.output_file)
        processor.process_orders()
        processor.generate_invoice_summary()
        self.assertTrue(Path(self.output_file).exists())
    
    def test_missing_field(self):
        """Test handling of missing required fields in order data."""
        invalid_orders_file = "invalid_orders.json"
        invalid_orders = [
            {"customer": "John Doe", "items": [{"name": "Laptop", "price": 1000, "quantity": 1}]}
        ]

        with open(invalid_orders_file, "w") as f:
            json.dump(invalid_orders, f)

        processor = OrderProcessor(invalid_orders_file, self.discounts_file, self.output_file)
        processor.process_orders()
        
        # Ensure no orders were added since it was invalid
        self.assertEqual(len(processor.orders), 0)

        os.remove(invalid_orders_file)

    
if __name__ == "__main__":
    unittest.main()
