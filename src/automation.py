import pandas as pd


def generate_restock_recommendations(
    ontology, threshold=20, safety_stock=10, min_restock=5, days_to_check=30
):
    latest_date = pd.to_datetime(ontology.orders["order_date"]).max()
    start_date = latest_date - pd.DateOffset(days_to_check)
    recent_orders = ontology.orders[
        (pd.to_datetime(ontology.orders["order_date"]) >= start_date)
        & (ontology.orders["order_status"].isin(["Delivered", "Shipped"]))
    ]

    demand = recent_orders.groupby("product_id").size()

    recommendations = ontology.inventory.merge(
        demand.rename("demand"), on="product_id", how="left"
    ).fillna(0)

    recommendations["recommended_restock_quantity"] = recommendations.apply(
        lambda row: max(
            min_restock, (row["demand"] + safety_stock) - row["stock_quantity"]
        )
        if row["stock_quantity"] < threshold
        else 0,
        axis=1,
    )

    return recommendations[(recommendations["recommended_restock_quantity"] > 0)][
        ["product_id", "warehouse_id", "recommended_restock_quantity"]
    ]
