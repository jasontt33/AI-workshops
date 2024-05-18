#!/bin/bash

## get all ec2 instances ids with the name tag that starts wtih aws-cloud9
INSTANCE_IDS=($(aws ec2 describe-instances --filters "Name=tag:Name,Values=aws-cloud9*" --query "Reservations[*].Instances[*].InstanceId" --output text --profile sandbox --region us-east-1))

# List of instance IDs
#INSTANCE_IDS=("i-0abcd1234efgh5678" "i-1abcd1234efgh5678" "i-2abcd1234efgh5678") # Add all your EC2 instance IDs here


printf "Instance IDs: %s\n" "${INSTANCE_IDS[@]}"

# for id in "${INSTANCE_IDS[@]}"; do
#     aws ec2 start-instances --instance-ids $id --region us-east-1 --profile sandbox
# done    

for id in "${INSTANCE_IDS[@]}"; do
    # Use AWS CLI to execute pip3 install command
    aws ssm send-command --instance-ids $id --document-name "AWS-RunShellScript" --parameters commands="pip3 install --upgrade pip setuptools wheel" --region us-east-1 --profile sandbox
done