# Google Cloud VPC Firewall Rules - Egress Deny Rule

## Step-01: Introduction
- **Firewall Egress Rule:** Egress Deny Rule

## Step-02: Create VM Instance
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet1 with startup-script nginx-webserver.sh [or] Create using Webconsole
cd 06-VPC-Firewall-Rules-Egress
gcloud compute instances create myvm5-egress \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1 
Important Note: Upload nginx-webserver.sh to Google Cloud shell if running gcloud commands on cloud shell

# List Compute Instances (Optional)
gcloud compute instances list   

# Connect to myvm1-egress from Cloud Shell using gcloud
gcloud compute ssh --zone "us-central1-a" "myvm5-egress" --project "gcplearn9"

# Install dnsutils and telnet packages in VM
sudo apt install -y dnsutils
sudo apt install -y telnet
Note: We need to use nslookup command in this demo, so we need to install dnsutils package in the VM

# Run nslookup command
nslookup stacksimplify.com
Observation:
1. Make a note of IP addresses
2. We will use these IP addresses when we create a egress firewall in next step

# Run the following tests before applying egress firewall
telnet stacksimplify.com 80
telnet stacksimplify.com 443
ping stacksimplify.com
[or]
You can use individual IPs of website from nslookup output
Observation:
1. telnet tests to port 80 and 443 should be successful
2. ICMP test also should be successful
```

## Step-03: Create Ingress firewall rule
- Goto -> VPC Networks -> vpc2-custom -> FIREWALLS -> ADD FIREWALL RULE
- **Name:** fw-egress-deny-80-443-icmp
- **Description:** Deny outbound to destination "stacksimplify.com" on port 80, 443 and ICMP
- **Network:** vpc2-custom
- **Priority:** 1000
- **Direction of traffic:** Egress
- **Action on match:** Deny
- **Targets:** All Instances in the network
- **Destination filter:** IPv4 ranges
- **Destination IPv4 range:** 99.84.160.0/24 (output of command nslookup stacksimplify.com)
- **Source filter:** None
- **Protocols and ports:** Specified protocols and ports
- **TCP:** 80,443
- **Other:** icmp
- Click on **CREATE**
```t
# Using gcloud (Optional - for reference only)
gcloud compute --project=gcplearn9 firewall-rules create fw-egress-deny-80-443-icmp --description=Deny\ outbound\ to\ destination\ \"stacksimplify.com\"\ on\ port\ 80,\ 443\ and\ ICMP --direction=EGRESS --priority=1000 --network=vpc2-custom --action=DENY --rules=tcp:80,tcp:443,icmp --destination-ranges=99.84.160.0/24
```
## Step-04: Perform tests after Egress rule created
```t
# Run the following tests before applying egress firewall
telnet stacksimplify.com 80
telnet stacksimplify.com 443
ping stacksimplify.com
[or]
You can use individual IPs of website from nslookup output

Observation:
1. telnet tests to port 80 and 443 should fail as egress rule is denying
2. ICMP test also should fail as egress rule is denying
```

## Step-05: Delete Firewall rule and Delete VM
```t
# Delete firewall rule
gcloud compute firewall-rules delete fw-egress-deny-80-443-icmp

# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm5-egress --zone=us-central1-a 
```

