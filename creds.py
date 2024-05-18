import boto3
import base64
from botocore.exceptions import ClientError
import json
import os

def get_it():

    secret_name = "dev/workshop/"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.

    sec = json.loads(secret)
   
    ## 'getters' to be used in other modules
    get_it.openai_api_key = sec["OPENAI_API_KEY"]
    get_it.azure_openai_api_key = sec["AZURE_API_KEY"]
    get_it.azure_openai_endpoint = sec["AZURE_API_ENDPOINT"]
    get_it.azure_openai_version = sec["AZURE_API_VERSION"]

get_it()