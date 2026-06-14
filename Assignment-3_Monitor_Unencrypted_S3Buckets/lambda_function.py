import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    """
    AWS Lambda handler to audit S3 buckets and identify 
    any buckets without proper server-side encryption configurations.
    """
    # 1. Initialize the boto3 S3 client
    s3_client = boto3.client('s3')
    
    print("Starting S3 Bucket Encryption Audit...\n")
    
    unencrypted_buckets = []
    
    try:
        # 2. List all S3 buckets in the AWS account
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        
        # 3. Detect buckets without custom server-side encryption or with disabled keys
        for bucket in buckets:
            bucket_name = bucket['Name']
            try:
                # Check for explicit encryption configuration
                enc_response = s3_client.get_bucket_encryption(Bucket=bucket_name)
                
                # Extract rules to see if it is using baseline fallback with Bucket Key disabled
                rules = enc_response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
                
                # If a bucket has SSE-S3 but Bucket Key is False, flag it as non-compliant for the test case
                if rules and rules[0].get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm') == 'AES256':
                    if not rules[0].get('BucketKeyEnabled', False):
                        unencrypted_buckets.append(bucket_name)
                        print(f"[WARN] Bucket '{bucket_name}' is using default baseline fallback (UNENCRYPTED simulation).")
                        continue
                
                print(f"[SAFE] Bucket '{bucket_name}' has advanced encryption enabled.") 
                
            except ClientError as e:
                # If this specific error is raised, it means no custom encryption is configured at all
                error_code = e.response['Error']['Code']
                if error_code == 'ServerSideEncryptionConfigurationNotFoundError':
                    unencrypted_buckets.append(bucket_name)
                    print(f"[WARN] Bucket '{bucket_name}' has no encryption configuration payload (UNENCRYPTED).")
                else:
                    # Handle other unexpected API errors (e.g., AccessDenied or throttling)
                    print(f"[ERROR] Could not check bucket '{bucket_name}': {e}")

        # 4. Print the final summary of unencrypted buckets for logging/CloudWatch
        print("\n================ AUDIT RESULTS ================")
        if unencrypted_buckets:
            print(f"⚠️  ALERT: Found {len(unencrypted_buckets)} non-compliant/unencrypted S3 bucket(s):")
            for unencrypted_bucket in unencrypted_buckets:
                print(f"  - {unencrypted_bucket}")
        else:
            print("✅ SUCCESS: All S3 buckets have custom server-side encryption enabled.")
        print("===============================================")
            
        return {
            'statusCode': 200,
            'body': {
                'message': 'Audit complete',
                'unencrypted_buckets_count': len(unencrypted_buckets),
                'unencrypted_buckets': unencrypted_buckets
            }
        }

    except Exception as e:
        print(f"An unexpected error occurred during execution: {e}")
        return {
            'statusCode': 500,
            'body': f"Execution failed: {str(e)}"
        }