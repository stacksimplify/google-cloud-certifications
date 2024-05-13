---
title: Google Cloud Unmanaged Instance Groups
description: Learn to Create Unmanaged Instance Groups on Google Cloud Platform GCP
---
      
## Step-01: Introduction
1. Create VM Instances (VM1: e2-micro and VM2: e2-small)
2. Create **Unmanaged Instance Group**
3. Create Health Check
4. Create Firewall rule for Health Check
5. Create Load Balancer and Verify the traffic from LB IP to VM Instances
6. Clean-Up all the resources created as part of this demo

## Step-02: Create VMs
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance - vm1
gcloud compute instances create vm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 

# Create VM Instance - vm2
gcloud compute instances create vm2 \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 
```

## Step-03: Create Unmanaged Instance Group
- **Name:** umig-1
- **Description:** unmanaged-instance-group-1
- **Location:** us-central1(IOWA)
- **Zone:** us-central1-a
- **Network:** default (leave to defaults)
- **Subnetwork:** default (leave to defaults)
- **VM Instances:** vm1, vm2
- **Specify Port Name Mapping:** 
   - **Port Name:** webserver-port
   - **Port Numbers:** 80
- Click on **CREATE**
```t
# Create Unmanaged Instance Group
gcloud compute instance-groups unmanaged create umig-1 \
   --project=gcplearn9 \
   --description=unmanaged-instance-group-1 \
   --zone=us-central1-a

# Set Named ports in Unmanaged Instance Group
gcloud compute instance-groups unmanaged set-named-ports umig-1 \
   --project=gcplearn9 \
   --zone=us-central1-a \
   --named-ports=webserver-port:80

# Add VM Instances to Unmanaged Instance Group
gcloud compute instance-groups unmanaged add-instances umig-1 \
   --project=gcplearn9 
   --zone=us-central1-a \
   --instances=vm1,vm2
```

## Step-04: Review Unmanaged Instance Group Properties
- Go to Compute Engine -> Instance Groups -> Click on **umig-1**
- Review the following Tabs
   - Overview
   - Details
   - Monitoring
   - Errors (Not applicable for Unmanaged Instance Groups)

## Step-05: Create Health Check 
- **What is Health Check?**
1. A health check determines whether a VM instance is healthy by sending requests to the instance. 
2. An instance is considered healthy if it returns consecutive responses within a specified time. 
3. Health checks are used for load balancing and autoscaling managed instance groups
- Go to Compute Engine -> Instance Groups -> Health Checks -> **CREATE HEALTH CHECK**
- **Name:** app1-health-check
- **Description:** 
- **Scope:** Regional 
- **Region:** us-central-1 (IOWA)
- **Protocol:** HTTP
- **Port:** 80
- **Proxy Protocol:** None
- **Request Path:** /index.html
- **Response:** Welcome
- **Host HTTP Header:** leave empty (leave to defaults)
- **Logs:** Off (leave to defaults) If enabled Cloud Logging cost is going to be high
- **Health Criteria:** Leave to defaults
```t
# Create Health Check
gcloud compute health-checks create http app1-health-check \
   --project=gcplearn9 \
   --port=80 \
   --request-path=/index.html \
   --proxy-header=NONE \
   --response=Welcome \
   --region=us-central1 \
   --no-enable-logging \
   --check-interval=10 \
   --timeout=5 \
   --unhealthy-threshold=3 \
   --healthy-threshold=2
```
- Click on **CREATE**

## Step-06: Create a firewall rule to allow health check probes to connect to your app 
- Health check probes come from addresses in the ranges 130.211.0.0/22 and 35.191.0.0/16, so make sure your firewall rules allow the health check to connect. 
```t
# Create Firewall rule
gcloud compute firewall-rules create allow-health-check \
    --allow tcp:80 \
    --source-ranges 130.211.0.0/22,35.191.0.0/16 \
    --network default
