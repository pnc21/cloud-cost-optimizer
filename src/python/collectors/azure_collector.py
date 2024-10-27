from azure.identity import ClientSecretCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

class AzureCostCollector:
    def __init__(self):
        load_dotenv()
        
        # Load Azure credentials
        self.credential = ClientSecretCredential(
            tenant_id=os.getenv('58aacd75-d157-41b5-ac70-cfab64997411'),
            client_id=os.getenv('AZ136074a7-8dd7-4bc6-8157-dd63b74bdc76'),
            client_secret=os.getenv('1075c46d-f194-4a45-94e8-15dc5acb92c1')
        )
        self.subscription_id = os.getenv('442ea53c-74a1-4939-988b-2d6c2a467050')
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
            return self._format_response(list(usage_details))
        except Exception as e:
            print(f"Error collecting Azure costs: {str(e)}")
            return None

    def _format_response(self, usage_details):
        formatted_data = []
        for detail in usage_details:
            cost_data = {
                'date': detail.usage_start.strftime('%Y-%m-%d'),
                'service': detail.consumed_service,
                'cost': float(detail.cost),
                'currency': detail.billing_currency
            }
            formatted_data.append(cost_data)
        return formatted_data

if __name__ == "__main__":
    collector = AzureCostCollector()
    costs = collector.get_cost_data()
    for cost in costs:
        print(f"Date: {cost['date']}, Service: {cost['service']}, Cost: {cost['cost']} {cost['currency']}")