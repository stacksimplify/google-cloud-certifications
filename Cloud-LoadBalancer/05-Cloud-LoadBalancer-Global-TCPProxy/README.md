# Google Cloud - Global External Network Load Balancer TCP Proxy

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- Create Global External Load NetworkBalancer - TCP Proxy

## Step-02: Create Health check - TCP
```t
# Create a health check -  TCP
gcloud compute health-checks create tcp global-tcp-health-check --port 80
```

## Step-03: Create Global External Network Load Balancer
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Network Load Balancer (TCP/SSL):** START CONFIGURATION
- **Internet facing or internal only:** From Internet to my VMs
- **Multiple regions or single region:** Multiple regions (or not sure yet)
- **Classic or advanced traffic management:** Advanced traffic management 
- **Load Balancer name:** global-lb-external-tcp
### Backend Configuration
- CLick on **CREATE A BACKEND SERVICE**
- **Name:** global-lb-external-tcp
- **Description:** global-lb-external-tcp
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
  - **Instance Group:** mig1-us-east1
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**  
- **Health Check:** global-tcp-health-check
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-tcp
- **Description:** frontend-tcp
- **Protocol:** TCP
- **Network Service Tier:** Premium (Current project-level tier, change)
- **IP Version:** IPv4
- **IP Address:** global-lb-ip5 **CREATE NEW EXTERNAL STATCI IP**
- **Port:** 80
- **Proxy protocol:** OFF
### Review and Finalize
- Review all settings
- Click on **CREATE**

## Step-03: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-tcp
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

## Step-04: Access Application using LB IP on browser
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Access Application 
http://LB-IP
Observation: Application should be accessible
```

## Step-05: Test multi-region functionality (Send traffic to region closest to client)
- To simulate a user in a different geography, you can connect to one of your virtual machine instances in a different region, and then run a curl command from that instance to see the request go to an instance in the region closest to it.
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Region: us-central1
gcloud compute ssh --zone "us-central1-c" "mig1-us-central1-xq12" 
curl http://LB-IP
curl http://34.49.252.214

# Region: us-east1
gcloud compute ssh --zone "us-east1-d" "mig2-us-east1-693l" 
curl http://LB-IP
curl http://34.49.252.214
```

## Step-06: Delete Load Balancer
- Delete the  Load balancer created as part of this demo.
