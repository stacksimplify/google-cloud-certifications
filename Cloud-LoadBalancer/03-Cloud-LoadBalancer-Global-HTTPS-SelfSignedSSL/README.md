# Google Cloud - Global Application Load Balancer HTTPS

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- **Pre-requisite-2:** Create Self-Signed SSL Certificates 
- Create Global Application Load Balancer - HTTPS with Self-Signed SSL Certificates

## Step-02: Pre-requisite-2: Create Self-Signed Certificates
```t
# Create and Change Directory
mkdir  SSL-SelfSigned-Certs
cd SSL-SelfSigned-Certs

# Create your app1 key:
openssl genrsa -out app1.key 2048

# Create your app1 certificate signing request:
openssl req -new -key app1.key -out app1.csr -subj "/CN=app1.stacksimplify.com"

# Create your app1 certificate:
openssl x509 -req -days 7300 -in app1.csr -signkey app1.key -out app1.crt
```

## Step-03: Create Global HTTPS Load Balancer
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Select Application Load Balancer (HTTP/S):** START CONFIGURATION
- **Internet facing or internal only:** 
From Internet to my VMs or serverless services
- **Global or Regional:**
Global external Application Load Balancer
- **Load Balancer name:** global-lb-external-https-selfsignedssl
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-https-selfsignedssl
- **Description:** frontend-https-selfsignedssl
- **Protocol:** HTTPS
- **IP Version:** IPv4
- **IP Address:** global-lb-ip2 **CREATE NEW EXTERNAL STATCI IP**
- **Port:** 443
#### UPLOAD SELF-SIGNED CERTIFICATE
- Click on CREATE A NEW CERTIFICATE
- **NAME:** app1-ssl-self-signed
- **Description:** app1-ssl-self-signed
- Click on **CREATE**
- **Enable HTTP to HTTPS Redirect:** enabled
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

## Step-04: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-https-selfsigned
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

# Step-05: Verify SSL Certificate in Certificate Manager
- Goto Security -> Certificate Manager -> Data Protection 
- Click on **CLASSIC CERTIFICATES** -> app1-ssl-self-signed

## Step-06: Access Application using LB IP on browser
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Access Application - HTTP
http://LB-IP
Observation: Should redirect to HTTPS URL

# Access Application - HTTPS
https://LB-IP
```

## Step-07: Delete Load Balancer
- Delete the  Load balancer created as part of this demo.
