import os

import pandas as pd

from src.automation import generate_restock_recommendations
from src.data_processing import process_data
from src.insights import (
    calculate_delivery_times,
    get_top_products,
    plot_warehouse_shortages,
)
from src.ontology import LogisticsOntology


def main():
    os.makedirs("output", exist_ok=True)

    orders, inventory, shipments = process_data()

    ontology = LogisticsOntology(orders, inventory, shipments)

    recommendations = generate_restock_recommendations(ontology)
    recommendations.to_csv("output/restock_recommendations.csv", index=False)

    top_products = get_top_products(ontology)
    top_products.to_csv("output/top_products.csv", index=False)

    delivery_times = calculate_delivery_times(ontology)
    pd.DataFrame(delivery_times).to_csv("output/average_delivery_times.csv", index=True)

    plot_warehouse_shortages(ontology).savefig("output/warehouse_shortages.png")


if __name__ == "__main__":
    main()
