# Order Processing System

This is a CLI-based order processing system that efficiently handles a queue of customer orders,
applies discounts, calculates totals, and generates an invoice summary.

## Features

- Load and validate orders from a JSON file
- Apply discounts from a discount JSON file
- Support for multiple currencies
- Parallel processing for handling large order files
- Generates an invoice summary as a text file
- Proper error handling for missing files, invalid JSON, and missing fields
- Unit tests included

## Prerequisites

Make sure you have the following installed:

- Python 3.7 or later
- `pip` for package management

## Installation

Clone the repository:

```sh
$ git clone https://github.com/miraz-ezaz/OrderPrcoessingSystem.git
$ cd OrderPrcoessingSystem
```

## Usage

Run the order processing system with:

```sh
$ python order_processor.py <orders.json> <discounts.json> <output.txt>
```

Example:

```sh
$ python order_processor.py orders.json discounts.json invoice_summary.txt
```

### Input Files

#### Orders JSON (`orders.json`)

```json
[
  {
    "order_id": 101,
    "customer": "Alice",
    "items": [
      { "name": "Laptop", "price": 1000, "quantity": 1 },
      { "name": "Mouse", "price": 50, "quantity": 2 }
    ],
    "discount_code": "SUMMER10",
    "currency": "USD"
  }
]
```

#### Discounts JSON (`discounts.json`)

```json
{
  "SUMMER10": 10,
  "WELCOME5": 5
}
```

### Output File (`invoice_summary.txt`)

```
Order ID: 101 | Customer: Alice | Total Before Discount: $1100.00 | Total After Discount: $990.00
```

## Running Tests

To run the test suite:

```sh
$ python -m unittest test_order_processor.py
```

For verbose output:

```sh
$ python -m unittest -v test_order_processor.py
```

## Logging

The system logs errors and key actions. Logs are printed to the console and can be customized in `order_processor.py`
