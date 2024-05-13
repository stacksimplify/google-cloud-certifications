# Cloud VPC Modes - Auto and Custom

## Step-01: Introduction
- Create Auto Mode VPC Network
- Create Custom VPC Network
- Create Subnet in Custom VPC Network
- Create or Launch a compute instance in a subnet in custom vpc network with webserver startup script and verify
- Clean-Up: Delete compute instance


## Step-02: Understand default VPC Network
- Go to VPC Network -> default VPC
- **default subnets** are pre-created and ready for use in **default vpc**

## Step-03: Auto mode VPC Network
### Step-03-01: Create a auto mode VPC network
- Goto VPC Network -> **CREATE VPC NETWORK**
- **Name:** vpc1-auto
- **Description:** Automode VPC
- **Subnets:** automatic
- **Firewall Rules:**
  - allow-custom (internal access between all subnets in a vpc)
  - allow-icmp
  - allow-rdp
  - allow-ssh
- **Dynamic routing mode:** Regional (Leave to default)
- Click on **CREATE**
### Step-03-02: Verify Auto mode VPC resources
- Goto vpc1-auto -> SUBNETS
- Verify subnets created in each region

## Step-04: Custom mode VPC Network
### Step-04-01: Create Custom mode VPC Network
- Goto VPC Network -> **CREATE VPC NETWORK**
- **Name:** vpc2-custom
- **Description:** Custom-mode-VPC
- **Subnets:** Custom
- **Firewall rules:**
  - allow-ssh
  - allow-icmp
- **Dynamic routing mode:** Regional (Leave to default)
- Click on **CREATE**


### Step-04-02: Create a Subnet
- Gotp VPC Networks -> vpc2-custom -> SUBNETS -> ADD SUBNET
- **Name:** mysubnet1
- **Description:** mysubnet1
- **VPC Network:** vpc2-custom
- **Region:** us-central1
- **Purpose:** None
- **IP stack type:** IPv4(single-stack)
- **IP Subnet:** 10.225.0.0/20
- REST ALL LEAVE TO DEFAULT
- Click on **ADD**


## Step-05: Create VM Instance in mysubnet1 of vpc2-custom VPC Network
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in mysubnet1 [or] Create using Webconsole
cd 01-VPC-Auto-and-Custom
gcloud compute instances create myvm1 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=mysubnet1 

# List Compute Instances (Optional)
gcloud compute instances list   

# Describe Compute Instance to view Network configuration (Optional)
gcloud compute instances describe myvm1 --zone=us-central1-a

# Connect to VM (Optional)
gcloud compute ssh --zone "ZONE_NAME" "VM_NAME" --project "PROJECT_ID"
gcloud compute ssh --zone "us-central1-a" "myvm1" --project "gcplearn9"


# Verify Application Deployed in Custom VPC
1. Verify if Compute Instance deployed in vpc2-custom network, in mysubnet1
2. Verify VM Instance Interal IP Address
```


## Step-06: Delete VM Instance 
- Delete VM Instance created as part of this demo
```t
# List and Delete Compute Instance
gcloud compute instances list 
gcloud compute instances delete myvm1 --zone=us-central1-a --delete-disks=all
```
