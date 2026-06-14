import boto3
import os
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # 1. Initialize the boto3 S3 client
    s3_client = boto3.client('s3')
    
    # Target bucket name
    BUCKET_NAME = 'my-aws-automated-cleanup-bucket' 
    
    # TEMPORARY FOR TESTING: Set to 0 days so it matches the newly uploaded files!
    # Once testing is verified, we will change this back to 30.
    age_threshold = datetime.now(timezone.utc) - timedelta(days=30)
    
    print(f"Starting cleanup routine for bucket: {BUCKET_NAME}")
    print(f"Target threshold (Deleting items older than): {age_threshold}")
    
    deleted_count = 0
    
    try:
        # 2. List objects using a paginator
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    file_key = obj['Key']
                    file_last_modified = obj['LastModified']
                    
                    # 3. Age validation
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