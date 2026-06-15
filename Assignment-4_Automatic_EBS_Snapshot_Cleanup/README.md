# Assignment 4: Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## Objective
To architect a serverless, cost-optimized automation pipeline using AWS Lambda and Python (Boto3). This workflow programmatically backs up critical enterprise storage components by generating localized Amazon Elastic Block Store (EBS) snapshots while automatically auditing and purging expired snapshots older than 30 days to limit infrastructure waste.

## Architectural Overview
1. **Trigger Engine:** Manual validation through the AWS Console Test Framework or scheduled automation driven via Amazon EventBridge Rules (CloudWatch Events).
2. **Compute Core:** A runtime environment executing Python 3.x inside AWS Lambda.
3. **Identity Brokerage:** An execution IAM Role giving the compute layer access to create, manipulate, and terminate EC2 storage snapshots.
4. **Target Resource:** A dedicated Amazon Elastic Block Store (EBS) volume.
5. **Telemetry Logs:** CloudWatch logs capturing step-by-step structural output detailing all adjustments.

---

## Step-by-Step Implementation Guide

### Step 1: Baseline Storage Inventory Setup
1. Navigate to the **Amazon EC2 Dashboard** and locate the **Elastic Block Store -> Volumes** sidebar segment.
2. Select an existing EBS volume or create a small test volume (e.g., 1 GiB GP3).
3. Extract and preserve the explicit alpha-numeric string representing the **Volume ID** (e.g., `vol-0xxxxxxxxxxxxxxxx`).

### Step 2: Provisioning the Lambda Execution IAM Role
1. Navigate to the **IAM Console** and proceed to create a new execution role targeting AWS Lambda.
2. Under Permissions, attach an architectural policy capable of standard snapshot manipulation. 
   * *For Sandbox simplicity:* Attach `AmazonEC2FullAccess`.
   * *For Real-World Security Compliance:* Ensure narrow principle-of-least-privilege boundaries using custom actions (`ec2:CreateSnapshot`, `ec2:DeleteSnapshot`, `ec2:DescribeSnapshots`, `ec2:CreateTags`).
3. Name the role explicitly: `LambdaEBSSnapshotLifecycleRole`.

### Step 3: Deployment of the Lambda Function
1. Navigate to the **AWS Lambda Console** and create a new function titled `EBS-Snapshot-Lifecycle-Manager`.
2. Configure the system environment with **Python 3.x** as the primary runtime.
3. Under the **Change default execution role** dropdown, select the existing role matching `LambdaEBSSnapshotLifecycleRole`.
4. Replace the default template with the provided `lambda_function.py` code. Ensure you input your extracted Volume ID inside the configuration block or declare it via the *Configuration -> Environment Variables* panel under the key name `TARGET_VOLUME_ID`.
5. Deploy the changes.

### Step 4: Event-Driven Automation Trigger Setup (Bonus)
1. Select **Add Trigger** from the Lambda Function visual designer layout.
2. Select **EventBridge (CloudWatch Events)** from the source inventory list.
3. Choose **Create a new rule**. Name the pattern: `WeeklyEBSSnapshotSchedule`.
4. Configure a standard schedule pattern expression like `rate(7 days)` or use a Cron string to coordinate routine automated invocation.

### Step 5: Manual Invocation & Lifecycle Validation
1. Click **Test** within the Lambda development console block to produce a dummy test event.
2. Trigger the code manually and await execution completion.
3. Observe the outputs rendered via execution logs to verify programmatic asset updates.