# Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

An automated, serverless solution designed to maintain AWS S3 storage hygiene. This project utilizes an AWS Lambda function written in Python (Boto3) to scan a specific S3 bucket and automatically delete objects that are older than 30 days.

## 🚀 Project Overview

As cloud data grows, retaining stale files can lead to unnecessary accumulation and inflated AWS storage costs. This project implements a lightweight automation script that evaluates the `LastModified` timestamp of S3 objects against a UTC-standard 30-day threshold, purging outdated files while logging actions for audit purposes.

---

## 🛠️ Architecture Components

*   **Amazon S3:** The storage target holding the files.
*   **AWS Lambda (Python 3.x):** The serverless execution environment handling the logic.
*   **AWS IAM:** Provides the specific security role granting the Lambda execution environment authority to manage objects inside S3.
*   **Boto3:** The AWS SDK for Python used to paginate through bucket contents and issue deletion commands.

---

## 📋 Implementation Steps

### 1. S3 Bucket Configuration
1. Navigate to the **S3 Dashboard** in the AWS Console.
2. Click **Create bucket**, specify a unique name (e.g., `my-automated-cleanup-bucket`), and retain the default settings.
3. Upload several test files into the bucket. 
   > 💡 *Note: S3 timestamps are generated server-side upon upload. For rapid manual testing, you can adjust the `days=30` variable in the script to `days=0` to evaluate the code against newly uploaded files.*

### 2. IAM Execution Role Setup
1. Open the **IAM Dashboard**.
2. Select **Roles** > **Create role**.
3. Choose **AWS Service** as the trusted entity and select **Lambda**.
4. Attach the `AmazonS3FullAccess` policy. *(Note: For production, remember to scope this down to the specific bucket ARN using Least Privilege principles).*
5. Name the role (e.g., `LambdaS3CleanupRole`) and click **Create**.

### 3. Lambda Deployment
1. Navigate to the **AWS Lambda Dashboard** and select **Create function** (Author from scratch).
2. Configure with:
   * **Runtime:** Python 3.x
   * **Execution Role:** Use an existing role -> Select `LambdaS3CleanupRole`
3. Paste the cleanup script provided below into the code editor.
4. Update the `BUCKET_NAME` variable placeholder with your actual S3 bucket name.
5. Click **Deploy**.

---

## 💻 Script Source Code

```python
import boto3
import os
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # Initialize the boto3 S3 client
    s3_client = boto3.client('s3')
    
    # Configuration - Replace with your bucket name
    BUCKET_NAME = 'my-automated-cleanup-bucket' 
    
    # Establish UTC time threshold (30 days ago)
    age_threshold = datetime.now(timezone.utc) - timedelta(days=30)
    
    print(f"Starting cleanup for bucket: {BUCKET_NAME}")
    print(f"Targeting files modified before: {age_threshold}")
    
    deleted_count = 0
    
    try:
        # Utilize S3 Page Iterator to safely handle large buckets (>1000 objects)
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    file_key = obj['Key']
                    file_last_modified = obj['LastModified']
                    
                    # Evaluate object age
                    if file_last_modified < age_threshold:
                        print(f"Deleting: {file_key} (Modified: {file_last_modified})")
                        s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_key)
                        deleted_count += 1
                        
        print(f"Cleanup complete. Total files deleted: {deleted_count}")
        return {
            'statusCode': 200,
            'body': f"Successfully deleted {deleted_count} old files."
        }
        
    except Exception as e:
        print(f"Error occurred during execution: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error cleaning bucket: {str(e)}"
        }