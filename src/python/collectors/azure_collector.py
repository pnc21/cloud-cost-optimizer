from azure.mgmt.consumption import ConsumptionManagementClient
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import json

class AzureCostCollector:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.subscription_id = "your_subscription_id"
        self.client = ConsumptionManagementClient(self.credential, self.subscription_id)

    def get_cost_data(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        try:
            usage_details = self.client.usage_details.list(
                scope=f"/subscriptions/{self.subscription_id}",
                filter=f"usageStart ge '{start_date}' and usageEnd le '{end_date}'"
            )
            return self._format_response(usage_details)
        except Exception as e:
            print(f"Error collecting Azure costs: {str(e)}")
            return None

    def _format_response(self, usage_details):
        formatted_data = []
        for detail in usage_details:
            cost_data = {
                'date': detail.usage_start,
                'service': detail.consumed_service,
                'cost': float(detail.cost),
                'currency': detail.billing_currency
            }
            formatted_data.append(cost_data)
        return formatted_data

if __name__ == "__main__":
    collector = AzureCostCollector()
    costs = collector.get_cost_data()
    print(json.dumps(costs, indent=2))