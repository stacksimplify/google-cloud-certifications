---
title: Google Cloud IAM - Implement IAM Conditions
description: Learn to use Google Cloud IAM Conditions
---

## Step-01: Introduction
- Implement IAM Conditions practically

## Step-02: Create a VM Instance 
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance
gcloud compute instances create vm201 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default 
```

## Step-03: Pre-requisite: Create a test gmail id for this demo
- gcpuser08@gmail.com
- NO ROLE ASSIGNED
- **Observation:** NO ACCESS TO COMPUTE ENGINE SERVICE

## Step-04: NEGATIVE CASE: Associate a Role: Compute Viewer with Condition which fails
### Step-04-01: Add Principal with IAM Role:Computr Viewer with Condition and Verify
- Go to IAM & Admin -> IAM -> GRANT ACCESS
#### IAM ROLE
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Compute Viewer
#### IAM Condition
- **Title:** access-on-a-day
- **Condition type:** Day of week
- **Operator:** On
- **Day of week:** Tuesday
- **Choose time zone:** India Standard Time IST
- Click on **SAVE**
```t
# CEL - Common Expression Language
request.time.getDayOfWeek("Asia/Calcutta") == 2
```
- Click on **SAVE**
### Step-04-02: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- Go to **Compute Engine**
- **Observation:** We should see NO ACCESS TO COMPUTE ENGINE


## Step-05: POSITIVE CASE: Associate a Role: Compute Viewer with Condition which passes
### Step-05-01: Add Principal with IAM Role:Computr Viewer with Condition and Verify
- Go to IAM & Admin -> IAM -> GRANT ACCESS
#### IAM ROLE
- **Add Principal:** gcpuser08@gmail.com
- **Select Role:** Compute Viewer
#### IAM Condition
- **Title:** access-on-a-day
- **Condition type:** Day of week
- **Operator:** On
- **Day of week:** CURRENT DAY (sunday)
- **Choose time zone:** India Standard Time IST
- Click on **SAVE**
```t
# CEL - Common Expression Language
request.time.getDayOfWeek("Asia/Calcutta") == 0
```
- Click on **SAVE**
### Step-05-02: Login to Google Cloud with new user gcpuser08@gmail.com
- Open in New incognito window
- [Login to Google Cloud](https://cloud.google.com)
  - **Username:** gcpuser08@gmail.com
  - **Password:** XXXXXXXX
- Select Project **gcplearn9**
- Go to **Compute Engine**
- **Observation:** We should be able to view the COmpute engine VM instances


## Step-06: Clean-Up
```t
# Delete VM instance
gcloud compute instances delete vm201 --zone=us-central1-a 

# Remove access to gcpuser08@gmail.com
1. Remove IAM Condition
2. Remove Compute Viewer Role
```





