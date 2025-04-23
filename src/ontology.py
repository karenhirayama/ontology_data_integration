import pandas as pd


class LogisticsOntology:
    def __init__(self, orders, inventory, shipments):
        self.orders = orders
        self.inventory = inventory
        self.shipments = shipments
        
        self.product_warehouses = inventory.groupby('product_id')['warehouse_id'].apply(list).to_dict()
        self.order_shipments = shipments.groupby('order_id').first().to_dict(orient='index')
        
        self._build_cross_functional_indices()

    def _build_cross_functional_indices(self):
        self.shipment_analysis = pd.merge(
            self.shipments,
            self.orders[['order_id', 'product_id', 'order_date']],
            on='order_id'
        )
        
        self.carrier_lead_times = (
            self.shipment_analysis
            .groupby(['product_id', 'carrier'])
            ['order_date'].apply(lambda x: (pd.to_datetime('today') - x).dt.days.mean())
            .unstack()
        )

    def predict_inventory_needs(self, safety_factor=1.2, days_to_check=30, lead_time_if_missing=7):
        demand = self.orders.groupby('product_id').size()
        
        recommendations = (
            self.inventory
            .merge(demand.rename('monthly_demand'), on='product_id', how='left')
            .merge(self.carrier_lead_times.stack().rename('lead_time'), 
                  on='product_id', how='left')
            .fillna({'lead_time': lead_time_if_missing})
        )
        
        recommendations['needed_stock'] = (
            (recommendations['monthly_demand'] / days_to_check * 
             recommendations['lead_time'] * 
             safety_factor
        ).round().astype(int))
        
        return recommendations