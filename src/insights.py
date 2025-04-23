import matplotlib.pyplot as plt
import pandas as pd


def calculate_delivery_times(ontology):
    merged = pd.merge(
        ontology.shipments[ontology.shipments["status"] == "Delivered"],
        ontology.orders,
        on="order_id",
    )

    merged["order_date"] = pd.to_datetime(merged["order_date"])
    merged["delivery_date"] = pd.to_datetime("today")
    merged["delivery_days"] = (merged["delivery_date"] - merged["order_date"]).dt.days

    return merged.groupby("carrier")["delivery_days"].mean().round(1)


def get_top_products(ontology, days=90):
    cutoff_date = pd.to_datetime("today") - pd.Timedelta(days=days)
    recent_orders = ontology.orders[ontology.orders["order_date"] >= cutoff_date]

    top_products = recent_orders["product_id"].value_counts().head(5).reset_index()
    top_products.columns = ["product_id", "units_sold"]
    return top_products


def plot_warehouse_shortages(ontology):
    demand = ontology.orders.groupby("product_id").size().reset_index(name="demand")

    shortage = ontology.inventory.merge(demand, on="product_id", how="left")
    shortage["shortage"] = (shortage["demand"] - shortage["stock_quantity"]).clip(
        lower=0
    )

    warehouse_shortage = (
        shortage.groupby("warehouse_id")["shortage"].sum().reset_index()
    )

    plt.figure(figsize=(12, 6))
    plt.bar(
        warehouse_shortage["warehouse_id"],
        warehouse_shortage["shortage"],
        color="#ff6961",
    )
    plt.title("Inventory Shortages by Warehouse (Based on Recent Demand)")
    plt.xlabel("Warehouse")
    plt.ylabel("Shortage Units")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return plt
