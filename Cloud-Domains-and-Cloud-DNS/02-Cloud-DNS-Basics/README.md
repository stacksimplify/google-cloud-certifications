# Cloud DNS -  Basics

## Step-01: Introduction
1. Register a Domain using Cloud Domains
2. Create a Cloud DNS Zone
3. Reserve the External IP Address
4. Create VM Instance with sample app, reserved external IP
5. Create DNS Record Set
6. Access Sample Application using browser with DNS Name
7. Delete all the resources created as part of this demo

## Step-02: Review/Create Cloud DNS Zone 
- Goto Network Services -> Cloud DNS -> CREATE ZONE
- **Zone type:** Public
- **Zone name:** kalyanreddydaida-com
- **DNS Name:** kalyanreddydaida.com
- REST ALL LEAVE TO DEFAULTS
- Click on **CREATE**

## Step-03: Reserve the External Static IP Address 
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Reserve the External Static IP Address 
gcloud compute addresses create ext-static-ip-for-dns-demo --region=us-central1
```

## Step-04: Cerate VM Instance with reserved External IP
```t
# Create VM with External [or] Create using Webconsole
gcloud compute instances create cloud-dns-demovm \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,address=EXTERNAL_IP \
    --metadata-from-file=startup-script=nginx-webserver.sh

# Replaced EXTERNAL_IP 
gcloud compute instances create cloud-dns-demovm \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,address=34.41.67.198 \
    --metadata-from-file=startup-script=nginx-webserver.sh

# List Compute Instances
gcloud compute instances list   

# Review External IP of VM
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

# Verify Application Deployed 
1. Verify VM Instance External IP Address
2. Access Application via browser and verify
http://<EXTERNAL-IP>
Observation:
1. Application should be accessible
```


## Step-05: Create DNS Record set
- Goto Network Services -> Cloud DNS -> ZONES -> kalyanreddydaida-com -> RECORD SETS -> ADD STANDARD
- DNS Name: mydnsdemo.kalyanreddydaida.com
- IPv4 Address: EXTERNAL-IP

## Step-06: Access Sample application using DNS Name in browser
```t
# Verify your setup
dig mydnsdemo.kalyanreddydaida.com
dig +trace mydnsdemo.kalyanreddydaida.com

# nslookup test
nslookup mydnsdemo.kalyanreddydaida.com

# Access Application
http://mydnsdemo.kalyanreddydaida.com
```

## Step-07: Delete VM Instance, Firewall Rule and Release Static IP
- Delete VM Instance created as part of this demo
- Delete Firewall rule created as part of this demo
- Release External Static IP Address
```t
# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete cloud-dns-demovm --zone=us-central1-a --delete-disks=all

# List and Delete Firewall rule which we created
gcloud compute firewall-rules list --network=default
gcloud compute firewall-rules delete fw-ingress-80-allinstances --network=default

# List and Delete/Release IP Addresss (External)
Go to VPC Network -> IP Addresses -> Select IP -> RELEASE STATIC ADDRESS -> RELEASE
```
