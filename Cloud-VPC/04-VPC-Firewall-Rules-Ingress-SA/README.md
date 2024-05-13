# Google Cloud VPC Firewall Rules - Target as Service Account

## Step-01: Introduction
- **Firewall Ingress Rule:** Ingress with Target as Service Account

## Step-02: Create VM Instance
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet1 with startup-script nginx-webserver.sh [or] Create using Webconsole
cd 04-VPC-Firewall-Rules-Ingress-SA
gcloud compute instances create myvm3-service-accounts \
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
- **Name:** fw-ingress-80-service-accounts
- **Description:** Allow inbound port 80 for all instances with specified service account
- **Network:** vpc2-custom
- **Priority:** 1000
- **Direction of traffic:** Ingress
- **Action on match:** Allow
- **Targets:** Specified Service Account
- **Service account scope:** In this project
- **Target service account:** Compute engine default service account
- **Source filter:** IPv4 ranges
- **Source IPv4 range:** 0.0.0.0/0
- **Second source filter:** None
- **Destination filter:** None
- **Protocols and ports:** Specified protocols and ports
- **TCP:** 80
- Click on **CREATE**
```t
# Using gcloud (Optional - for reference only)
gcloud compute --project=gcplearn9 firewall-rules create fw-ingress-80-service-accounts --description="Allow inbound port 80 for all instances with specified service account" --direction=INGRESS --priority=1000 --network=vpc2-custom --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-service-accounts=899156651629-compute@developer.gserviceaccount.com
```
## Step-04: Access Application deployed in VM
```t
# List Compute Instances
gcloud compute instances list   

# Verify Application Deployed in Custom VPC
1. Perform curl and telnet tests
telnet EXTERNAL_IP 80
curl EXTERNAL_IP
2. Access Application via browser and verify
http://<EXTERNAL-IP>
Observation:
1. Should pass, application should be accessible
```

## Step-05: Delete Firewall rule and Delete VM
```t
# Delete firewall rule
gcloud compute firewall-rules delete fw-ingress-80-service-accounts

# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm3-service-accounts --zone=us-central1-a --delete-disks=all 
```

