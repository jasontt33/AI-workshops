import boto3
import json
import base64

def get_secret(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    # The secret returned is a string in JSON format, convert it to a dict
    secret_dict = json.loads(secret)

    return secret_dict

# Usage
secret_name = "dev/workshop/"
region_name = "us-east-1"
secret_dict = get_secret(secret_name, region_name)
print(secret_dict)