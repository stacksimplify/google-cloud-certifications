---
title: GCP Google Cloud Platform - Cloud Monitoring Uptime Checks
description: Learn to deploy Cloud Monitoring Uptime checks
---

## Step-01: Introduction
0. Implement the following Cloud Monitoring concepts
1. Create VM Instance with sample webserver installed
2. Define Uptime checks
3. Define Alert Policy and Notification Channel
4. Simulate Incidents
5. Verify incidents in email and address incidents

## Step-02: Create VM Instance with sample webserver installed
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance
gcloud compute instances create myvm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 

# List Compute Instances
gcloud compute instances list   
```
## Step-03: Create Uptime Checks
- Go to Cloud Monitoring -> Detect -> Uptime checks -> CREATE UPTIME CHECK
### Target
- **Protocol:** HTTP
- **Resource type:** Instance
- **Applies to:** Single
- **Instance:** myvm1 
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
- **Name:** Uptime failure
- **Durantion:** 1 minute
- **Notifications:** Create new Notification channel (EMAIL)
- **CONTINUE**
### Review 
- **Enter a name for the uptime check**
- **Title:** myvm1 uptime check
- Click on **CREATE**

## Step-04: Verify Uptime checks
- Go to Cloud Monitoring -> Detect -> Uptime checks -> **myvm1 uptime check**
```t
# Verify check_passed value
check_passed=0
```

## Step-05: Review Alert Policy
- Go to Cloud Monitoring -> Detect -> Uptime checks -> **myvm1 uptime check** -> **myvm1 uptime check uptime failure**
- **OR**
- Go to Cloud Monitoring -> Detect -> Alerting -> Policies


## Step-06: Stop VM and Verify the Incidents
```t
# Stop VM
gcloud compute instances stop myvm1 --zone=us-central1-a

# Verify email in gmail
We should see a Incident email

# Verify the Uptime checks
Go to Cloud Monitoring -> Detect -> myvm1 uptime check 

# Verify the incidents
Go to Cloud Monitoring -> Detect -> Alerting  -> Incidents -> Open Incident

# Verify check_passed value in Alert policy
check_passed=6
Observation: should be greater than 0
```

## Step-07: Start VM and Verify the Incidents
```t
# Start VM
gcloud compute instances start myvm1 --zone=us-central1-a

# Verify the incidents
Go to Cloud Monitoring -> Detect -> Alerting  -> Incidents -> Open Incident
check_passed=6
Observation: 
1. should be check_passed=0
2. Incident should be auto-closed
```

## Step-08: Review
```t
# Connect to VM Instance
gcloud compute ssh --zone "us-central1-a" "myvm1" --project "gcplearn9"

# Verify Nginx access logs
tail -100f /var/log/nginx/access.log

# Sample Log - Cloud Monitoring Entries
35.205.72.231 - - [03/May/2024:04:32:05 +0000] "GET /index.html HTTP/1.1" 200 248 "-" "GoogleStackdriverMonitoring-UptimeChecks(https://cloud.google.com/monitoring)"
35.238.118.210 - - [03/May/2024:04:32:10 +0000] "GET /index.html HTTP/1.1" 200 248 "-" "GoogleStackdriverMonitoring-UptimeChecks(https://cloud.google.com/monitoring)"
```
