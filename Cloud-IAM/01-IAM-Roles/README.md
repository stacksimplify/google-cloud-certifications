---
title: Google Cloud IAM - Master IAM Roles
description: Learn to use Cloud IAM Roles in Google Cloud
---

## Step-01: Introduction
- We are going to use all 3 role types in this demo
  - Basic Roles
  - Predefined Roles
  - Custom Roles

## Step-02: Create a VM Instance 
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance
gcloud compute instances create vm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default 
```

## Step-03: Pre-requisite: Create a test gmail id for this demo
- gcpuser08@gmail.com

## Step-04: Basic Role: Owner
### Step-04-01: Add Principal with IAM Role:Owner and Verify
- Go to IAM & Admin -> IAM -> GRANT ACCESS
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Owner
- Click on **SAVE**
- Invitation will be sent to new user

### Step-04-02: Login to gmail and accept Invitation
- Login to gamil and accept invitation
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX

### Step-04-03: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- **Observation:** We should see a full access for all resources

## Step-05: Predefined Role: Compute Viewer
### Step-05-01: Add Principal with IAM Role Compute Viewer
- Go to IAM & Admin -> IAM -> GRANT ACCESS
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Compute Viewer
- Click on **SAVE**

### Step-05-02: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- **Observation:** We should see only read-only access


## Step-06: Custom Role: Stop and Start VMs
### Step-06-01: Create Custom Role
- Go to IAM -> Roles -> **CREATE ROLE**
- **Title:** Custom Role Start Stop VM
- **ID:** customRoleStartStopVM101
- **ADD PERMISSIONS:** compute.instance.start, compute.instance.stop
- Click on **CREATE**

### Step-06-02: Additional Role: Add Principal with IAM Role custom-role-start-stop-vm
- Go to IAM & Admin -> IAM -> GRANT ACCESS
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Compute Viewer
- **Select Role:** Custom Role Start Stop VM
- Click on **SAVE**

### Step-06-03: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- **Observation-1:** We should see only read-only access
- **Observation-2:** We should be able to stop and start the VM instance

