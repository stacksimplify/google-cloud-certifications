---
title: Google Cloud Create VM instance with Disk Snapshot
description: Learn to Create VM instance with Disk Snapshot on Google Cloud Platform GCP
---

## Step-01: Introduction
- Understand Compute Engine -> Storage -> Disks
- VM Boot Disk
  - Public Images
  - Custom Images
  - Snapshots
  - Existing Disks
- Create a Disk Snapshot
- Create VM Instance with Disk Snapshot

## Step-02: Start VM demo4-vm-from-machine-image
- Go to Compute Engine -> VM Instances -> demo8-vm1 -> Actions -> Start

## Step-03: Create Snapshot
- **Option-1:** Go to Compute Engine -> Storage -> Disks -> demo8-vm1 -> Actions -> Create Snapshot
- **Option-2:** Go to Compute Engine -> Storage -> Snapshots -> Create Snapshot
- **Name:** demo8-vm1-snapshot-1
- **Description:** demo8-vm1-snapshot-1
- **source disk:** demo8-vm1
- **Location:** Mutli-regional
- **Select Location:** us (United States)
- **Encryption:** Uses same encryption as disk
- **Application consistency:** unchecked (leave to defaults)
- Click on **Create**
```t
# Create Snapshot
gcloud compute snapshots create demo8-vm1-snapshot \
    --project=gcplearn9 \
    --description=demo8-vm1-snapshot \
    --source-disk=demo8-vm1 \
    --source-disk-zone=us-central1-a \
    --storage-location=us
```

## Step-04: Review Snapshot Properties
- Go to Compute Engine -> Storage -> Snapshots ->  demo8-vm1-snapshot
- Review Snapshot Properties

## Step-05: Create VM or Disk using Snapshot
- Go to Compute Engine -> Storage -> Snapshots ->  demo8-vm1-snapshot
- Review **CREATE INSTANCE**
- Review **CREATE DISK**

## Step-06: Discuss about Creating Snapshot Schedule
1. **Schedule Options:** Hourly, Daily, Weekly
2. **Autodeletion snapshots after:** 14
3. **Deletion Rule:** Keep Snapshots or Delete Snapshots older than 14 days


## Additional Reference
- [Linux application consistent persistent disk snapshot](https://cloud.google.com/compute/docs/disks/creating-linux-application-consistent-pd-snapshots)