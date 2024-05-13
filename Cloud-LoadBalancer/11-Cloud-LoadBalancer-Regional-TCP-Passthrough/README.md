# Google Cloud - Regional Network Load Balancer TCP Pass-through

## Step-01: Introduction
1. Create Regional Application Load Balancer - TCP Pass-through
2. Access Application and verify
3. Delete all the resources created as part of this demo

## Step-02: Create Firewwall Rules
```t
# Firewall Rule-1: Create Firewall Rule 
## 1. This is required for Demo-11: Cloud LoadBalancer Regional TCP Passthrough
gcloud compute firewall-rules create vpc3-custom-allow-nlb-passthrough \
  --network=vpc3-custom \
  --target-tags=lb-tag \
  --allow=tcp:80 \
  --source-ranges=0.0.0.0/0
```

## Step-03: Create Regional Load Balancer - TCP Pass-through
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Network Load Balancer (TCP/SSL):** START CONFIGURATION
- **Internet facing or internal only:** From Internet to my VMs
- **Multiple regions or single region:** Single Region Only
- **Load Balancer type:** Pass-through
- **Backend type:** Backend Service
- Click on **CONTINUE**
- **Load Balancer name:** regional-lb-external-tcp-passthrough
- **Region:** us-central1
### Backend Configuration
- CLick on **CREATE A BACKEND SERVICE**
- **Name:** regional-lb-external-tcp-proxy
- **Description:** regional-lb-external-tcp-proxy
- **Backend type:** Instance Group
- **Protocol:** TCP
- **BACKENDS**
  - **IP stack type:** IPv4 (single stack)
  - **Instance Group:** zmig1-us-1
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**
  - **IP stack type:** IPv4 (single stack)
  - **Instance Group:** zmig1-us-2
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**  
- **Health Check:** regional-tcp-health-check  (**CREATE REGIONAL TCP HEALTH CHECK)
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-tcp
- **Description:** frontend-tcp
- **Protocol:** TCP
- **Network Service Tier:** Premium (Current project-level tier, change)
- **IP Version:** IPv4
- **IP Address:** regional-lb-ip1 **CREATE NEW EXTERNAL STATCI IP**
- **Port:** Single
- **Port number:** 80
### Review and Finalize
- Review all settings
- Click on **CREATE**


## Step-04: Verify Load Balancer
- Go to Network Services -> Load Balancing -> regional-lb-external-tcp-proxy
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

## Step-05: Access Application using LB IP on browser
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Access Application
http://LB-IP

# Send traffic to the load balancer
while true; do curl -m1 35.239.219.141; done
```

## Step-06: Delete Load Balancer
- Delete the  Load balancer created as part of this demo. 
- Delete Zonal Managed Instance Groups

## Step-07: (OPTIONAL) Create Load Balancer using gcloud
```t
# Reserve IP Address
gcloud compute addresses create network-lb-ipv4 \
    --region us-central1

# Create a backend service
gcloud compute backend-services create network-lb-backend-service \
    --protocol TCP \
    --health-checks tcp-health-check \
    --health-checks-region us-central1 \
    --region us-central1

# Add the instance groups to the backend service.
gcloud compute backend-services add-backend network-lb-backend-service \
--instance-group zmig-us-1 \
--instance-group-zone us-central1-a \
--region us-central1

gcloud compute backend-services add-backend network-lb-backend-service \
--instance-group zmig-us-2 \
--instance-group-zone us-central1-c \
--region us-central1

# Create the forwarding rules 
gcloud compute forwarding-rules create network-lb-forwarding-rule-ipv4 \
  --load-balancing-scheme EXTERNAL \
  --region us-central1 \
  --ports 80 \
  --address network-lb-ipv4 \
  --backend-service network-lb-backend-service

# Look up the load balancer's external IP address
gcloud compute forwarding-rules describe network-lb-forwarding-rule-ipv4 \
    --region us-central1

# Access Application
http://LB-IP

# Send traffic to the load balancer
while true; do curl -m1 35.239.219.141; done
```
