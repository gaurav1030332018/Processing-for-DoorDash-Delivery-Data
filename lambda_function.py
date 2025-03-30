import json
import boto3
import os

s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# Set your SNS Topic ARN (Replace with actual ARN)
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:078933838842:topic1"

def lambda_handler(event, context):
    try:
        # Extract bucket name and object key from S3 event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        print(f"Processing file: s3://{bucket_name}/{object_key}")

        # Read the uploaded JSON file from S3
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        file_content = file_obj['Body'].read().decode('utf-8')

        # Parse JSON data
        data = json.loads(file_content)

        # Filter records with status "delivered"
        delivered_orders = [order for order in data if order.get('status') == "delivered"]

        if not delivered_orders:
            print("No delivered orders found.")
            return {"statusCode": 200, "message": "No delivered orders found."}

        # Convert filtered data to JSON
        filtered_data_json = json.dumps(delivered_orders, indent=4)

        # Define the output file name
        output_key = object_key.replace("raw_input", "filtered_output")

        # Define the target bucket
        target_bucket = "doordash-target-gb1"

        # Save the filtered JSON data to the target S3 bucket
        s3_client.put_object(Bucket=target_bucket, Key=output_key, Body=filtered_data_json)

        print(f"Filtered data saved to s3://{target_bucket}/{output_key}")

        # Send SNS notification
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"File {object_key} processed successfully. Filtered data saved to {target_bucket}/{output_key}.",
            Subject="DoorDash Data Processing Success"
        )

        return {
            "statusCode": 200,
            "message": "Processing completed successfully."
        }

    except Exception as e:
        print(f"Error: {str(e)}")

        # Send error notification to SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Error processing file {object_key}: {str(e)}",
            Subject="DoorDash Data Processing Failed"
        )

        return {
            "statusCode": 500,
            "error": str(e)
        }
