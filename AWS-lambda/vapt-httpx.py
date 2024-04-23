import json
import boto3
import time


def lambda_handler(event, context):

    # boto3 client
    client = boto3.client("ec2")
    ssm = boto3.client("ssm")
    s3 = boto3.client("s3")
    
    bucket = "vapt-s3"

    # getting instance information
    describeInstance = client.describe_instances()

    InstanceId = []
    # fetchin instance id of the running instances
    for i in describeInstance["Reservations"]:
        for instance in i["Instances"]:
            if instance["State"]["Name"] == "running":
                InstanceId.append(instance["InstanceId"])

    # looping through instance ids
    for instanceid in InstanceId:
        # command to be executed on instance
        response = ssm.send_command(
            InstanceIds=[instanceid],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": ["cat /home/ubuntu/project/subs.txt | httpx -silent | aws s3 cp - s3://vapt-s3/web.txt ; aws s3 cp s3://vapt-s3/web.txt /home/ubuntu/project/web.txt ; cat /home/ubuntu/project/web.txt "]
            },
        )

        # fetching command id for the output
        command_id = response["Command"]["CommandId"]

        time.sleep(30)

        # fetching command output
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instanceid)
        print(output)
        
    filename = 'testweb' + '.txt'
    uploadByteStream = bytes(json.dumps(output['StandardOutputContent']).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=filename, Body=uploadByteStream)

    return {"statusCode": 200, "body": json.dumps(output["StandardOutputContent"]), "scantype": event["scantype"]}
