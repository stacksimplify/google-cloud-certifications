---
title: Google Cloud IAM - Master IAM Roles using gcloud cli
description: Learn to use Cloud IAM Roles in Google Cloud
---

## Step-01: Introduction
- We are create IAM Roles using gcloud
  - gcloud iam roles create with flags
  - gcloud iam roles create with role definition in YAML file
  - gcloud iam roles update

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

## Step-04: Custom Role: Delete VM
### Step-04-01: Role Definition using YAML file
```yaml
title: "Custom Compute Instance Delete Role 102"
description: "My custom role used for deletion of Compoute Instance 101"
stage: "ALPHA"
includedPermissions:
- compute.instances.delete
```

### Step-04-02: Create a IAM Role with YAML File at Project Level
```t
# Upload the file to Cloud Shell
Upload the file: delete-instance-role.yaml to cloud shell

# Create a IAM Role with YAML File
gcloud iam roles create myInstanceDelete102 \
  --project=gcplearn9 \
  --file=delete-instance-role.yaml

# Describe Role
gcloud iam roles describe ROLE_ID --project=gcplearn9
gcloud iam roles describe myInstanceDelete102 --project=gcplearn9
```

### Step-04-03: Create a IAM Role with gcloud using flags at Project Level
```t
# Create a IAM Role with flags
gcloud iam roles create myInstanceReset102 \
  --project=gcplearn9 \
  --title="Custom Compute Instance Reset Role 102" \
  --description="My custom role used for Reset of Compoute Instance" \
  --permissions="compute.instances.reset" \
  --stage="ALPHA" 

# Describe Role
gcloud iam roles describe ROLE_ID --project=gcplearn9
gcloud iam roles describe myInstanceReset102 --project=gcplearn9
```

## Step-05: Add IAM Roles to User: gcpuser08@gmail.com
- Go to IAM & Admin -> IAM -> GRANT ACCESS
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Compute Viewer
- **Select Role:** Custom Role Start Stop VM
- **Select Role:** Custom Compute Instance Delete Role 102
- **Select Role:** Custom Compute Instance Reset Role 102
- Click on **SAVE**


## Step-06: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- **Observation-1:** We should have options **DELETE** and **RESET** options enabled


## Step-07: Update IAM Role (ADD PERMISSIONS, REMOVE PERMISSIONS) with flags
```t
# ADD PERMISSIONS: Update a IAM Role with flags to 
gcloud iam roles update myInstanceReset102 \
  --project=gcplearn9 \
  --add-permissions="compute.instances.suspend"

# Describe Role
gcloud iam roles describe ROLE_ID --project=gcplearn9
gcloud iam roles describe myInstanceReset102 --project=gcplearn9  

# REMOVE PERMISSIONS: Update a IAM Role with flags to 
gcloud iam roles update myInstanceReset102 \
  --project=gcplearn9 \
  --remove-permissions="compute.instances.suspend"

# Describe Role
gcloud iam roles describe ROLE_ID --project=gcplearn9
gcloud iam roles describe myInstanceReset102 --project=gcplearn9  
```
## Step-08: Clean-Up VM Instances
- Delete VM Instances 
