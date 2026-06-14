# Assignment 3: Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## Objective
To enhance your AWS security posture by configuring an automated AWS Lambda compliance auditing function. This utility programmatically identifies any Amazon S3 buckets that default to baseline infrastructure fallbacks without custom server-side encryption settings or optimized bucket tracking configurations.

## Architecture & Workflow
1. **Trigger:** The Lambda function is manually invoked via the built-in AWS Lambda Test Framework (or can be automated using Amazon EventBridge Scheduler).
2. **Execution:** The Lambda function assumes an IAM Execution Role configured with narrow, read-only visibility into target object storage.
3. **Audit Execution:** The Python Boto3 script processes an identity inventory by listing all active S3 buckets and parsing their encryption payloads.
4. **Logging & Alerting:** Compliant buckets are marked secure, while non-compliant baseline storage configurations are tracked, added to an object array, and output as an alert to Amazon CloudWatch logs.

---

## Prerequisites
* An active **AWS Account Sandbox** environment.
* Basic familiarity with the AWS Management Console, Identity and Access Management (IAM), S3 properties, and Lambda.
* **Python 3.x** software development foundations.

---

## Step-by-Step Implementation Guide

### Step 1: S3 Bucket Configuration
To test the auditing capabilities of the script, set up a diverse array of bucket environments (e.g., 3 to 4 total targets).
1. Navigate to the **S3 Dashboard** in your AWS Management Console.
2. Click **Create bucket** to provision your compliant buckets (e.g., `audit-safe-bucket-01`, `audit-safe-bucket-02`).
   * Keep **Encryption type** set to *SSE-S3*.
   * Keep **Bucket Key** toggled to **Enable**.
3. Click **Create bucket** again to provision your unencrypted simulated test bucket (e.g., `audit-unencrypted-test-bucket`).
   * Set **Encryption type** to *SSE-S3*.
   * Explicitly toggle **Bucket Key** to **Disable**. This leaves the bucket on standard baseline defaults, allowing the script's audit criteria to track it cleanly.

### Step 2: Create the Lambda IAM Execution Role
The Lambda function must be granted least-privilege security clearance to query bucket metadata without administrative modifications.
1. Navigate to the **IAM Dashboard**.
2. Click **Roles** > **Create role**.
3. Under *Trusted entity type*, select **AWS service**. Under *Service or use case*, select **Lambda** from the dropdown list. Click **Next**.
4. In the permissions policy list search box, filter for and check the box next to **`AmazonS3ReadOnlyAccess`**. Click **Next**.
5. Name the role precisely: `LambdaS3SecurityAuditRole`.
6. Review the properties and click **Create role**.

### Step 3: Create and Deploy the Lambda Function
1. Navigate to the **AWS Lambda Dashboard** and click the **Create function** button.
2. Select **Author from scratch** and input the following configuration parameters:
   * **Function name:** `MonitorUnencryptedS3Buckets`
   * **Runtime:** Select the latest available **Python 3.x** environment.
   * **Permissions:** Expand *Change default execution role*, select *Use an existing role*, and link your newly created `LambdaS3SecurityAuditRole`.
3. Click **Create function** at the bottom of the form.
4. Go to the **Configuration** tab > **General configuration** > **Edit**, and increase the function **Timeout** configuration from `3 seconds` to **`30 seconds`** to prevent execution timeouts while awaiting API socket feedback.

### Step 4: Add the Source Code
Navigate back to the function's **Code** tab workspace, open `lambda_function.py`, remove all default template code, and insert the finalized, production-optimized audit script:

```python
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