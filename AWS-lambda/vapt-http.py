import json

def lambda_handler(event, context):
    # TODO implement
    subdomain = event["subdomain"]
    
    return {"subdomain": "http://" + subdomain, "scantype": event["scantype"]}
