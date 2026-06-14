import boto3

# Create EC2 client
ec2 = boto3.client('ec2')


def lambda_handler(event, context):
    """
    AWS Lambda function to manage EC2 instances based on tags.

    Action=Auto-Stop  -> Stops running EC2 instances
    Action=Auto-Start -> Starts stopped EC2 instances
    """

    try:

        print("===== EC2 Automation Started =====")

        stop_ids = []
        start_ids = []

        # ============================================================
        # Find instances tagged with Action=Auto-Stop
        # ============================================================
        stop_response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Action',
                    'Values': ['Auto-Stop']
                }
            ]
        )

        # Process Auto-Stop instances
        for reservation in stop_response['Reservations']:
            for instance in reservation['Instances']:

                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']

                print(
                    f"Auto-Stop Instance Found: "
                    f"{instance_id}, Current State: {instance_state}"
                )

                # Only stop instances that are currently running
                if instance_state == 'running':
                    stop_ids.append(instance_id)

        # Stop running instances
        if stop_ids:
            ec2.stop_instances(InstanceIds=stop_ids)

            print(
                f"Successfully initiated stop operation "
                f"for instances: {stop_ids}"
            )
        else:
            print("No running Auto-Stop instances found.")

        # ============================================================
        # Find instances tagged with Action=Auto-Start
        # ============================================================
        start_response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'tag:Action',
                    'Values': ['Auto-Start']
                }
            ]
        )

        # Process Auto-Start instances
        for reservation in start_response['Reservations']:
            for instance in reservation['Instances']:

                instance_id = instance['InstanceId']
                instance_state = instance['State']['Name']

                print(
                    f"Auto-Start Instance Found: "
                    f"{instance_id}, Current State: {instance_state}"
                )

                # Only start instances that are currently stopped
                if instance_state == 'stopped':
                    start_ids.append(instance_id)

        # Start stopped instances
        if start_ids:
            ec2.start_instances(InstanceIds=start_ids)

            print(
                f"Successfully initiated start operation "
                f"for instances: {start_ids}"
            )
        else:
            print("No stopped Auto-Start instances found.")

        print("===== EC2 Automation Completed Successfully =====")

        return {
            'statusCode': 200,
            'body': {
                'message': 'EC2 automation completed successfully',
                'stopped_instances': stop_ids,
                'started_instances': start_ids
            }
        }

    except Exception as e:

        print(f"ERROR: {str(e)}")

        return {
            'statusCode': 500,
            'body': {
                'message': 'EC2 automation failed',
                'error': str(e)
            }
        }