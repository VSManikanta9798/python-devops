import boto
import winstats
from boto.ec2 import cloudwatch
from boto.utils import get_instance_metadata


def collect_memory_usage():
    meminfo = winstats.get_mem_info()
    mem_percent = meminfo.MemoryLoad
    #print(mem_percent)
    return meminfo.MemoryLoad


def send_custom_metrics(instance_id, region, metrics, namespace, unit):
    cw = cloudwatch.connect_to_region(region)
    ec2 = boto.connect_ec2()

    instance = ec2.get_only_instances(instance_ids=[instance_id])[0]

    if "aws:autoscaling:groupName" in instance.tags:
        cw.put_metric_data(
            namespace,
            metrics.keys(),
            metrics.values(),
            unit=unit,
            dimensions={"AutoScalingGroupName": instance.tags["aws:autoscaling:groupName"]}
        )



if __name__ == "__main__":
    metadata = get_instance_metadata()
    instance_id = metadata["instance-id"]
    region = metadata["placement"]["availability-zone"][0:-1]

    mem_percent = collect_memory_usage()

    send_custom_metrics(
        instance_id,
        region,
        {"Autoscaling": mem_percent},
        namespace="EC2/Autoscaling-3",
        unit="Percent"
    )






















# import boto
# import psutil
# import re
# from boto.ec2 import cloudwatch
# from boto.utils import get_instance_metadata
#
#
# def collect_memory_usage():
#     """
#     Use /proc/meminfo and regular expression to grep system memory usage
#     """
#
#     meminfo = {}
#     pattern = re.compile("([\w\(\)]+):\s*(\d+)(:?\s*(\w+))?")
#     with open("/proc/meminfo") as f:
#         for line in f:
#             match = pattern.match(line)
#             if match:
#                 meminfo[match.group(1)] = float(match.group(2))
#     return meminfo
#
#
# def calculate_mem_usage_percentage():
#     """
#     Calculate MemUsage and SwapUsage for CloudWatch
#     Return the two values as percentage
#     """
#
#     mem_usage = collect_memory_usage()
#
#     mem_free = mem_usage["MemFree"] + mem_usage["Buffers"] + mem_usage["Cached"]
#     mem_used = mem_usage["MemTotal"] - mem_free
#     mem_percent = mem_used / mem_usage["MemTotal"] * 100
#
#     if mem_usage["SwapTotal"] != 0:
#         swap_used = mem_usage["SwapTotal"] - mem_usage["SwapFree"] - mem_usage["SwapCached"]
#         swap_percent = swap_used / mem_usage["SwapTotal"] * 100
#     else:
#         swap_percent = 0
#
#     return mem_percent, swap_percent
#
#
# def send_custom_metrics(instance_id, region, metrics, namespace, unit):
#     """
#     Send custom metrics to CloudWatch.
#
#     Input:
#     - instance_id is the unique ID of an EC2 instance
#     - region is a valid AWS region string, e.g. us-east-1
#     - metrics is expected to be a map of key (name) -> value pairs of metrics
#     - namespace is a custom metric name, usually of the type Service/Attribute, e.g. EC2/Memory
#     - unit is one of the acceptable units, see
#     https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDatum.html
#     """
#
#     cw = cloudwatch.connect_to_region(region)
#     ec2 = boto.connect_ec2()
#
#     cw.put_metric_data(
#         namespace,
#         metrics.keys(),
#         metrics.values(),
#         unit=unit,
#         dimensions={"InstanceId": instance_id}
#     )
#
#     # If the instance is also part of an Auto Scaling Group,
#     # we also send the custom metric to the ASG
#     instance = ec2.get_only_instances(instance_ids=[instance_id])[0]
#
#     if "aws:autoscaling:groupName" in instance.tags:
#         cw.put_metric_data(
#             namespace,
#             metrics.keys(),
#             metrics.values(),
#             unit=unit,
#             dimensions={"AutoScalingGroupName": instance.tags["aws:autoscaling:groupName"]}
#         )
#
#
# def should_autoscale(mem_percent, cpu_percent):
#     """
#     Given Memory and CPU Usage, return 2 if we should scale out (instances += 1),
#     0 if we should scale in (instances -= 1), or 1 if we should do nothing.
#     """
#
#     if cpu_percent >= HIGH_CPU_THRESHOLD or mem_percent >= HIGH_MEMORY_THRESHOLD:
#         return 2
#     elif cpu_percent < LOW_CPU_THRESHOLD and mem_percent < LOW_MEMORY_THRESHOLD:
#         return 0
#     return 1
#
#
# if __name__ == "__main__":
#     metadata = get_instance_metadata()
#     instance_id = metadata["instance-id"]
#     region = metadata["placement"]["availability-zone"][0:-1]
#
#     # Get the attributes (all in percentage) we want to push to CloudWatch
#     mem_percent, swap_percent = calculate_mem_usage_percentage()
#     memory_metrics = {
#         "MemUsage": mem_percent,
#         "SwapUsage": swap_percent
#     }
#     cpu_percent = psutil.cpu_percent(interval=.5)
#
#     # Compute the custom autoscaling value and publish it to CloudWatch
#     autoscaling_value = should_autoscale(mem_percent, cpu_percent)
#     send_custom_metrics(
#         instance_id,
#         region,
#         {"Autoscaling": autoscaling_value},
#         namespace="EC2/Autoscaling",
#         unit="Count"
#     )