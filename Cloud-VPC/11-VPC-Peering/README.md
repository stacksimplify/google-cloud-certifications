# Google Cloud VPC - VPC Peering

## Step-01: Introduction
- Create two VPCs vpc1 and vpc2
- Create two subnets one in each vpc (vpc1subnet, vpc2subnet)
- Create two VM instances one in each subnet (vpc1-vm, vpc2-vm)
- Verify ping tests from VM Instances and it should **FAIL**
- Create VPC Peering connections between VPC1 and VPC2
- Verify ping tests from VM instances and it should **PASS**

## Step-02: Create VPC1 and Subnet in VPC1
### Step-02-01: Create VPC1
- Goto VPC Network -> **CREATE VPC NETWORK**
- **Name:** vpc1
- **Description:** VPC1 custom mode
- **Subnets:** Custom
- **Firewall rules:**
  - allow-ssh
  - allow-icmp
  - allow-custom
- **Dynamic routing mode:** Global (Leave to default)
- Click on **CREATE**

### Step-02-02: Create a Subnet in VPC1
- Gotp VPC Networks -> VPC1 -> SUBNETS -> ADD SUBNET
- **Name:** vpc1subnet
- **Description:** vpc1subnet in us-central1 region
- **VPC Network:** vpc1
- **Region:** us-central1
- **Purpose:** None
- **IP stack type:** IPv4(single-stack)
- **IP Subnet:** 10.0.1.0/24
- REST ALL LEAVE TO DEFAULT
- Click on **ADD**


## Step-03: Create VPC2 and Subnet in VPC2
### Step-03-01: Create VPC2
- Goto VPC Network -> **CREATE VPC NETWORK**
- **Name:** vpc2
- **Description:** VPC2 custom mode
- **Subnets:** Custom
- **Firewall rules:**
  - allow-ssh
  - allow-icmp
  - allow-custom
- **Dynamic routing mode:** Global (Leave to default)
- Click on **CREATE**

### Step-03-02: Create a Subnet in VPC2
- Gotp VPC Networks -> VPC2 -> SUBNETS -> ADD SUBNET
- **Name:** vpc2subnet
- **Description:** vpc2subnet in us-central1 region
- **VPC Network:** vpc2
- **Region:** us-central1
- **Purpose:** None
- **IP stack type:** IPv4(single-stack)
- **IP Subnet:** 10.0.121.0/24
- REST ALL LEAVE TO DEFAULT
- Click on **ADD**


## Step-04: Create VM Instances in both VPCs
```t
# Set Project 
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM in vpc1subnet1 
gcloud compute instances create vpc1-vm \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=vpc1subnet

# Create VM in vpc2subnet1 
gcloud compute instances create vpc2-vm \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=vpc2subnet
```
## Step-05: Verify ping test between both vms created in VPC1 and VPC2
```t
# Connect to VM and Verify Ping from vpc1-vm to vpc2-vm 
gcloud compute ssh --zone "us-central1-a" "vpc1-vm" --project "gcplearn9"
ping <vpc2-vm-internalip>
Observation: 
1. ping test should FAIL

# Connect to VM and Verify Ping from vpc2-vm to vpc1-vm
gcloud compute ssh --zone "us-central1-a" "vpc1-vm" --project "gcplearn9"
ping <vpc1-vm-internalip>
Observation: 
1. ping test should FAIL
```

## Step-06: Create VPC Peering Connections for VPC1 and VPC2
### Step-06-01: Create VPC Peering connection from VPC1 to VPC
- Go to VPC Network -> VPC network peering -> **CREATE PEERING CONNECTION**
- **Name:** vpc1-to-vpc2-peering
- **Your VPC Network:** vpc1
- **Peered VPC network:** gcplearn9
- **VPC network name:** vpc2
- **IPv4 (single-stack):** Enabled
- **Import subnet routes with privately used public IPv4 addresses:** ENABLED
- **Export subnet routes with privately used public IPv4 addresses:** ENABLED
- Click on **CREATE**

### Step-06-02: Create VPC Peering connection from VPC1 to VPC
- Go to VPC Network -> VPC network peering -> **CREATE PEERING CONNECTION**
- **Name:** vpc2-to-vpc1-peering
- **Your VPC Network:** vpc2
- **Peered VPC network:** gcplearn9
- **VPC network name:** vpc1
- **IPv4 (single-stack):** Enabled
- **Import subnet routes with privately used public IPv4 addresses:** ENABLED
- **Export subnet routes with privately used public IPv4 addresses:** ENABLED
- Click on **CREATE**


## Step-07: Verify VPC Peering connection status
- Go to VPC Network -> VPC network peering -
- Both peering connections status should be *ACTIVE**

## Step-08: Verify ping test between both vms created in VPC1 and VPC2
```t
# Connect to VM and Verify Ping from vpc1-vm to vpc2-vm 
gcloud compute ssh --zone "us-central1-a" "vpc1-vm" --project "gcplearn9"
ping <vpc2-vm-internalip>
Observation: 
1. ping test should PASS

# Connect to VM and Verify Ping from vpc2-vm to vpc1-vm
gcloud compute ssh --zone "us-central1-a" "vpc1-vm" --project "gcplearn9"
ping <vpc1-vm-internalip>
Observation: 
1. ping test should PASS
```
