import boto3

def reboot_instances():
    ec2 = boto3.resource('ec2')

    # Get all instances
    instances = ec2.instances.all()

    for instance in instances:
        # Check if instance name starts with 'aws-cloud9-'
        for tag in instance.tags:
            if tag['Key'] == 'Name' and tag['Value'].startswith('aws-cloud9-WorkshopEnv'):
                print(f'Rebooting instance {instance.id}')
                instance.reboot()

# Usage
reboot_instances()