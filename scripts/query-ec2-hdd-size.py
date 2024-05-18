import boto3
import boto3.session

## boto3 script to query all ec2s and their storage volumes to see how large they are
session = boto3.session.Session(profile_name='sandbox', region_name='us-east-1')
ec2_client = boto3.client('ec2')

# Get all EC2 instances
response = ec2_client.describe_instances()

# Iterate over each reservation
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        
        # Get all attached volumes for the instance
        response = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_id]}])
        
        # Iterate over each volume
        for volume in response['Volumes']:
            volume_id = volume['VolumeId']
            volume_size = volume['Size']
            
            print(f"Instance ID: {instance_id}, Volume ID: {volume_id}, Volume Size: {volume_size} GB")
