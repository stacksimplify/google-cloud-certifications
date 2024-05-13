---
title: Google Cloud Create Regional Persistent Disk for VM
description: Learn to Create Regional Persistent Disk and attach to VM on Google Cloud Platform GCP
---

## Step-01: Introduction
- Understand importance of Regional persistence disks
- Create a Regional Persistence Disk
- Associate it with two Virtual Machines in `Read-Only` Mode. 

## Step-02: Create Regional Persistent Disk
- Go to Compute Engine -> Storage -> Disks -> Create Disk
- **Name:** regional-disk1
- **Description:** regional-disk1
- **Location:** Regional
  - **Region:** us-central1 (Iowa)
  - **Zone:** us-central1-a
  - **Replica Zone:** us-central1-b
- **Disk source type:** Blank disk
- **Disk settings:** 
  - **Disk type:** Balanced Persistent Disk
  - **Click on COMPARE DISK TYPES** - UNDERSTAND ABOUT VARIOUS DISK OPTIONS
  - **Size:** 200
- **Snapshot schedule (Recommended):**  leave empty (leave to defaults)
- **Encryption:** Google managed encryption 
- **ADD LABEL:** environment=dev 
- Click on **CREATE**
```t
# Create Regional Persistent Disk
gcloud compute disks create regional-disk2 \
    --project=gcplearn9 \
    --type=pd-balanced \
    --description=regional-disk2 \
    --size=200GB \
    --region=us-central1 \
    --replica-zones=projects/gcplearn9/zones/us-central1-a,projects/gcplearn9/zones/us-central1-f
```

## Step-03: Review newly created Regional Disk properties
- Go to Compute Engine -> Storage -> Disks -> **regional-disk1** -> Click on it
- Review **Properties**
- Primarily review the **Zones** property

## Step-04: Create VM Instances
```t
# Create VM Instance: VM1
gcloud compute instances create vm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default 

# Create VM Instance: VM2
gcloud compute instances create vm2 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default 
```

## Step-05: Associate Regional Disk to VM1
- Go to Compute Engine -> VM Instances ->  **vm1** -> Edit
- **Additional disks**
- Click **Attach existing disk**
- **Disk:** regional-disk1
- **Mode:** Read-Only
- **Deletion rule:** Keep Disk
- **Device name:** Based on disk name (default)
- Click on **Done**
- Click on **SAVE**


## Step-06: Associate Regional Disk to VM2
- Go to Compute Engine -> VM Instances ->  **vm2** -> Edit
- **Additional disks**
- Click **Attach existing disk**
- **Disk:** regional-disk1
- **Mode:** Read-Only
- **Deletion rule:** Keep Disk
- **Device name:** Based on disk name (default)
- Click on **Done**
- Click on **SAVE**
- **KEY OBSERVATION:** Review the error message for **Read-Write** when associating to second instance. 


## Step-07: Clean-Up
```t
# Delete VM Instances
gcloud compute instances delete vm1 --zone us-central1-a
gcloud compute instances delete vm2 --zone us-central1-a

# Delete Regional Persistent Disk
gcloud compute disks delete regional-disk1 --region us-central1
gcloud compute disks delete regional-disk2 --region us-central1
```

## Additional Reference
- https://cloud.google.com/compute/docs/disks/regional-persistent-disk