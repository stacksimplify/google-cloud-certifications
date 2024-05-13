# Google Cloud - Regional Application Load Balancer Internal HTTP 

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- Create Regional Application Load Balancer Internal - HTTP


## Step-02: **Pre-requisite-2:** Reserve proxy-only subnet exclusively for regional load balancing proxies.
- Goto VPC Networks -> vpc3-custom -> SUBNETS -> **ADD SUBNET**
- **Name:** lb-subnet-proxyonly-us-central1
- **Description:** lb-subnet-proxyonly-us-central1
- **Region:** us-central1
- **Purpose:** Regional Managed Proxy
- **Role:** Active
- **IPv4 Range:** 10.129.0.0/23
- Click on **ADD**

## Step-03: **Pre-requisite-3:** Create Firewall rule 
- **fw-allow-proxy-only-subnet:** An ingress rule that allows connections from the proxy-only subnet to reach the backends.
```t
# Firewall Rule: Allow connections from Proxy Only Subnets for All Instances in the network
gcloud compute firewall-rules create vpc3-custom-allow-proxy-only-subnet \
    --network=vpc3-custom \
    --action=allow \
    --direction=ingress \
    --source-ranges=10.129.0.0/23 \
    --rules=tcp:80,tcp:443,tcp:8080
```

## Step-04: **Pre-requisite-4:** Create Regional Health Check - HTTP
```t
# Create Regional Health Check
gcloud compute health-checks create http regional-http-health-check --port=80 --region=us-central1 
```

## Step-05: Create Regional Application Load Balancer - HTTP
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Select Application Load Balancer (HTTP/S):** START CONFIGURATION
- **Internet facing or internal only:** Only between my VMs or serverless services
- **Global or Regional:** Regional Internal Application Load Balancer
- **Load Balancer name:** regional-lb-internal-http
- **Region:** us-central1
- **Network:** vpc3-custom
### Backend Configuration
- CLick on **CREATE A BACKEND SERVICE**
- **Name:** regional-mybackend-svc1
- **Description:** regional-mybackend-svc1
- **Backend type:** Instance Group
- **Protocol:** HTTP
- **Named Port:** webserver80 (AUTO-POPULATED WHEN BACKEND IS SELECTED AS mig1-lbdemo)
- **Timeout:** 30
- **BACKENDS**
  - **Instance Group:** zmig-us-1
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**
  - **Instance Group:** zmig-us-2
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**  
- **Health Check:** regional-http-health-check
- **Security:**
  - **Cloud Armor backend security policy:** NONE
- Click on **CREATE**  
### Routing Rules
- **Mode:** Simple host and path rule
- REST ALL LEAVE TO DEFAULTS
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-http
- **Description:** frontend-http
- **Protocol:** HTTP
- **Subnetwork:** mysubnet1
- **Port:** 80
- **IP Address:** regional-internal-lb-ip1 **CREATE NEW INTERNAL STATCI IP**
- **Global access:** Enable
- Click on **DONE**
### Review and Finalize
- Review all settings
- Click on **CREATE**

## Step-06: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-http
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

## Step-07: Test from same region: us-central1
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Connect to any VM created as part of MIG
gcloud compute ssh --zone "us-central1-c" "zmig-us-2-9jm9" --project "gcplearn9"

# Access Application
curl http://INTERNAL-LB-IP
curl http://10.135.0.8
```

## Step-08: Test from different region: us-east1 (Global Access Enabled)
- As Global Access is enabled, verify if this internal load balancer is accessible via other regions
```t
# Create Client VM in region us-east1
gcloud compute instances create us-east1-clientvm \
    --zone=us-east1-c \
    --subnet=us-east1-subnet

# Connect to VM using gcloud
gcloud compute ssh --zone "us-east1-c" "us-east1-clientvm" 

# Access Application
curl http://INTERNAL-LB-IP
curl http://10.135.0.8
```

## Step-09: Delete Load Balancer
- Delete the  Load balancer created as part of this demo.
- Delete Test VM
```t
# Delete Test VM
gcloud compute instances delete us-east1-clientvm --zone=us-east1-c 
```