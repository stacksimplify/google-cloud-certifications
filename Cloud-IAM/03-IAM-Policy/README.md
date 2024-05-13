---
title: Google Cloud IAM - Master IAM Policies
description: Learn to use Google Cloud IAM Policies
---

## Step-01: Introduction
- Learn the following about IAM Policies
  - get-iam-policy
  - add-iam-policy-binding
  - remove-iam-policy-binding

## Step-02: Get IAM Policy Command
```t
# Get IAM Policy 
gcloud <resource-type> get-iam-policy <resource-id> 
gcloud projects get-iam-policy gcplearn9

# Get IAM Policy with format
gcloud <resource-type> get-iam-policy <resource-id> 
gcloud projects get-iam-policy gcplearn9 --format=json
gcloud projects get-iam-policy gcplearn9 --format=yaml
```
## Step-03: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- Access **Cloud Storage Buckets Service**
- **Observation-1:** gcpuser08@gmail.com dont have access to Cloud Storage Buckets Service don't have 
```t
# ERROR MESSAGE
You need additional access to the project:  gcplearn9
To request access, contact your project administrator and provide them a copy of the following information:

Troubleshooting info:
  Principal: gcpuser08@gmail.com
  Resource: gcplearn9
  Troubleshooting URL: console.cloud.google.com/iam-admin/troubleshooter;permissions=storage.buckets.list;principal=gcpuser08@gmail.com;resources=%2F%2Fcloudresourcemanager.googleapis.com%2Fprojects%2Fgcplearn9/result

Missing or denied permissions:
  storage.buckets.list
```

## Step-04: Add IAM Policy Binding
```t
# Set Project and User (UPDATE YOUR PROJECT AND USER DETAILS HERE)
PROJECTID=gcplearn9
USERID=gcpuser08@gmail.com

# Add IAM Policy Binding
gcloud <resource-type> add-iam-policy-binding <resource-id> --member <principal> --role=<roleid>
gcloud projects add-iam-policy-binding $PROJECTID --member user:$USERID --role=roles/storage.admin

# Get IAM Policy for the Project
gcloud projects get-iam-policy gcplearn9
```

## Step-05: Verify access to Cloud Storage Service
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- Access **Cloud Storage Buckets Service**
- **Observation-1:** gcpuser08@gmail.com should have access to Cloud Storage Buckets Service

## Step-06: Remove IAM Binding
```t
# Set Project and User (UPDATE YOUR PROJECT AND USER DETAILS HERE)
PROJECTID=gcplearn9
USERID=gcpuser08@gmail.com

# Add IAM Policy Binding
gcloud <resource-type> remove-iam-policy-binding <resource-id> --member <principal> --role=<roleid>
gcloud projects remove-iam-policy-binding $PROJECTID --member user:$USERID --role=roles/storage.admin

# Get IAM Policy for the Project
gcloud projects get-iam-policy gcplearn9
```

## Step-07: Verify access to Cloud Storage Service
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- Access **Cloud Storage Buckets Service**
- **Observation-1:** gcpuser08@gmail.com should not have access to Cloud Storage Buckets Service

## Step-08: Delete VM Instance
```t
# Delete VM instance
gcloud compute instances delete vm1 --zone us-central1-a
```


## References 
- https://cloud.google.com/iam/docs/principal-identifiers
- https://cloud.google.com/sdk/gcloud/reference/iam/policies/create
