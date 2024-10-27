from collectors.aws_collector import AWSCostCollector
from collectors.azure_collector import AzureCostCollector
from datetime import datetime
import json
from pymongo import MongoClient

class CostAnalyzer:
    def __init__(self):
        self.aws_collector = AWSCostCollector()
        self.azure_collector = AzureCostCollector()
        self.mongo_client = MongoClient('mongodb://localhost:27017/')
        self.db = self.mongo_client['cloud_costs']

    def collect_all_costs(self):
        # Collect costs from all providers
        aws_costs = self.aws_collector.get_cost_data()
        azure_costs = self.azure_collector.get_cost_data()

        # Format and store data
        timestamp = datetime.now().strftime('%Y-%m-%d')
        
        cost_data = {
            'timestamp': timestamp,
            'aws': aws_costs if aws_costs else [],
            'azure': azure_costs if azure_costs else [],
            'total_aws': sum(cost['cost'] for cost in aws_costs) if aws_costs else 0,
            'total_azure': sum(cost['cost'] for cost in azure_costs) if azure_costs else 0
        }

        # Store in MongoDB
        self.db.cost_records.insert_one(cost_data)
        return cost_data

    def get_cost_summary(self):
        latest_costs = self.db.cost_records.find_one(
            sort=[('timestamp', -1)]
        )
        return {
            'aws_total': latest_costs['total_aws'],
            'azure_total': latest_costs['total_azure'],
            'total': latest_costs['total_aws'] + latest_costs['total_azure'],
            'timestamp': latest_costs['timestamp']
        }

if __name__ == "__main__":
    analyzer = CostAnalyzer()
    costs = analyzer.collect_all_costs()
    print(json.dumps(costs, indent=2))