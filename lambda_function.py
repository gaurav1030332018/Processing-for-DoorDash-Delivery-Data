import json
import boto3

# AWS clients
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Buckets and SNS topic
INPUT_BUCKET = "door-dashlanding-gb1"
OUTPUT_BUCKET = "doordash-target-gb1"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:078933838842:topic1"


def lambda_handler(event, context):
    try:
        # Get file details from event
        record = event['Records'][0]
        source_bucket = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']

        print(f"Processing file: s3://{source_bucket}/{file_key}")

        # Read the file from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        orders = json.loads(file_content)

        # Filter only delivered orders
        delivered_orders = [order for order in orders if order['status'] == 'delivered']

        # Save filtered orders to output bucket
        output_file_key = f"processed/{file_key}"
        s3_client.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_file_key,
            Body=json.dumps(delivered_orders, indent=4)
        )

        print(f"Filtered file saved to s3://{OUTPUT_BUCKET}/{output_file_key}")

        # Send SNS notification
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"File {file_key} processed. {len(delivered_orders)} delivered orders saved.",
            Subject="DoorDash Processing Complete"
        )

        return {"statusCode": 200, "message": "Processing complete"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "error": str(e)}
