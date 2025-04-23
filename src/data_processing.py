import pandas as pd


def load_data():
    orders = pd.read_csv("data/Orders.csv")
    inventory = pd.read_csv("data/Inventory.csv")
    shipments = pd.read_csv("data/Shipments.csv")
    return orders, inventory, shipments


def clean_data(orders, inventory, shipments):
    orders["order_date"] = pd.to_datetime(orders["order_date"])

    orders["order_status"] = orders["order_status"].str.strip().str.title()
    shipments["status"] = shipments["status"].str.strip().str.title()

    orders = orders.drop_duplicates(subset=["order_id"])
    inventory = inventory.drop_duplicates(subset=["product_id", "warehouse_id"])
    shipments = shipments.drop_duplicates(subset=["shipment_id"])

    return orders, inventory, shipments


def validate_data(orders, inventory, shipments):
    invalid_shipments = shipments[~shipments["order_id"].isin(orders["order_id"])]
    if not invalid_shipments.empty:
        print(
            f"Warning: {len(invalid_shipments)} shipments reference non-existent orders"
        )

    return orders, inventory, shipments


def process_data():
    orders, inventory, shipments = load_data()
    orders_clean, inventory_clean, shipments_clean = clean_data(
        orders, inventory, shipments
    )
    return validate_data(orders_clean, inventory_clean, shipments_clean)
