# Cloud NAT Gateway - VPC Internal-Only IP Address

## Step-01: Introduction
1. Create VM Instance without External IP
2. Test `ping google.com` from vm instance and it should fail
3. Create Cloud NAT and Cloud Router
4. Test `ping google.com` from vm instance and it should be successful
5. Delete all resources created

## Step-02: Create a VM Instance with Internal-Only IP Address
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet1 without External IP Address
gcloud compute instances create myvm8-internal-only \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1,no-address
   
# Connect to VM using gcloud
gcloud compute ssh --zone "us-central1-a" "myvm8-internal-only" --tunnel-through-iap 

# Ping to any Internet URL
ping stacksimplify.com
ping google.com
Observation:
1. Should fail, because VM dont have internet access

# Try and Install any package
sudo apt install -y telnet
Observation:
1. Should fail, because VM dont have internet access to download and install package
```

## Step-03: Create Cloud Router
- Goto Network Connectivity -> Cloud Routers > CREATE ROUTER
- **Name:** mycloudrouter1
- **Description:** mycloudrouter1
- **Network:** vpc2-custom
- **Region:** us-central1
- **Routes:** Advertise all subnets visible to the Cloud Router (Default)
- Click on **CREATE**
```t
# Create Cloud Router (Optional - for reference only)
gcloud compute routers create mycloudrouter1 --description=mycloudrouter1 --region=us-central1 --network=vpc2-custom
```

## Step-04: Create Cloud NAT
- **Important Note:** Cloud NAT is region and VPC specific
- Goto Network Services -> Cloud NAT -> GET STARTED
- **Gateway name:** mycloudnat1
- **NAT Type:** Public
- **Select Cloud Router:** vpc2-custom
- **Region:** us-central1
- **Cloud Router:** mycloudrouter1
- **Cloud NAT mapping**
  - **Source endpoint type:** VM Instances
  - **Source:** Primary and Secondary ranges for all subnets
  - **Cloud NAT IP Address:** Automatic
  - **Network Service Tier:** Premium
- Click on **CREATE**  


## Step-05: Verify Internet access in after Cloud NAT Gateway created
```t
# Connect to VM using gcloud
gcloud compute ssh --zone "us-central1-a" "myvm8-internal-only" --tunnel-through-iap 

# Important Note
Wait for 2 to 3 minutes after the Cloud NAT is created before performing below tests

# Ping to any Internet URL
ping stacksimplify.com
ping google.com
Observation:
1. Should pass, because VM is able to access internet using Cloud NAT Gateway

# Try and Install any package
sudo apt install -y telnet
Observation:
1. Should pass, because VM is able to access internet using Cloud NAT Gateway to download and install the package

# Verify External IP created for Cloud NAT
Go to VPC Networks -> IP Addresses
```

## Step-06: Delete VM Instance and Cloud Run Service
```t
# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm8-internal-only --zone=us-central1-a --delete-disks=all 

# Delete Cloud NAT Gateway and Cloud Router
1. Goto Network Services -> Cloud NAT -> mycloudnat1 -> DELETE
2. Goto Network Connectivity -> Cloud Routers -> mycloudrouter1 -> DELETE
```

