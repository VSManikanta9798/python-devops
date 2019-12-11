import boto3

ACCESS_KEY = ''
SECRET_KEY = ''
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