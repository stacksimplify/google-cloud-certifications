---
title: Google Cloud IAM - Service Accounts
description: Learn to use Google Cloud IAM Policies
---

## Step-01: Introduction
- Perform Service Account steps using gcloud
  - Create VM Instance
  - Connect to Compute Instance and create Storage Bucket and it should fail with default service account associated to Compute Instance
  - Create a Service Account
  - Associate a Storage Admin Role to Service Account
  - Swithc the Service Account to Compute Instance with new one
  - Connect to Compute Instance, create Storage Bucket and It should work
  - Delete VM Instance

## Step-02: Create a VM Instance 
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance
gcloud compute instances create vm902 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default 
```

## Step-03: Connect to VM Instance and verify with default service account we have access to create Storage Buckets
```t
# Connect to VM Instance
gcloud compute ssh --zone "us-central1-a" "vm902" --project "gcplearn9"

# Set Project config
gcloud config set project PROJECT-ID
gcloud config set project gcplearn9

# List Accounts or Service Accounts configured
gcloud auth list

# List Cloud Storage Buckets
gcloud storage buckets list

# Create Cloud Storage Bucket
gcloud storage buckets create gs://BUCKET_NAME
gcloud storage buckets create gs://mybucket1032

## Sample Output
dkalyanreddy@vm902:~$ gcloud storage buckets create gs://mybucket1032
Creating gs://mybucket1032/...
ERROR: (gcloud.storage.buckets.create) HTTPError 403: Access denied.
dkalyanreddy@vm902:~$ 
```

## Step-04: Create IAM Service Account using Cloud Shell
```t
# List Accounts or Service Accounts configured
gcloud auth list

# Create IAM Service Account
gcloud iam service-accounts create SERVICE_ACCOUNT_NAME \
  --description="DESCRIPTION" \
  --display-name="DISPLAY_NAME"

# REPLACE VALUES
gcloud iam service-accounts create mysa902 \
  --description="Service Account for VM Instances with Storage Admin privileges" \
  --display-name="mysa902"  

# Describe Service Account
gcloud iam service-accounts describe mysa902@gcplearn9.iam.gserviceaccount.com  
```

## Step-05: Verify the Service Account 
- Goto -> IAM & Admin -> Service Accounts -> **mysa902@gcplearn9.iam.gserviceaccount.com**
- DETAILS TAB
- PERMISSIONS TAB
- KEYS TAB
- METRICS TAB
- LOGS TAB

## Step-06: Grant access to Service Account and Verify
### Step-06-01: Grant Service Account an IAM Role
```t
# Grant service account an IAM role 
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com" \
  --role="ROLE_NAME"

# REPLACE VALUES
gcloud projects add-iam-policy-binding gcplearn9 \
  --member="serviceAccount:mysa902@gcplearn9.iam.gserviceaccount.com" \
  --role="roles/storage.admin"    

# Get IAM Policy for the Project
gcloud projects get-iam-policy gcplearn9

# Sample Output
- members:
  - serviceAccount:mysa902@gcplearn9.iam.gserviceaccount.com
  role: roles/storage.admin
```
### Step-06-02: Verify Service Account
- Goto -> IAM & Admin -> IAM -> **mysa902@gcplearn9.iam.gserviceaccount.com**
- Click on **EDIT**
- Click on **ASSIGN ROLES**  (If we want to add more roles)

## Step-07: Update VM Instance with new Service Account
```t
# Stop VM Instance
gcloud compute instances stop vm902 --zone us-central1-a

# Update VM Instance with Service Account
gcloud compute instances set-service-account vm902 \
  --project=gcplearn9 \
  --zone=us-central1-a \
  --scopes=cloud-platform \
  --service-account=mysa902@gcplearn9.iam.gserviceaccount.com 

# Describe VM Instance
gcloud compute instances describe vm902 --zone us-central1-a

# Start VM Instance
gcloud compute instances start vm902 --zone us-central1-a
```
## Step-08: Connect to VM Instance and verify with new service account we have access to create Storage Buckets
```t
# Connect to VM Instance
gcloud compute ssh --zone "us-central1-a" "vm902" --project "gcplearn9"

# List Accounts or Service Accounts configured
gcloud auth list
Observation:
1. Newly created service account should be active

# Set Project config
gcloud config set project PROJECT-ID
gcloud config set project gcplearn9

# List Cloud Storage Buckets
gcloud storage buckets list

# Create Cloud Storage Bucket
gcloud storage buckets create gs://BUCKET_NAME
gcloud storage buckets create gs://mybucket1032
Important Note: Bucket name should be unique across google cloud

## Sample Output
dkalyanreddy@vm902:~$ gcloud storage buckets create gs://mybucket1032
Creating gs://mybucket1032/...
dkalyanreddy@vm902:~$ 

# List Cloud Storage Buckets
gcloud storage buckets list

# Delete Cloud Storage Bucket 
gcloud storage buckets delete gs://mybucket1032
```

## Step-09: Delete VM Instance
```t
# Delete VM instance
gcloud compute instances delete vm902 --zone us-central1-a
```

## Step-10: Get IAM Policy and Verify the Service Account and Role
```t
# Get IAM Policy for the Project
gcloud projects get-iam-policy gcplearn9

# Sample Output
- members:
  - serviceAccount:mysa902@gcplearn9.iam.gserviceaccount.com
  role: roles/storage.admin
```
