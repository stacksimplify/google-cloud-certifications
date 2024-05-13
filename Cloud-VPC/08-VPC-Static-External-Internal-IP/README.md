# Google Cloud VPC - Internal and External Static IP Address

## Step-01: Introduction
- Create External Static IP
- Create Internal Static IP
- Create VM Instance with External and Internal Static IP
- Create firewall rule with port 80 allow from all instances
- Access Application and verify
- Delete VM Instance, Firewall rule and Exteenal and Internal IP Addresses

## Step-02: Create External and Internal Static IP Address
- Goto VPC Networks -> IP Addresses
### RESERVE EXTERNAL IP ADDRESS
- Name: myexternalip1
- Description: My External IP created for a VM
- REST ALL LEAVE TO DEFAULTS
- Click on **RESERVE**
```t
# Create External IP
gcloud compute addresses create myexternalip1 --region=us-central1
```
### RESERVE INTERNAL IP ADDRESS
- Name: myinternalip1
- Description: My Internal IP created for a VM
- IP Version: IPv4
- Network: vpc2-custom
- Subnetwork: mysubnet1
- Static IP Address: Assign Automatically
- Purpose: Non-shared
- Click on **RESERVE**
```t
# Create Internal IP
gcloud compute addresses create myinternalip1 --region=us-central1 --subnet=mysubnet1 
```
## Step-03: Create VM Instance with External and Internal Static IP
```t
# Create VM with External and Internal IP [or] Create using Webconsole
cd 08-VPC-Static-External-Internal-IP
gcloud compute instances create myvm7-static-ips \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,address=EXTERNAL_IP,private-network-ip=INTERNAL_IP \
    --metadata-from-file=startup-script=nginx-webserver.sh

# Replaced EXTERNAL_IP and INTERNAL_IP
cd 08-VPC-Static-External-Internal-IP
gcloud compute instances create myvm7-static-ips \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,address=34.41.67.198,private-network-ip=10.1.0.5 \
    --metadata-from-file=startup-script=nginx-webserver.sh

# List Compute Instances
gcloud compute instances list   

# Review External and Internal IP of VM
1. IPs should match whatever we reserved as Static IPs

# Create Firewall Rule
gcloud compute firewall-rules create fw-ingress-80-allinstances \
    --description="Allow inbound port 80 for all instances in a network" \
    --direction=INGRESS \
    --priority=1000 \
    --network=vpc2-custom \
    --action=ALLOW \
    --rules=tcp:80 \
    --source-ranges=0.0.0.0/0

# Verify Application Deployed in Custom VPC
1. Verify VM Instance Interal IP Address
2. Access Application via browser and verify
http://<EXTERNAL-IP>
Observation:
1. Application should be accessible
```


## Step-04: Delete VM Instance and Firewall Rule
- Delete VM Instance created as part of this demo
- Delete Firewall rule created as part of this demo
```t
# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm7-static-ips --zone=us-central1-a --delete-disks=all

# List and Delete Firewall rule which we created
gcloud compute firewall-rules list 
gcloud compute firewall-rules delete fw-ingress-80-allinstances

# List and Delete IP Addresss (External and Internal)
Go to VPC Network -> IP Addresses -> Select both IPS -> RELEASE STATIC ADDRESS -> RELEASE
```
