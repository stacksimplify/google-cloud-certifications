# Google Cloud - Regional Managed Instance Groups

## Step-01: Introduction
- Creatre VPC: vpc3-custom
- Create Firewall Ingress Rules
  1. Allow ICMP
  2. Allow SSH 22
  3. Allow all ip, all ports between VM instances in a VPC network
  4. Allows traffic from the Google Cloud health checking systems (130.211.0.0/22 and 35.191.0.0/16)
- Create two subnets in two regions
  1. us-central1-subnet
  2. us-east1-subnet  
- Create Instance Template in us-central1, us-east1 regions
- Create Global Health check  (applicable for both us-east1 and us-central1 regions)
- Create Managed Instance Groups in us-central1, us-east1 regions
  - Create Managed Instance Group (MIG)
  - Create Named port for MIG

## Step-02: Create VPC Network
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VPC Network
gcloud compute networks create vpc3-custom --subnet-mode=custom --bgp-routing-mode=global
```

## Step-03: Create VPC Firewall Rules 
```t
# Firewall Rule-1: Allows ICMP connections from any source to any instance on the network
gcloud compute firewall-rules create vpc3-custom-allow-icmp \
  --network=vpc3-custom \
  --description=Allows\ ICMP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network \
  --direction=INGRESS \
  --priority=65534 \
  --source-ranges=0.0.0.0/0 \
  --action=ALLOW \
  --rules=icmp

# Firewall Rule-2: Allows TCP connections from any source to any instance on the network using port 22.
gcloud compute firewall-rules create vpc3-custom-allow-ssh \
  --network=vpc3-custom \
  --description=Allows\ TCP\ connections\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ port\ 22. \
  --direction=INGRESS \
  --priority=65534 \
  --source-ranges=0.0.0.0/0 \
  --action=ALLOW \
  --rules=tcp:22 

# (OPTIONAL) Firewall Rule-3: Allows connection from any source to any instance on the network using custom protocols
gcloud compute firewall-rules create vpc3-custom-allow-custom \
  --network=vpc3-custom \
  --description=Allows\ connection\ from\ any\ source\ to\ any\ instance\ on\ the\ network\ using\ custom\ protocols. \
  --direction=INGRESS \
  --priority=65534 \
  --source-ranges=10.128.0.0/9 \
  --action=ALLOW \
  --rules=all   

# Firewall Rule-4: Ingress rule that allows traffic from the Google Cloud health checking systems (130.211.0.0/22 and 35.191.0.0/16).
gcloud compute firewall-rules create vpc3-custom-allow-health-check \
  --network=vpc3-custom \
  --description=Allows\ traffic\ from\ Google\ Cloud\ health\ checking\ systems \
  --direction=ingress \
  --source-ranges=130.211.0.0/22,35.191.0.0/16 \
  --action=allow \
  --rules=tcp:80      
```

## Step-04: Create Subnets
```t
# Subnet1: Create Subnet in us-central1 region 
gcloud compute networks subnets create us-central1-subnet \
  --description=us-central1-subnet \
  --range=10.135.0.0/20 \
  --stack-type=IPV4_ONLY \
  --network=vpc3-custom \
  --region=us-central1

# Subnet2: Create Subnet in us-east1 region
gcloud compute networks subnets create us-east1-subnet \
  --description=us-east1-subnet \
  --range=10.145.0.0/20 \
  --stack-type=IPV4_ONLY \
  --network=vpc3-custom \
  --region=us-east1
```

## Step-05: Create Health Check - Global
```t
# Create health check - global
gcloud compute health-checks create http global-http-health-check --port 80
```

## Step-06: Review Startup Script
```sh
#!/bin/bash
sudo apt install -y telnet
sudo apt install -y nginx
sudo systemctl enable nginx
sudo chmod -R 755 /var/www/html
HOSTNAME=$(hostname)
sudo echo "<!DOCTYPE html> <html> <body style='background-color:rgb(250, 210, 210);'> <h1>Welcome to StackSimplify - WebVM App1 </h1> <p><strong>VM Hostname:</strong> $HOSTNAME</p> <p><strong>VM IP Address:</strong> $(hostname -I)</p> <p><strong>Application Version:</strong> V1</p> <p>Google Cloud Platform - Demos</p> </body></html>" | sudo tee /var/www/html/index.html
```

## Step-07: us-central1: Create Instance Template and Managed Instance Group
- **Important Note:**
  1. Upload nginx-webserver.sh to Google Cloud shell if running gcloud commands on cloud shell
  2. Ensure nginx-webserver.sh is present in the current directory where you are running this gcloud command
- Create Instance Template
- Create Managed Instance Group
  - Create Managed Instance Group (MIG)
  - Create Named port for MIG
```t
# 1. us-central1: Create Instance Template
gcloud compute instance-templates create it-lbdemo-us-central1 \
   --region=us-central1 \
   --network=vpc3-custom \
   --subnet=us-central1-subnet \
   --machine-type=e2-micro \
   --metadata-from-file=startup-script=nginx-webserver.sh

# 2. Create the managed instance group and select the instance template.
gcloud compute instance-groups managed create mig1-us-central1 \
    --template=it-lbdemo-us-central1 \
    --size=2 \
    --zones=us-central1-b,us-central1-c \
    --health-check=global-http-health-check

# 3. Add a named port to the instance group
gcloud compute instance-groups set-named-ports mig1-us-central1 \
    --named-ports webserver80:80 \
    --region us-central1
```

## Step-04: us-east1: Create Instance Template and Managed Instance Group
- Create Instance Template
- Create Managed Instance Group
  - Create Managed Instance Group (MIG)
  - Create Named port for MIG
```t
# 1. us-east1: Create Instance Template
gcloud compute instance-templates create it-lbdemo-us-east1 \
   --region=us-east1 \
   --network=vpc3-custom \
   --subnet=us-east1-subnet \
   --machine-type=e2-micro \
   --metadata-from-file=startup-script=nginx-webserver.sh 

# 2. us-east1: Create the managed instance group and select the instance template.
gcloud compute instance-groups managed create mig2-us-east1 \
    --template=it-lbdemo-us-east1 \
    --size=2 \
    --zones=us-east1-c,us-east1-d \
    --health-check=global-http-health-check

# 3. us-east1: Add a named port to the instance group
gcloud compute instance-groups set-named-ports mig2-us-east1 \
    --named-ports webserver80:80 \
    --region us-east1
```

## Step-05: Verify the following resources
1. VPC
2. Subnets
3. Firewalls
4. Health Checks
5. Instance Templates
6. Managed Instance Groups

