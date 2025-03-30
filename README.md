# Processing for DoorDash Delivery Data

## Overview
This project automates the processing of daily delivery data from DoorDash using AWS services. When a JSON file containing delivery records is uploaded to an Amazon S3 bucket, an AWS Lambda function is triggered to filter records based on delivery status and store the filtered data in another S3 bucket. Notifications regarding the processing outcome are sent via Amazon SNS.

## Requirements
- AWS Account
- Amazon S3 buckets: `doordash-landing-zn` and `doordash-target-zn`
- AWS Lambda
- Amazon SNS
- AWS IAM (for permissions)
- AWS CodeBuild (for CI/CD)
- GitHub (for version control)
- Python & Pandas library
- Email subscription for SNS notifications

## Steps

### 1️⃣ Sample JSON File for Daily Data
A sample JSON file named `2024-03-09-raw_input.json` contains 10 delivery records with different statuses such as `cancelled`, `delivered`, and `order placed`:

```json
{"id": 1, "status": "delivered", "amount": 20.5, "date": "2024-03-09"}
{"id": 2, "status": "cancelled", "amount": 15.0, "date": "2024-03-09"}
{"id": 3, "status": "order placed", "amount": 22.5, "date": "2024-03-09"}
...
```

Daily JSON files will be uploaded to `doordash-landing-zn` with the format `yyyy-mm-dd-raw_input.json`. Upon file upload, data processing starts automatically.

### 2️⃣ Set Up S3 Buckets
- Create **two S3 buckets**:
  - `doordash-landing-zn` (for incoming raw files)
  - `doordash-target-zn` (for processed files)

### 3️⃣ Set Up Amazon SNS Topic
- Create an **SNS topic** for sending processing notifications.
- Subscribe an **email** to the topic to receive notifications.

### 4️⃣ Create IAM Role for Lambda
- Create an **IAM role** with the following permissions:
  - Read from `doordash-landing-zn`
  - Write to `doordash-target-zn`
  - Publish messages to the **SNS topic**

### 5️⃣ Create and Configure AWS Lambda Function
- Use **Python** as the runtime.
- Include the **pandas library** in the deployment package or use a Lambda Layer.
- Set up an **S3 trigger** to invoke the function when files are uploaded to `doordash-landing-zn`.

#### Lambda Function Workflow
1. Read the JSON file into a **pandas DataFrame**.
2. **Filter** records where `status` is **"delivered"**.
3. Write the filtered DataFrame to a **new JSON file** in `doordash-target-zn`.
4. Publish a **success/failure notification** to the **SNS topic**.

### 6️⃣ AWS CodeBuild for CI/CD
- Host the Lambda function code on **GitHub**.
- Set up an **AWS CodeBuild project** linked to your repository.
- Configure `buildspec.yml` for **automated deployment** of Lambda function updates.

### 7️⃣ Testing and Verification
- Upload the **sample JSON file** to `doordash-landing-zn`.
- Verify that the **Lambda function** triggers correctly.
- Check `doordash-target-zn` for the processed file and confirm its contents.
- Ensure you **receive an email notification** about processing completion.



---


