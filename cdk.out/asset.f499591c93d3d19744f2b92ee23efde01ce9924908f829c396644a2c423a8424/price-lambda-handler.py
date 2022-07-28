import os
from datetime import datetime


def handler(event, context):

    price_per_km = int(os.environ['PRICE_PER_KM'])
    price_per_minute = int(os.environ['PRICE_PER_MINUTE'])
    base_fair = int(os.environ['BASE_FAIR'])
    distance = int(os.environ['DISTANCE'])

    """
        Assuming formula for caluclation for each trip we are assuming is:
            total_price = ( (price_per_km * 1) + (price_per_minute *1.5) + base_fair ) / distance
    """

    fair_price = ( (price_per_km * 1) + (price_per_minute *1.5) + base_fair ) / distance
    print("Fair Price:", fair_price)
    return {
        'statusCode': 200,
        'result': fair_price,
        'body': 'Lambda was invoked successfully.'
    }

