# Google Cloud - Global Application Load Balancer HTTP

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- Create Global Application Load Balancer - HTTP

## Step-02: Create Global HTTP Load Balancer
### Application Load Balancer (HTTP/S)
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Select Application Load Balancer (HTTP/S):** START CONFIGURATION
- **Internet facing or internal only:** 
From Internet to my VMs or serverless services
- **Global or Regional:** Global external Application Load Balancer
- Click on **CONTINUE**
- **Load Balancer name:** global-lb-external-http
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-http
- **Description:** frontend-http
- **Protocol:** HTTP
- **IP Version:** IPv4
- **IP Address:** global-lb-ip1 **CREATE NEW EXTERNAL STATCI IP**
- **Port:** 80
- Click on **DONE**
### Backend Configuration
- CLick on **CREATE A BACKEND SERVICE**
- **Name:** mybackend-svc1
- **Description:** mybackend-svc1
- **Backend type:** Instance Group
- **Protocol:** HTTP
- **Named Port:** webserver80 (AUTO-POPULATED WHEN BACKEND IS SELECTED AS mig1-lbdemo)
- **Timeout:** 30
- **BACKENDS**
  - **Instance Group:** mig1-us-central1
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**
  - **Instance Group:** mig1-us-east1
  - **Port Numbers:** 80
  - REST ALL LEAVE TO DEFAULTS
  - Click on **DONE**  
- Disable **Cloud CDN**
- **Health Check:** http-health-check
- **Security:**
  - **Cloud Armor backend security policy:** NONE
- Click on **CREATE**  
### Routing Rules
- **Mode:** Simple host and path rule
- REST ALL LEAVE TO DEFAULTS
### Review and Finalize
- Review all settings
- Click on **CREATE**

## Step-03: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-http
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

## Step-04: Access Application using LB IP on browser
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Access Application
http://LB-IP
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
curl http://34.49.252.214/

# Region: us-east1
gcloud compute ssh --zone "us-east1-d" "mig2-us-east1-693l" 
curl http://LB-IP
curl http://34.49.252.214/
```


## Step-06: Delete Load Balancer
- Delete the  Load balancer created as part of this demo.
