---
title: Google Cloud Compute Engine Hyperdisks
description: Learn to Compute Engine Hyperdisks
---

## Step-01: Introduction
- Understand Hyperdisks
- Create Hyperdisk
 
## Step-02: Create Hyperdisk
- Go to Compute Engine -> Storage -> Disks
- **Name:** hyperdisk1
- **Description:** hyperdisk1
- **Location:** 
  - **Region:** us-central1 (Iowa)
  - **Zone:** us-central1-a
- **Disk source type:** Blank disk
- **Disk settings:** 
  - **Disk type:** Hyperdisk Balanced
  - **Size:** 100
  - **Provisioned IOPS:** 3600 (LEAVE TO DEFAULTS)
  - **Provisioned throughput:** 290 (LEAVE TO DEFAULTS)
- **Storage pool:** leave UNCHECKED  
- **Snapshot schedule (Recommended):**  leave empty 
- **Encryption:** Google managed encryption 
- Click on **CREATE**
```t
# Create Hyperdisk Balanced
gcloud compute disks create hyperdisk2 \
    --project=gcplearn9 \
    --type=hyperdisk-balanced \
    --description=hyperdisk1 \
    --size=100GB \
    --zone=us-central1-a \
    --provisioned-iops=3600 \
    --provisioned-throughput=290
```

## Step-03: Review the Hyperdisk
- Go to Compute Engine -> Storage -> Disks -> hyperdisk1

## Step-04: Clean-Up
```t
# Delete Hyperdisk
gcloud compute disks delete hyperdisk1 --zone us-central1-a
```
## Additional Reference
- https://cloud.google.com/compute/docs/disks/hyperdisks