# Google Cloud VPC - Private Google Access 

## Step-01: Introduction
- Create Cloud Run service with Internal Endpoint 
- Create Subnet (mysubnet2pga) with Private Google Access enabled
- Create VM Instance in subnet (PGA: ON, mysubnet2pga) with External IP disabled 
- Create VM Instance in subnet (PGA: OFF, mysubnet1) with External IP disabled 
- Verify access to Cloud Run service from both VM Instances using curl
- **Expected Result:**
  - curl from VM Instance in subnet with **PGA:ON** should be **successful**
  - curl from VM Instance in subnet with **PGA:OFF** should **fail**
- **Clean-Up:** Delete all the resources created as part of this demo

## Step-02: Create Cloud Run Service with Internal Endpoint
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Set Cloud Run Region
gcloud config set run/region REGION
gcloud config set run/region us-central1
gcloud config list

# Deploy Cloud Run Service
gcloud run deploy myservice201 \
--image=stacksimplify/google-cloud-run:v1 \
--allow-unauthenticated --ingress=internal \
--port=80 \
--region=us-central1

# Access Service via browser or curl
https://myservice201-ntm7u2mecq-uc.a.run.app
Observation:
1. Should not be accessible
2. Cloud Run endpoint is a private endpoint, not publicly accessible
```

## Step-03: Create a Subnet with Private Google Access enabled 
- Gotp VPC Networks -> vpc2-custom -> SUBNETS -> ADD SUBNET
- **Name:** mysubnet2pga
- **Description:** Subnet with Private Google Access enabled
- **VPC Network:** vpc2-custom
- **Region:** us-central1
- **Purpose:** None
- **IP stack type:** IPv4(single-stack)
- **IP Subnet:** 10.231.0.0/20
- **Private Google Access:** ON
- REST ALL LEAVE TO DEFAULT
- Click on **ADD**

## Step-04: Create a VM Instance without External IP Address in mysubnet2pga
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet2pga without External IP Address
gcloud compute instances create myvm-pga-on \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet2pga,no-address

# Connect to VM using gcloud
gcloud compute ssh --zone "us-central1-a" "myvm-pga-on" --tunnel-through-iap 

# Curl to Cloud Run Service
curl https://myservice201-ntm7u2mecq-uc.a.run.app
Observation:
1. curl should be successful
2. Request goes via Google Private access
```

## Step-05: Create a VM Instance without External IP Address in mysubnet1 where Private Google Access not enabled
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet1 without External IP Address
gcloud compute instances create myvm-pga-off \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,no-address

# Connect to VM using gcloud
gcloud compute ssh --zone "us-central1-a" "myvm-pga-off" --tunnel-through-iap 

# Curl to Cloud Run Service
curl https://myservice201-ntm7u2mecq-uc.a.run.app
Observation:
1. curl should fail
2. Private google access not enabled in mysubnet1
```

## Step-06: Delete VM Instance and Cloud Run Service
```t
# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm-pga-on --zone=us-central1-a --delete-disks=all 
gcloud compute instances delete myvm-pga-off --zone=us-central1-a --delete-disks=all 

# List and Delete Cloud Run Service
gcloud run services list
gcloud run services delete myservice201
```