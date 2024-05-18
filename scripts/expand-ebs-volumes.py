import boto3

def expand_volumes(new_size):
    session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
    ec2 = session.resource('ec2')
    ec2_client = session.client('ec2')

    instances = ec2.instances.all()
    for instance in instances:
        for tag in instance.tags:
            if 'Name' == tag['Key']:
                name = tag['Value']
                for i in range(26, 41):
                    if f"aws-cloud9-WorkshopEnv{i}" in name:
                        for volume in instance.volumes.all():
                            if volume.size < new_size:
                                print(f"Expanding volume {volume.id} from {volume.size}GB to {new_size}GB")
                                ec2_client.modify_volume(VolumeId=volume.id, Size=new_size)

# Usage
expand_volumes(26)