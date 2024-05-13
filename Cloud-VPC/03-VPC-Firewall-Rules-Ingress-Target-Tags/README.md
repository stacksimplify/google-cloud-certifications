# Google Cloud VPC Firewall Rules - Target as Target Tags

## Step-01: Introduction
- **Firewall Ingress Rule:** Ingress with Target as Specified Target Tags

## Step-02: Create VM Instance
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet1 with startup-script nginx-webserver.sh[or] Create using Webconsole
cd 03-VPC-Firewall-Rules-Ingress-Target-Tags
gcloud compute instances create myvm2-target-tags \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1 \
    --metadata-from-file=startup-script=nginx-webserver.sh
Important Note: Upload nginx-webserver.sh to Google Cloud shell if running gcloud commands on cloud shell

# List Compute Instances (Optional)
gcloud compute instances list   

# Verify Application Deployed in Custom VPC
1. Verify if Compute Instance deployed in vpc2-custom network, in mysubnet1
2. Verify VM Instance Interal IP Address
3. Perform curl and telnet tests
telnet EXTERNAL_IP 80
curl EXTERNAL_IP
4. Access Application via browser and verify
http://<EXTERNAL-IP>
Observation:
1. Should fail as there is no firewall rule with port 80 in VPC Firewall Rules
```

## Step-03: Create Ingress firewall rule
- Goto -> VPC Networks -> vpc2-custom -> FIREWALLS -> ADD FIREWALL RULE
- **Name:** fw-ingress-80-target-tags
- **Description:** Allow inbound port 80 for specified target tags
- **Network:** vpc2-custom
- **Priority:** 1000
- **Direction of traffic:** Ingress
- **Action on match:** Allow
- **Targets:** Specified target tags
- **Target tags:** mywebserver
- **Source filter:** IPv4 ranges
- **Source IPv4 range:** 0.0.0.0/0
- **Second source filter:** None
- **Destination filter:** None
- **Protocols and ports:** Specified protocols and ports
- **TCP:** 80
- Click on **CREATE**
```t
# Using gcloud (Optional - for reference only)
gcloud compute --project=gcplearn9 firewall-rules create fw-ingress-80-target-tags --description="Allow inbound port 80 for specified target tags" --direction=INGRESS --priority=1000 --network=vpc2-custom --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=mywebserver
```
## Step-04: Apply Tags to VM and Access Application
```t
# List Compute Instances
gcloud compute instances list   

# Update VM Instance to add the target-tag
gcloud compute instances add-tags INSTANCE_NAME --zone ZONE --tags TAGS
gcloud compute instances add-tags myvm2-target-tags --zone us-central1-a --tags mywebserver

# Verify if Target Tag associated with Compute Instance
gcloud compute instances describe myvm2-target-tags --zone=us-central1-a
[or]
Goto -> Compute Engine -> VM Instances -> myvm2-target-tags -> DETAILS Tab

# Verify Application Deployed in Custom VPC
1. Perform curl and telnet tests
telnet EXTERNAL_IP 80
curl EXTERNAL_IP
2. Access Application via browser and verify
http://<EXTERNAL-IP>
Observation:
1. Should pass, application should be accessible
```

## Step-05: Delete Firewall rule and verify
```t
# Delete firewall rule
gcloud compute firewall-rules delete fw-ingress-80-target-tags

# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm2-target-tags --zone=us-central1-a --delete-disks=all 
```
