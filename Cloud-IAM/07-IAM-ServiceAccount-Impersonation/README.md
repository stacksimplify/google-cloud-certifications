---
title: Google Cloud IAM - Service Accounts Impersonation
description: Learn to use Google Cloud IAM - Service Accounts Impersonation
---

## Step-01: Introduction
- Create VM Instance with a normal user impersonating using a Service Account which has Compute Admin permissions

## Step-02: Create a user with Compute Viewer Permission
- Go to IAM & Admin -> IAM -> GRANT ACCESS
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Compute Viewer
- Click on **SAVE**

## Step-03: Configure Cloud Shell gcloud with Normal user
```t
# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list

# Authorize with a user account without setting up a configuration.
gcloud auth login

# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list
```

## Step-04: Create Compute Instances using Normal User
```t
# Create VM Instance
gcloud compute instances create vm11 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default 

# Observation
1. As user  "gcpuser08@gmail.com" have only Compute Viewer role assigned, it cannot create VM Instance
2. It can only list VMs and cannot create VMs
```

## Step-05: Assign Service Account Token Creator Role to Normal User
```t
# Assign Service Account Token Creator Role
Normal User: gcpuser08@gmail.com
Role-1: Compute Viewer
Role-2: Service Account Token Creator
```

## Step-06: Create Service Account with required roles
```t
# Create Service Account with required roles
Service Account: mycomputeadmin@gcplearn9.iam.gserviceaccount.com 
Role-1: Service Account User
Role-2: Compute Admin
```

## Step-07: Create VM Instance with --impersonate-service-account
```t
# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list

# Authorize with a user account without setting up a configuration.
gcloud auth login
Observation: use the normal user gcpuser08@gmail.com

# Lists accounts whose credentials have been obtained using gcloud init
gcloud auth list

# Create VM Instances with  --impersonate-service-account Flag
gcloud compute instances create vm103 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --impersonate-service-account=mycomputeadmin@gcplearn9.iam.gserviceaccount.com 
Observation: 
1. VM instance should be created 

# List VM Instances
gcloud compute instances list
Observation:
1. This should work, because we have Compute Viewer permission to Normal user gcpuser08@gmail.com
2. We dont need "--impersonate-service-account" for this flag
```

## Step-08: Delete VM Instance using --impersonate-service-account flag
```t
# Delete VM Instance
gcloud compute instances delete vm103 \
  --zone=us-central1-a \
  --impersonate-service-account=mycomputeadmin@gcplearn9.iam.gserviceaccount.com 
```

## Additional References
- https://cloud.google.com/iam/docs/service-account-impersonation