```
## Step-07: Create a Load Balancer
- Go to Network Services -> Load Balancing -> Create Load Balancer -> HTTP(S) Load Balancing -> START CONFIGURATION
- **Internet facing or internal only:** From internet to my VMs
- Click on **Continue**
- **Name:** lb-for-umig1
- **WARNING:** Click on **RESERVE SUBNET**
   - **NAME:** proxy-only-subnet
   - **IP Address:** 10.0.0.0/24
   - Click on **CREATE**
```t
Proxy-only subnet required
The proxy servers implementing your Envoy-based load balancer need IP addresses, which will be allocated automatically from a subnet that you reserve for this purpose (and this purpose only) in region "us-central1". Each proxy will use its assigned IP address when connecting to the servers implementing your backend services
```
### Frontend Configuration
- **New Frontend IP and port**
- **Name:** fip-lb-umig
- **Protocol:** HTTP
- **Network Service Tier:** Premium
- **IP Version:** IPV4
- **IP Address:** Click on **CREATE IP ADDRESS** 
   - **NAME:** sip-lb-umig
   - **DESCRIPTION:** sip-lb-umig
- **Port:** 80
- Click on **DONE** 
### CREATE A BACKEND SERVICE
- Click on **CREATE A BACKEND SERVICE**
   - **Name:** lb-backend-umig
   - **Description:** lb-backend-umig
   - **Backend Type:** Instance Group
   - **Protocol:** HTTP
   - **Naed Port:** http
   - **Timeout:** 30
   - **New backend:** umig-1
   - **Port Numbers:** 80 (select webserver-port named port from that instance group)
   - **Balancing mode:** Utilization 
   - **Maximum backend utilization:** 80
   - **Maximum RPS:** leave empty (leave to defaults)
   - **Scope:** per instance (leave to defaults)
   - **Capacity:** 100
   - Click on **DONE**
   - Click on **CREATE**
- **Cloud CDN:** leave it unchecked (leave to defaults)   
- **Health check:** app1-health-check 
- **Logging:** leave unchecked (leave to defaults)
- **Security:** leave unselected (leave to defaults)   
- Click on **CREATE**
### Host and Path Rules
- **Mode:** Simple host and path rule

### Review and Finalize
1. Front End
2. Backend
- Click on **CREATE**
- It will take 3 to 5 minutes to create the load balancer. 

## Step-08: Verify Load Balancer Properties after creation
- Go to Network Services -> Load Balancing -> lb-for-umig
- Verify if Instances are Healthy

## Step-09: Access Sample Application using LB IP 
```t
# Access Sample App
http:/;<LB-IP-ADDRESS>
http://35.209.128.93
Observation: 
1. Keep refreshing to see the output from both Virtual Machines
2. You will see output from both VMs switching

# Curl with while loop runs every 1 second
while true; do curl http://35.209.128.93/; sleep 1; done
```

## Step-10: Clean-Up - Delete Load Balancer
- Go to Network Services -> Load Balancing -> lb-for-unmanaged-instance-group
- Click on **DELETE**
- Select **Backend services:lb-backend-umig** for deletion
- Leave **Health Checks: app1-health-check** unchecked to not to delete
- Click on **DELETE LOAD BALANCER AND SELECTED RESOURCES**

## Step-11: Clean-Up Delete Unmanaged Instance Group
- Go to Compute Engine -> Instance Groups -> Click **unmanaged-instance-group-1** 
- Click on **DELETE GROUP**
```t
# Delete Instance Group - Unmanaged
gcloud compute instance-groups unmanaged delete unmanaged-instance-group-1 \
   --project=gcplearn9 \
   --zone=us-central1-a
```

## Step-12: Clean-Up - Delete VM Instances
- Delete the VM instances
```t
# Delete VM 
gcloud compute instances delete vm1 --zone=us-central1-a
gcloud compute instances delete vm2 --zone=us-central1-a

# List VMs
gcloud compute instances list --filter='name:vm1'
gcloud compute instances list --filter='name:vm2'
```

## Step-13: Clean-Up - Release External IP Address used for LB
- Go to VPC Networks -> External IP Addresses
- Select **sip-lb-umig** and click on **RELEASE STATIC IP ADDRESS**
```t
# Delete External Static IP Address
gcloud compute addresses delete sip-lb-umig \
   --project=gcplearn9 \
   --region=us-central1
```


## References 
- [Instance Groups](https://cloud.google.com/compute/docs/instance-groups)