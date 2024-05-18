import boto3

def add_security_group_to_instances(security_group_id):
    session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
    ec2 = session.resource('ec2')

    # Get all instances
    instances = ec2.instances.all()

    for instance in instances:
        # Check if instance state is 'running', 'pending', 'stopping' or 'stopped'
        if instance.state['Name'] in ['running', 'pending', 'stopping', 'stopped']:
            # Check if instance name starts with 'WorkshopEnv'
            for tag in instance.tags:
                if tag['Key'] == 'Name' and tag['Value'].startswith('aws-cloud9-'):
                    # Get the current security groups
                    all_security_groups = [sg['GroupId'] for sg in instance.security_groups]

                    # Add the new security group
                    all_security_groups.append(security_group_id)

                    # Update the instance with the new security groups
                    instance.modify_attribute(Groups=all_security_groups)

# Usage
add_security_group_to_instances('sg-0843eef061b636cc8')