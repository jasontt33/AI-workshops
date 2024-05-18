

import boto3

session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
iam = session.client('iam')

# Define the policy that gives PowerUserAccess
policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"

# Create 24 IAM users
for i in range(26, 41):
    username = f'user{i}'
    password = 'ChangeMe123!@#'

    # Create the user
    iam.create_user(UserName=username)

    # Create a login profile for the user (this enables console access)
    iam.create_login_profile(
        UserName=username,
        Password=password,
        PasswordResetRequired=True
    )

    # Attach the policy to the user
    iam.attach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

    print(f"Created and configured user: {username}")