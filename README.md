# VAPT-AWS-Project

Finding Known Vulnerabilities using various scanning tools.  
We use AWS EC2 instance as a Platform and Lambda Functions to execute the programs. 
By using Docker image we build an image for each process using dockerfile. 
We create necessary roles and policies using IAM service. 
We use S3 service for storing each output from function. 
Most important Using Step Function we perform all the process in sequencial manner.
At the end , user gets a list of CVE IDs and Patch version of vulnerable domain.

# Installation of Tools 

subfinder :- go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@lastest


httpx :- go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest


nuclei :- go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

# AWS Services
EC2
Lambda
S3
IAM
Step Functions
