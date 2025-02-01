from google.cloud import billing
from google.cloud.billing import CloudBillingClient
from datetime import datetime, timedelta
import json

class GCPCostCollector:
    def __init__(self):
        self.client = CloudBillingClient()
        self.billing_account = "your-billing-account"

    def get_cost_data(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        try:
            request = billing.QueryCostsRequest(
                billing_account=f"billingAccounts/{self.billing_account}",
                date_range={
                    'start_date': {'year': int(start_date[:4]), 'month': int(start_date[5:7]), 'day': int(start_date[8:])},
                    'end_date': {'year': int(end_date[:4]), 'month': int(end_date[5:7]), 'day': int(end_date[8:])}
                }
            )
            response = self.client.query_costs(request)
            return self._format_response(response)
        except Exception as e:
            print(f"Error collecting GCP costs: {str(e)}")
            return None

    def _format_response(self, response):
        formatted_data = []
        for cost_info in response.cost_info:
            cost_data = {
                'date': cost_info.start_time.strftime('%Y-%m-%d'),
                'service': cost_info.service.name,
                'cost': float(cost_info.cost.amount),
                'currency': cost_info.cost.currency
            }
            formatted_data.append(cost_data)
        return formatted_data

if __name__ == "__main__":
    collector = GCPCostCollector()
    costs = collector.get_cost_data()
    print(json.dumps(costs, indent=2))