import json, os, subprocess

print("Outside function")

def lambda_handler(event, context):
    # TODO implement
    
    print("VAPT testing using AWS")
    
    # Testing individual keys from JSON
    for key in event:
        print(subprocess.getoutput(event[key]))
        
    # Writing to a file in /tmp
        f = open("../../tmp/vapt.txt", "w")
    f.write("something for CDAC project")
    f.close()
    
    # Reading what was written
    print(subprocess.getoutput("cat /tmp/vapt.txt"))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
