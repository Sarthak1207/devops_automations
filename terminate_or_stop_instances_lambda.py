import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Get the action from the event (either 'terminate' or 'stop')
    action = event.get('action', '').lower()
    
    if action not in ['terminate', 'stop']:
        return {
            'statusCode': 400,
            'body': "Invalid action. Please specify 'terminate' or 'stop'."
        }
    
    # Get all running instances
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    
    # Extract instance IDs
    instance_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    
    if not instance_ids:
        return {
            'statusCode': 200,
            'body': "No running instances found."
        }
    
    # Perform the requested action
    if action == 'terminate':
        terminate_response = ec2_client.terminate_instances(InstanceIds=instance_ids)
        return {
            'statusCode': 200,
            'body': f"Terminated instances: {instance_ids}",
            'details': terminate_response
        }
    elif action == 'stop':
        stop_response = ec2_client.stop_instances(InstanceIds=instance_ids)
        return {
            'statusCode': 200,
            'body': f"Stopped instances: {instance_ids}",
            'details': stop_response
        }