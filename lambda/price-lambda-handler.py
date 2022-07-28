import os
import boto3

def handler(event, context):

    # price_per_km = int(os.environ['PRICE_PER_KM'])
    # price_per_minute = int(os.environ['PRICE_PER_MINUTE'])
    # base_fair = int(os.environ['BASE_FAIR'])
    # distance = int(os.environ['DISTANCE'])

    price_per_km = 1
    price_per_minute = 1
    base_fair = 3
    distance = 13
    """
        Assuming formula for caluclation for each trip we are assuming is:
            fair_price = ( (price_per_km * 1) + (price_per_minute *1.5)) * distance + base_fair 
    """

    fair_price = ( (price_per_km * 1) + (price_per_minute *1.5)) * distance + base_fair 
    print("Fair Price:", fair_price)

    # Create SQS client
    sqs = boto3.client('sqs')

    queue_url = 'SQS_QUEUE_URL'

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'Message': {
                'DataType': 'String',
                'StringValue': "Ride is ready for you"
            },
            'Person': {
                'DataType': 'String',
                'StringValue': 'Person1'
            }
        },
        MessageBody=(
            f"Ride is ready for you with calculated Price{fair_price}"
        )
    )
    print(response['MessageId'])

    return {
        'statusCode': 200,
        'result': fair_price,
        'body': 'Lambda was invoked successfully and message sent to users'
    }