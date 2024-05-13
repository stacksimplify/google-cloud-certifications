# VPC Network Firewall Policies

## Step-01: Introduction
1. Create VM Instance in vpc1-auto VPC Network
2. Create VM Instance in vpc2-custom VPC Network
3. Create a Network Firewall policy (Allow Port 80) and associate it to both VPC networks
4. Access application hosted on both VMs
5. Delete VMs and Firewall Policy

## Step-02: Create VM Instances in vpc1-auto and vpc2-custom VPC Networks
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM with startup-script nginx-webserver.sh 
cd 05-VPC-Firewall-Rules-Ingress-Destination
gcloud compute instances create myvm6-vpc1-auto \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=vpc1-auto \
    --metadata-from-file=startup-script=nginx-webserver.sh

gcloud compute instances create myvm6-vpc2-custom \
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
telnet VM1_EXTERNAL_IP 80
telnet VM2_EXTERNAL_IP 80
curl VM1_EXTERNAL_IP
curl VM2_EXTERNAL_IP
4. Access Application via browser and verify
http://<VM1_EXTERNAL-IP>
http://<VM2_EXTERNAL-IP>
Observation:
1. Should fail as there is no firewall rule with port 80 in VPC Firewall Rules
```

## Step-03: Create Network Firewall Policy
- Goto Network Security -> Cloud NGFW -> Firewall Policies -> CREATE FIREWALL POLICY
### Configure policy
- **Policy name:** fw-policy-allow-80-in-vpc1-and-vpc2
- **Description:** Allow port 80 in vpc1-auto and vpc2-custom
- **Deployment scope:** Global
### Add rules
- Click on **ADD RULES**
- **Priority:** 100
- **Description:** Allow 80 rule for vpc1-auto and vpc2-custom
- **Direction of traffic:** Ingress
- **Target Type:** All instances in the network
- **Source:** 
  - **IP Type:** IPv4
  - **IP Ranges:** 0.0.0.0/0
- **Protocols and ports:** Specified protocols and ports
  - **TCP:** 80  
- Click on **CREATE**
### Associate policy with VPC networks (optional)
- Click on **ASSOCIATE**
- Select vpc1-auto and vpc2-custom
- Click **CREATE**
  
## Step-04: Verify application access after applying Firewall Policy  
```t
# List Compute Instances (Optional)
gcloud compute instances list   

# Verify Application Deployed in Custom VPC
1. Verify if Compute Instance deployed in vpc2-custom network, in mysubnet1
2. Verify VM Instance Interal IP Address
3. Perform curl and telnet tests
telnet VM1_EXTERNAL_IP 80
telnet VM2_EXTERNAL_IP 80
curl VM1_EXTERNAL_IP
curl VM2_EXTERNAL_IP
4. Access Application via browser and verify
http://<VM1_EXTERNAL-IP>
http://<VM2_EXTERNAL-IP>
Observation:
1. Should pass
```

## Step-05: Delete Firewall Policy and Delete VM
```t
# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm6-vpc1-auto --zone=us-central1-a 
gcloud compute instances delete myvm6-vpc2-custom --zone=us-central1-a 

# Delete firewall policy
Note: We cannot delete firewall policy when it is associated with VPC Networks
1. Remove Association to VPC networks
2. Delete Firewall Policy
```
