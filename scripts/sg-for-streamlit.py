import boto3

def create_security_group_with_inbound_rule(group_name, description, vpc_id):
    session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
    ec2 = session.client('ec2')

    # Create security group
    response = ec2.create_security_group(
        GroupName=group_name,
        Description=description,
        VpcId=vpc_id
    )

    security_group_id = response['GroupId']

    # Add tags
    ec2.create_tags(
        Resources=[security_group_id],
        Tags=[
            {'Key': 'Owner', 'Value': 'rogerTheDeveloper'},
            {'Key': 'Project', 'Value': 'Workshop'}
        ]
    )

    # Add inbound rule
    data = ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 8500,
                'ToPort': 8599,
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            }
        ]
    )

    print(f'Security Group Created {security_group_id} in vpc {vpc_id}.')

# Usage
create_security_group_with_inbound_rule('workshop-sg', 'workshop-sg', 'vpc-02008038be9d185c4')