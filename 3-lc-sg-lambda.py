from __future__ import print_function

import json
import datetime
import time
import boto3

AUTO_SCALLING_GROUP = 'Hayes-Test-ASG'
LC_1 = 'LC-micro'
LC_2 = 'LC-Large'

print('Loading function')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # get autoscaling client
    client = boto3.client('autoscaling')

    # get object for the ASG we're going to update, filter by name of target ASG
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[event[AUTO_SCALLING_GROUP]])

    if not response['AutoScalingGroups']:
        return 'No such ASG'


    # update ASG to use new LC
    if response.get('AutoScalingGroups')[0]['LaunchConfigurationName'] == LC_1:
        client.update_auto_scaling_group(AutoScalingGroupName=AUTO_SCALLING_GROUP, LaunchConfigurationName=LC_2)
    else:
        client.update_auto_scaling_group(AutoScalingGroupName=AUTO_SCALLING_GROUP, LaunchConfigurationName=LC_1)

    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTO_SCALLING_GROUP])
    newLaunchConfigName = response.get('AutoScalingGroups')[0]['LaunchConfigurationName']

    return 'Updated ASG `%s` with new launch configuration `%s`' % (event['targetASG'], newLaunchConfigName)
