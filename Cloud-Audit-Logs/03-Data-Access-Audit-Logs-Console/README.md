# Cloud Audit Logs - Data Access Audit Logs

## Step-01: Introduction
- We are going to learn about **Data Access Audit Logs**
- We are going to enable it using **Audit Logs** service in Cloud IAM using Google Cloud web console

## Step-02: Review IAM Policy BEFORE Audit Log Changes
```t
# Review IAM Policy - Before changes
gcloud projects get-iam-policy gcplearn9 --format=yaml
```

## Step-03: Enable Data Access Audit Logs in Cloud IAM
- Go to Cloud IAM -> Audit Logs
- Select **Compute Engine API** -> Enable
- **Admin Read**
  - Getting information about a resource (compute.images.get)
  - Listing resources (compute.instances.list)
  - Listing resources across scope (aggregated list requests) (compute.interconnectAttachments.aggregatedList)
- **Data Read**
  - Exclusively enabled for compute.instance.getSerialPortOutput)
- Click on **SAVE**


## Step-04: Review IAM Policy AFTER Audit Log Changes
```t
# Review IAM Policy - AFTER changes
gcloud projects get-iam-policy gcplearn9 --format=yaml

# FOLLOWING WILL BE ADDED TO IAM Policy
auditConfigs:
- auditLogConfigs:
  - logType: ADMIN_READ
  - logType: DATA_READ
  service: compute.googleapis.com
```

## Step-05: List VM Instances from Cloud Shell
```t
# List VM Instances
gcloud compute instances list
```

## Step-06: Review Data Access Logs in Log Explorer
- Go to Log Explorer -> Select Logs -> **data_access**
```t
# Log Query
logName="projects/gcplearn9/logs/cloudaudit.googleapis.com%2Fdata_access"
```