import boto3

# Create IAM client
session = boto3.Session(profile_name='sandbox', region_name='us-east-1')
iam = session.client('iam')

# Define the policy that was attached to the users
policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"

# Delete 30 IAM users
for i in range(1, 31):
    username = f'user{i}'

    # Detach the policy from the user
    iam.detach_user_policy(
        UserName=username,
        PolicyArn=policy_arn
    )

    # Delete the login profile (this disables console access)
    iam.delete_login_profile(UserName=username)

    # Delete the user
    iam.delete_user(UserName=username)

    print(f"Deleted user: {username}")