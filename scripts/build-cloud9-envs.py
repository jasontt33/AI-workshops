import boto3
from time import sleep

users = [f'user{i}' for i in range(26, 41)]

def create_cloud9_environment(env_name):
    session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
    client = session.client('cloud9')
    response = client.create_environment_ec2(
        name=env_name,
        description='Cloud9 Environment for Workshop',
        instanceType='t3.small',  # Choose the instance type
        automaticStopTimeMinutes=30,  # Adjust as needed
        subnetId='subnet-0909b906900e82a1d',  # Replace with your subnet ID
        imageId='amazonlinux-2-x86_64',  # Replace with your AMI ID
        ownerArn='arn:aws:iam::185666558041:user/jthompson-cli'
    )
    print(response)
    # Add members to the environment
    env_id = response['environmentId']
    for user in users:
        sleep(5)
        response = client.create_environment_membership(
            environmentId=env_id,
            userArn=f'arn:aws:iam::185666558041:user/{user}',
            permissions='read-write'  # Replace with the desired permission level
        )
    return response


def main():
    env_names = [f'WorkshopEnv{i}' for i in range(26, 41)]
    for name in env_names:
        response = create_cloud9_environment(name)
        print(f"Created Cloud9 Environment: {name}")

if __name__ == "__main__":
    main()
