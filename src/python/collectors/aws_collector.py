import os
from dotenv import load_dotenv
import boto3
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class AWSCostCollector:
    def __init__(self):
        self.client = boto3.client('ce',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

    def get_cost_data(self, start_date=None, end_date=None):
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'}
                ]
            )
            return self._format_response(response)
        except Exception as e:
            print(f"Error collecting AWS costs: {str(e)}")
            return None

    def _format_response(self, response):
        costs = []
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                cost_data = {
                    'date': result['TimePeriod']['Start'],
                    'service': group['Keys'][0],
                    'cost': float(group['Metrics']['UnblendedCost']['Amount']),
                    'currency': group['Metrics']['UnblendedCost']['Unit']
                }
                costs.append(cost_data)
        return costs

if __name__ == "__main__":
    collector = AWSCostCollector()
    costs = collector.get_cost_data()
    print("AWS Costs:")
    for cost in costs:
        print(f"Date: {cost['date']}, Service: {cost['service']}, Cost: {cost['cost']} {cost['currency']}")