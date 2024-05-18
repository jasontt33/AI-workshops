import boto3

def delete_cloud9_environment(environment_name):
    session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
    client = session.client('cloud9')

    # List all environments
    environments = client.list_environments()

    # Find the environment ID of the environment with the given name
    environment_id = None
    for environment in environments['environmentIds']:
        environment_info = client.describe_environments(
            environmentIds=[environment]
        )
        if environment_info['environments'][0]['name'] == environment_name:
            environment_id = environment
            break

    # If the environment was found, delete it
    if environment_id is not None:
        client.delete_environment(
            environmentId=environment_id
        )
        print(f"Deleted environment {environment_name}")
    else:
        print(f"Environment {environment_name} not found")

# Replace 'my-environment' with the name of the environment you want to delete

# Replace 'my-environment' with the name of the environment you want to delete
delete_cloud9_environment('WorkshopEnv1')
delete_cloud9_environment('WorkshopEnv2')
delete_cloud9_environment('WorkshopEnv3')
delete_cloud9_environment('WorkshopEnv6')