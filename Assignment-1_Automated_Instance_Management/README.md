# AWS Serverless Assignments

## Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

### Objective

The objective of this assignment is to gain hands-on experience with AWS Lambda and Boto3 by automating the management of Amazon EC2 instances based on instance tags.

The Lambda function performs the following actions:

* Detects EC2 instances tagged with `Action=Auto-Stop` and stops them.
* Detects EC2 instances tagged with `Action=Auto-Start` and starts them.
* Logs the affected instance IDs in Amazon CloudWatch.

---

## Architecture

```text
EC2 Instance 1 (Action=Auto-Stop)
                |
                |
                v
         AWS Lambda
     (EC2InstanceManager)
                ^
                |
                |
EC2 Instance 2 (Action=Auto-Start)
```

---

## Technologies Used

* AWS EC2
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Python 3.x
* Boto3 SDK

---

## Prerequisites

* AWS Account
* IAM permissions to create EC2, Lambda, and IAM resources
* Python Runtime (AWS Lambda)
* Git and GitHub

---

## Step 1: Create EC2 Instances

Created two Amazon EC2 instances using Amazon Linux 2023 AMI and t2.micro instance type.

### Instance 1

| Property      | Value                 |
| ------------- | --------------------- |
| Name          | Serverless-Instance-1 |
| Instance Type | t2.micro              |
| Tag Key       | Action                |
| Tag Value     | Auto-Stop             |

### Instance 2

| Property      | Value                 |
| ------------- | --------------------- |
| Name          | Serverless-Instance-2 |
| Instance Type | t2.micro              |
| Tag Key       | Action                |
| Tag Value     | Auto-Start            |

---

## Step 2: Create IAM Role

Created an IAM role for AWS Lambda.

### Policies Attached

* AmazonEC2FullAccess
* AWSLambdaBasicExecutionRole

Role Name:

```text
Lambda-EC2-Manager-Role
```

---

## Step 3: Create Lambda Function

Function Name:

```text
EC2InstanceManager
```

Runtime:

```text
Python 3.x
```

Execution Role:

```text
Lambda-EC2-Manager-Role
```

---

## Step 4: Lambda Function Code

```python
import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Find Auto-Stop instances
    stop_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            }
        ]
    )

    stop_ids = []

    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print("Stopped instances:", stop_ids)

    # Find Auto-Start instances
    start_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    start_ids = []

    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print("Started instances:", start_ids)

    return {
        'statusCode': 200,
        'body': 'EC2 automation completed successfully'
    }
```

---

## Boto3 Operations Performed

### Describe Instances

```python
ec2.describe_instances()
```

Used to retrieve EC2 instances based on tags.

### Stop Instances

```python
ec2.stop_instances()
```

Used to stop instances tagged as:

```text
Action=Auto-Stop
```

### Start Instances

```python
ec2.start_instances()
```

Used to start instances tagged as:

```text
Action=Auto-Start
```

---

## Testing

### Before Execution

| Instance Tag | State   |
| ------------ | ------- |
| Auto-Stop    | Running |
| Auto-Start   | Stopped |

### Lambda Invocation

Lambda function was manually invoked using a test event:

```json
{}
```

### After Execution

| Instance Tag | State   |
| ------------ | ------- |
| Auto-Stop    | Stopped |
| Auto-Start   | Running |

---

## Screenshots

### EC2 Instances

![EC2 Instances](screenshots/01-ec2-instances-tags.png)

### IAM Role

![IAM Role](screenshots/02-iam-role.png)

### Lambda Function Code

![Lambda Code](screenshots/03-lambda-code.png)

### Before Execution

![Before Execution](screenshots/04-before-execution.png)

### Lambda Execution Success

![Lambda Success](screenshots/05-lambda-success.png)

### After Execution

![After Execution](screenshots/06-after-execution.png)

### CloudWatch Logs

![CloudWatch Logs](screenshots/07-cloudwatch-logs.png)

---

## Result

Successfully implemented an AWS Lambda function using Boto3 to automatically manage EC2 instances based on instance tags.

The Lambda function:

* Stopped instances tagged with `Action=Auto-Stop`
* Started instances tagged with `Action=Auto-Start`
* Logged execution details to CloudWatch

This demonstrates serverless automation using AWS Lambda and Amazon EC2.
