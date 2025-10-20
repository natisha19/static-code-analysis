#cleaned, fixed, and documented ver of inventory_system.py
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename="inventory.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    # Adds item to inventory with validation and safe logging.
    if logs is None:  # fix 1: avoid mutable default argument
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):  # ✅ FIX 2: Validate input types
        logging.warning(f"Invalid input types for addItem: item={item}, qty={qty}")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info(f"Added {qty} of {item}")


def remove_item(item, qty):
    # Removes item safely with specific exception handling.
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        logging.info(f"Removed {qty} of {item}")
    except KeyError:  # fix 3: Use specific exception instead of bare except
        logging.warning(f"Attempted to remove non-existent item: {item}")


def get_qty(item):
    # Returns quantity of an item if it exists.
    return stock_data[item]


def load_data(file="inventory.json"):
    # Loads inventory data safely from a file.
    global stock_data
    try:
        # fix 4: Use context manager for safe file handling
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        logging.info("Data loaded successfully.")
    except FileNotFoundError:
        logging.warning("Inventory file not found. Starting with empty data.")


def save_data(file="inventory.json"):
    # Saves inventory data safely to a file.
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f)
    logging.info("Data saved successfully.")


def print_data():
    # Prints all inventory data.
    print("Items Report")
    for i, q in stock_data.items():
        print(f"{i} -> {q}")  # fix 5: Use f-string


def check_low_items(threshold=5):
    # Return list of items below threshold quantity.
    return [i for i, q in stock_data.items() if q < threshold]


def main():
    # Main function to demonstrate inventory operations.
    add_item("apple", 10)
    add_item("banana", 2)
    add_item(123, "ten")  # This will now log a warning and not crash
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()

    # fix 6: Removed eval() and replaced it with a safe equivalent
    logging.info("Eval removed for security.")


if __name__ == "__main__":
    main()
