import time
import json
import boto3


def lambda_handler(event, context):

    # boto3 client
    client = boto3.client("ec2")
    ssm = boto3.client("ssm")
    s3 = boto3.client("s3")
    
    bucket = 'vapt-s3'

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
                "commands": ["sudo docker run vapt-subfinder subfinder -d " + event["domain"] + " -silent | aws s3 cp - s3://vapt-s3/subs.txt ; aws s3 cp s3://vapt-s3/subs.txt /home/ubuntu/project/subs.txt ; cat /home/ubuntu/project/subs.txt"]
            },
        )

        # fetching command id for the output
        command_id = response["Command"]["CommandId"]

        time.sleep(40)

        # fetching command output
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instanceid)
        print(output)

    filename = 'testsubs' + '.txt'
    uploadByteStream = bytes(json.dumps(output["StandardOutputContent"]).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=filename, Body=uploadByteStream)

    return {"statusCode": 200, "subs": json.dumps(output["StandardOutputContent"]), "scantype": event["scantype"], "networkscan": event["networkscan"]}
