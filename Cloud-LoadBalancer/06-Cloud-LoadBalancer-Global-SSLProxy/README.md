# Google Cloud - Global External Network Load Balancer SSL Proxy

## Step-01: Introduction
- **Pre-requisite-1:** Create Instance Templates, Create Managed Instance Groups as part of Section `Cloud-LoadBalancer/01-Managed-Instance-Groups`
- Create Global External Network Load Balancer - SSL Proxy

## Step-02: Create Health check - TCP
```t
# Create a health check -  TCP
gcloud compute health-checks create tcp tcp-health-check --port 80
```

## Step-03: Create Global External Network Load Balancer
- Go to Network Services -> Load Balancing -> CREATE LOAD BALANCER
- **Network Load Balancer (TCP/SSL):** START CONFIGURATION
- **Internet facing or internal only:** From Internet to my VMs
- **Multiple regions or single region:** Multiple regions (or not sure yet)
- **Classic or advanced traffic management:** Advanced traffic management 
- **Load Balancer name:** global-lb-external-ssl
### Backend Configuration
- CLick on **CREATE A BACKEND SERVICE**
- **Name:** global-lb-external-tcp
- **Description:** global-lb-external-ssl
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
- **Health Check:** tcp-health-check
### Frontend Configuration
- Click on **ADD FRONTEND IP AND PORT**
- **Name:** frontend-ssl
- **Description:** frontend-ssl
- **Protocol:** SSL
- **Network Service Tier:** Premium (Current project-level tier, change)
- **IP Version:** IPv4
- **IP Address:** global-lb-ip3 **CREATE NEW EXTERNAL STATCI IP**
- **Port:** 80
- **Proxy protocol:** OFF
- **Certificate:** app1-google-managed (**CREATE NEW GOOGLE MANAGED SSL CERTIFICATE**)
### Review and Finalize
- Review all settings
- Click on **CREATE**

## Step-03: Verify Load Balancer
- Go to Network Services -> Load Balancing -> global-lb-external-tcp
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
# Access Application - HTTPS
https://myapp1.kalyanreddydaida.com
```

## Step-08: Test multi-region functionality (Send traffic to region closest to client)
- To simulate a user in a different geography, you can connect to one of your virtual machine instances in a different region, and then run a curl command from that instance to see the request go to an instance in the region closest to it.
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Region: us-central1
gcloud compute ssh --zone "us-central1-c" "mig1-us-central1-xq12" 
curl https://myapp1.kalyanreddydaida.com


# Region: us-east1
gcloud compute ssh --zone "us-east1-d" "mig2-us-east1-693l" 
curl https://myapp1.kalyanreddydaida.com

```


## Step-09: Delete Load Balancer
- Delete the  Load balancer created as part of this demo.

## Additional References
- https://cloud.google.com/load-balancing/docs/tcp/set-up-global-ext-proxy-tcp