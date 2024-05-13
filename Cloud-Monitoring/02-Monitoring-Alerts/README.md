---
title: GCP Google Cloud Platform - Cloud Monitoring Alerts
description: Learn to deploy Cloud Monitoring Alerts
---

## Step-01: Introduction
- Install OpsAgent
- Cloud Monitoring Alerts


## Step-02: Install OpsAgent in the VM Instance
```t
# Verify VM Metrics
1. Go to Compute Engine -> VM Instances -> myvm1 -> OBSERVABILITY Tab
2. Click on CPU, PROCESS, MEMORY
3. It shows the message "Requires Ops Agent"

# Connect SSH to VM
gcloud compute ssh --zone "us-central1-a" "myvm1" --project "gcplearn9"

# Download Ops Agent
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh

# Install Ops Agent
sudo bash add-google-cloud-ops-agent-repo.sh --also-install
sudo apt list --installed | grep google-cloud-ops-agent

# Verify Ops Agent Status
sudo systemctl status google-cloud-ops-agent"*"

# Restarting Agent (Optional)
sudo service google-cloud-ops-agent restart

# Verify if OPS Agent installed successfully
Go to Cloud Monitoring -> Dashboards -> VM Instances (Predefined)
Verify if OpsAgent status
```

## Step-03: Review Recommended Alerts and Create Alerts
- Go to Compute Engine -> VM Instances -> OBSERVABILITY -> RECOMMENDED ALERTS
- Select Alert Policies
  - VM Instance - High CPU Utilization (myvm1)
  - VM Instance - High Disk Utilization (myvm1)
  - VM Instance - Host Error Log Detected (myvm1)
  - VM Instance - High Memory Utilization (myvm1)
- Configure notifications 
  - **Use notification channel:** enabled 
  - **Notification channel:** select channel 
- Click on **CREATE**

## Step-04: View Alert Policies
- Review all the alert policies

## Step-05: Review Log based alerts
- Review **VM Instance - Host Error Log Detected (myvm1)**