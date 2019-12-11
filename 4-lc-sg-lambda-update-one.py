from __future__ import print_function

import json
import datetime
import time
import boto3

print('Loading function')


def lambda_handler(event, context):
    AUTO_SCALLING_GROUP = 'Hayes-Test-ASG'
    LC = 'LC-micro'

    print("Received event: " + json.dumps(event, indent=2))

    # get autoscaling client
    client = boto3.client('autoscaling')

    # get object for the ASG we're going to update, filter by name of target ASG
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTO_SCALLING_GROUP])

    if not response['AutoScalingGroups']:
        return 'No such ASG'

    # update ASG to use new LC
    client.update_auto_scaling_group(AutoScalingGroupName=AUTO_SCALLING_GROUP, LaunchConfigurationName=LC)

    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[AUTO_SCALLING_GROUP])
    newLaunchConfigName = response.get('AutoScalingGroups')[0]['LaunchConfigurationName']

    return 'Updated ASG `%s` with new launch configuration `%s`' % (AUTO_SCALLING_GROUP, newLaunchConfigName)
