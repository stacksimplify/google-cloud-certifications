# Google Cloud - Regional Network Load Balancer TCP Proxy

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- Create Regional Application Load Balancer - TCP Proxy

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

## Step-04: **Pre-requisite-4:** Create Regional Health Check - TCP
```t
# Create Regional Health Check
gcloud compute health-checks create tcp regional-tcp-health-check --port=80 --region=us-central1 
```

## Step-05: Create Regional Load Balancer - TCP Proxy
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Network Load Balancer (TCP/SSL):** START CONFIGURATION
- **Internet facing or internal only:** From Internet to my VMs
- **Multiple regions or single region:** Single Region Only
- **Load Balancer type:** Proxy
- **Load Balancer name:** regional-lb-external-tcp-proxy
- **Region:** us-central1
- **Network:** vpc3-custom
### Backend Configuration
- CLick on **CREATE A BACKEND SERVICE**
- **Name:** regional-lb-external-tcp-proxy
- **Description:** regional-lb-external-tcp-proxy
- **Backend type:** Instance Group
- **Protocol:** TCP
- **Named Port:** webserver80 (AUTO-POPULATED WHEN BACKEND IS SELECTED AS mig1-lbdemo)
- **Timeout:** 30
- **IP address selection policy:** Only IPv4
- **BACKENDS**
  - **IP stack type:** IPv4 (single stack)
  - **Instance Group:** mig1-us-central1
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


## Step-06: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-http
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

## Step-07: Access Application using LB IP on browser
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Access Application
http://LB-IP
```

## Step-08: Delete Load Balancer
- Delete the  Load balancer created as part of this demo. 
