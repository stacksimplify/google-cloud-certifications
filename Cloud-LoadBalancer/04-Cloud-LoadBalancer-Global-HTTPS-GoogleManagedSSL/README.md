# Google Cloud - Global Application Load Balancer HTTPS

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- Create Global Application Load Balancer - HTTPS with Google Managed SSL Certificates

## Step-02: Create Global HTTPS Load Balancer
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Select Application Load Balancer (HTTP/S):** START CONFIGURATION
- **Internet facing or internal only:** 
From Internet to my VMs or serverless services
- **Global or Regional:**
Global external Application Load Balancer
- **Load Balancer name:** global-lb-external-https-google-managedssl
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-https-google-managedssl
- **Description:** frontend-https-google-managedssl
- **Protocol:** HTTPS
- **IP Version:** IPv4
- **IP Address:** global-lb-ip3 **CREATE NEW EXTERNAL STATCI IP**
- **Port:** 443
#### CREATE GOOGLE MANAGED SSL CERTIFICATE
- Click on CREATE A NEW CERTIFICATE
- **NAME:** app1-google-managed
- **Description:** app1-google-managed
- **DOMAINS:** myapp1.kalyanreddydaida.com, myapp1.stacksimplify.com
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


## Step-03: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-https-google-managedssl
- Review the Tabs
  - LOAD BALANCERS 
  - BACKENDS
  - FRONTENDS

# Step-04: Verify SSL Certificate in Certificate Manager
- Goto Security -> Certificate Manager -> Data Protection 
- Click on **CLASSIC CERTIFICATES**  -> app1-google-managed

## Step-05: Add DNS Recordset in your desired Domain Provider
- Create LB IP as A record in your DNS Provider
- In my case, I have a registered domains in Google and AWS
- So we will use **Google Cloud DNS** and **AWS Route53**
- We will create a **RECORD SET** in Google Cloud DNS and AWS Route53
- **Important Note-1:** WAIT FOR 1 to 2 hours for Google Managed SSL certificates to be provisioned and ACTIVE
- **Important Note-2:** Just to prove that not only Google Cloud DNS, it works on any DNS provider (if we just add our LB IP as A record to verify our domain before creating valid SSL certificate for that domain by Google managed SSL servide)
- **Additional Reference:** https://cloud.google.com/certificate-manager/docs/deploy

## Step-06: Popular Domain Registrars
- Namecheap
- GoDaddy
- BlueHost
- AWS Route53
- Google Cloud Domains

## Step-07: Access Application using LB IP on browser
- **Important Note:** WAIT FOR 3 to 5 Minutes before Load Balancer is fully operational
```t
# Access Application - HTTP
http://myapp1.kalyanreddydaida.com
http://myapp1.stacksimplify.com
Observation: Should redirect to HTTPS URL

# Access Application - HTTPS
https://myapp1.kalyanreddydaida.com
https://myapp1.stacksimplify.com
```


## Step-08: Delete Load Balancer
- Delete the  Load balancer created as part of this demo.
