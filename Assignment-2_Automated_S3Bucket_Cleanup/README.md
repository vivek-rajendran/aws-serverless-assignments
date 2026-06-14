# Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## 📌 Project Overview
This project demonstrates an automated serverless solution to optimize AWS storage costs by identifying and purging stale files. Using **AWS Lambda** and the **Boto3 SDK for Python**, the script automatically scans a target Amazon S3 bucket and deletes any objects that exceed a specific age threshold (e.g., 30 days). 

This solution is engineered to handle large-scale storage efficiently by utilizing S3 pagination templates, custom execution logic, and granular IAM security controls.

---

## 🛠️ Architecture Components

1. **Amazon S3**: Host storage bucket (`my-aws-automated-cleanup-bucket`) used to hold target files.
2. **AWS IAM**: A dedicated execution role (`LambdaS3CleanupRole`) with a managed `AmazonS3FullAccess` policy to securely grant object-deletion privileges.
3. **AWS Lambda**: A serverless function (`S3BucketCleanup`) running Python 3.14 that executes the cleanup script.

---

## 🚀 Step-by-Step Implementation Flow

### Step 1: S3 Bucket Setup & Baseline
* Created an S3 bucket named `my-aws-automated-cleanup-bucket`.
* Uploaded 7 sample PDF documents to establish a baseline for automated deletion tests.

### Step 2: IAM Security Configuration
* Provisionsed an IAM role named `LambdaS3CleanupRole`.
* Attached the `AmazonS3FullAccess` policy to grant the Lambda function authorization to look up (`s3:ListBucket`) and delete (`s3:DeleteObject`) items.

### Step 3: Lambda Function Deployment
* Created the serverless function `S3BucketCleanup` utilizing the **Python 3.14** runtime ecosystem.
* Linked the custom execution role configured in Step 2.
* Adjusted the default function timeout from **3.0 seconds to 30.0 seconds** to prevent `Sandbox.Timedout` limits during bulk object scanning.

### Step 4: Verification & Testing Run
* Configured a synchronous test event (`ManualS3Test`).
* Executed a live test run with a temporary testing threshold (`timedelta(days=0)`) to target and purge the newly uploaded testing files immediately.
* Reverted the script threshold to `timedelta(days=30)` for production deployment.

---

## 💻 Lambda Source Code (`lambda_function.py`)

```python
import boto3
import os
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # Initialize the boto3 S3 client
    s3_client = boto3.client('s3')
    
    # Target bucket name
    BUCKET_NAME = 'my-aws-automated-cleanup-bucket' 
    
    # Production threshold: Identify items older than 30 days
    age_threshold = datetime.now(timezone.utc) - timedelta(days=30)
    
    print(f"Starting cleanup routine for bucket: {BUCKET_NAME}")
    print(f"Target threshold (Deleting items older than): {age_threshold}")
    
    deleted_count = 0
    
    try:
        # List objects using a paginator to safely handle bulk objects
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    file_key = obj['Key']
                    file_last_modified = obj['LastModified']
                    
                    # Age validation check
                    if file_last_modified < age_threshold:
                        print(f"Deleting target match: {file_key} | Last Modified: {file_last_modified}")
                        
                        # Execute deletion command
                        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_key)
                        deleted_count += 1
                        
        print(f"Cleanup successfully completed. Total files purged: {deleted_count}")
        
        return {
            'statusCode': 200,
            'body': f"Execution successful. Cleaned {deleted_count} stale files from {BUCKET_NAME}."
        }
        
    except Exception as e:
        print(f"Execution failed with error: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Internal script error during cleanup execution: {str(e)}"
        }