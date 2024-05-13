---
title: Google Cloud Create VM instance with Instance Template
description: Learn to Create VM instance with Instance Template on Google Cloud Platform GCP
---

## Step-01: Introduction
1. Create an Instance Template
2. Create VM from Instance Template
3. Use **CREATE SIMILAR** option to create a clone of instance template
## Step-02: Create Instance Template
- Go to Compute Enginer -> Virtual Machines -> Instance Templates -> Create Instance Template -> Provide required details
- **Name:** demo4-instance-template
- **Location:** Regional
- **Region:** us-central1
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Availability Policies:**
  - **VM Provisioning Model:** Standard    
- **Display Device:** unchecked (leave to default)
- **Confidential VM Service:** unchecked (leave to default)
- **Container:** unchecked (leave to default)
- **Boot Disk:** Leave to defaults
- **Identity and API Access:**
  - **Service Account:** Compute Engine default Service Account
  - **Access Scopes:** Allow default Access
- **Firewall**
  - Allow HTTP Traffic
- **Advanced Options**
  - **Management:**
    - **Description:** demo4-vm-startupscript
    - **Reservations:** Automatically use created reservation (leave to default)
    - **Automation:**
      - **Startup Script:** Copy paste content from `webserver-install.sh` file
- Click on **Create**


## Step-03: Create VM Instance using Instance Template
- **Option-1:** Go to Compute Engine -> VM Instances -> Create Instance -> New VM instance from template -> demo4-instance-template -> Click on Continue 
- **Option-2:** Go to Compute Engine -> Instance Templates -> demo4-instance-template -> Create VM
- **Name:** demo4-vm-from-instance-template
- Rest all verify if loaded from Instance Template
- Click on **Create**


## Step-04: Verify by accessing webserver pages
- If required, you can do SSH connect and verify
```t
# Access Webserver Pages
http://<external-ip-of-vm>
```  
## Step-05: Stop VM, Delete VM 
- Go to VM Instances -> demo4-instance-template  -> delete
```t
# Delete VM instnace
gcloud compute instances delete demo4-instance-template --zone us-central1-a
```

## Step-05: Use CREATE SIMILAR Option in Instance Template
- Use **CREATE SIMILAR** option to create a clone of instance template
- **Name:** demo4-instance-template-v2

## Step-06: Create Instance Template using gcloud cli
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create Instance Template
gcloud compute instance-templates create demo4-it-v1 \
  --machine-type=e2-micro \
  --network-interface=network=default,network-tier=PREMIUM \
  --instance-template-region=us-central1 \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 
```