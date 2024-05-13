---
title: GCP Google Cloud Platform - Cloud Monitoring Groups
description: Learn to use Cloud Monitoring Groups
---

## Step-01: Introduction
1. Learn the following Cloud Monitoring concepts
2. Groups: 
  - Monitoring lets you define and monitor groups of resources, such as VM instances, databases, and load balancers. 
  - You can organize resources into groups based on criteria that make sense for your applications

## Step-02: Create VM Instance with sample webserver installed
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance: demovm1
gcloud compute instances create demovm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 

# Create VM Instance: demovm2
gcloud compute instances create demovm2 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 

# List Compute Instances
gcloud compute instances list   
```

## Step-03: Create Monitoring Group for both VMs
- Go to Cloud Monitoring -> Configure -> Groups -> **CREATE GROUP**
- **Name:** vm-group1
### Criteria
- **Type:** Name
- **Operator:** contains
- **Value:** demovm
- Click on **DONE**
- Click on **CREATE**


## Step-04: Create Uptime Checks
- Go to Cloud Monitoring -> Detect -> Uptime checks -> CREATE UPTIME CHECK
### Target
- **Protocol:** HTTP
- **Resource type:** Instance
- **Applies to:** Group
- **Group:** vm-group1 
- **Path:** /index.html
- **Check Frequency:** 1 minute
- **Regions:** Global (leave to defaults)
- REST ALL LEAVE TO DEFAULTS
- **CONTINUE**
### Response Validation
- **Response Timeout:** 10 seconds
- **Content matching is enabled**: Enable it
- **Response Content Match Type:** contains
- **Response content:** Welcome
- REST ALL LEAVE DEFAULTS
- **CONTINUE**
### Alert & Notification
- **Create an alert:** enable it
- **Name:** Uptime failure for vm-group1
- **Durantion:** 1 minute
- **Notifications:** Create new Notification channel (EMAIL)
- **CONTINUE**
### Review 
- **Enter a name for the uptime check**
- **Title:** vm-group1 Uptime Checks
- Click on **CREATE**


## Step-05: Stop VM and Verify the Incidents
```t
# Stop VM
gcloud compute instances stop demovm1 --zone=us-central1-a
gcloud compute instances stop demovm2 --zone=us-central1-a

# Verify email in gmail
We should see Incident emails for both VMs

# Observation
1. We can create monitoring alerts for group of VMs with a single policy
```

## Step-06: Clean-Up
```t
# Delete VMs
gcloud compute instances delete demovm1 --zone=us-central1-a
gcloud compute instances delete demovm2 --zone=us-central1-a

# Delete Uptime checks and Alert policy
Go to Cloud Monitoring -> Detect -> Uptime checks -> vm-group1 Uptime Checks -> DELETE

# Delete Groups
Go to Cloud Monitoring -> Configure -> Groups -> vm-group1 -> Delete
```
