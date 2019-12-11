import boto3

ACCESS_KEY = 'AKIAQED72P2QPAMQ4CFW'
SECRET_KEY = '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'
AUTO_SCALLING_GROUP = 'Hayes-Test-ASG'
LC = 'LC-Large'

client = boto3.client(
    'autoscaling',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTO_SCALLING_GROUP])

print(response.get('AutoScalingGroups')[0]['LaunchConfigurationName'])

client.update_auto_scaling_group(AutoScalingGroupName=AUTO_SCALLING_GROUP, LaunchConfigurationName=LC)


response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTO_SCALLING_GROUP])

print(response.get('AutoScalingGroups')[0]['LaunchConfigurationName'])