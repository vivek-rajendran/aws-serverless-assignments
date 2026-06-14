import boto3
import os
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    """
    AWS Lambda handler that connects to a specified S3 bucket and deletes 
    all objects that have not been modified within the last 30 days.
    """
    # 1. Initialize the boto3 S3 client
    s3_client = boto3.client('s3')
    
    # TODO: Replace with your actual S3 bucket name
    BUCKET_NAME = 'my-automated-cleanup-bucket-123' 
    
    # Define our age threshold (30 days ago from right now)
    # AWS S3 stores metadata timestamps in UTC, so we must use timezone.utc
    age_threshold = datetime.now(timezone.utc) - timedelta(days=30)
    
    print(f"Starting cleanup routine for bucket: {BUCKET_NAME}")
    print(f"Target threshold (Deleting items older than): {age_threshold}")
    
    deleted_count = 0
    
    try:
        # 2. List objects using a paginator
        # Paginators handle buckets with >1,000 files gracefully without truncation
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME)
        
        for page in pages:
            # Check if the bucket contains any keys/objects
            if 'Contents' in page:
                for obj in page['Contents']:
                    file_key = obj['Key']
                    file_last_modified = obj['LastModified']
                    
                    # 3. Check if the object's age exceeds 30 days
                    if file_last_modified < age_threshold:
                        # 4. Print the name of the deleted object for cloud logs
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