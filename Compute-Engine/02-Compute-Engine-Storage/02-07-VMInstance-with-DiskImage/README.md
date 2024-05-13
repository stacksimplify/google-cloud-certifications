---
title: Google Cloud Create VM instance with Disk Image
description: Learn to Create VM instance with Disk Image on Google Cloud Platform GCP
---

## Step-01: Introduction
- An image is a replica of a disk that contains the applications and operating system needed to start a VM. 
- You can create custom images or use public images pre-configured with Linux or Windows 
- Understand Compute Engine -> Storage -> Disks
- VM Boot Disk can be created using
  - Public Images
  - Custom Images
  - Snapshots
  - Existing Disks
- Create a Disk Image from any of the existing VM Disk
- Create VM Instance with Disk Image

## Step-02: Explore currently available Images in GCP
- Go to Compute Engine -> Storage -> Images 
- Review Disk images on GCP

## Step-03: Create VM Instance
```t
# Create VM Instance
gcloud compute instances create demo8-vm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 

# List Compute Instances
gcloud compute instances list   
gcloud compute instances list --filter='name:demo8-vm1'

# Access via Browser or curl
curl http://<external-ip-address>
http://<external-ip-address>

# Stop VM Instance (To create disk image)
gcloud compute instances stop demo8-vm1 --zone=us-central1-a
gcloud compute instances list --filter='name:demo8-vm1'

```

## Step-04: Create Disk Image
- **Option-1:** Go to Compute Engine -> Storage -> Disks -> demo8-vm1 -> Actions -> Create Image
- **Option-2:** Go to Compute Engine -> Storage -> Images -> Create Image
- **Name:** demo8-vm1-disk-image-v1
- **Source:** Disk
- **Source Disk:** demo8-vm1
- **Location:** Multi-regional (United States)
- **Family:** mynginx-apps
- **Description:** empty (leave to defaults)
- **Labels:** environment=dev, business-tier=hr
- **Encryption:** Google-managed key
- Click on **Create**
```t
# Create Disk Image from a Disk
gcloud compute images create demo8-vm1-disk-image-v1 \
    --project=gcplearn9 \
    --family=mynginx-apps \
    --source-disk=demo8-vm1 \
    --source-disk-zone=us-central1-a \
    --storage-location=us

# List Disk Images
gcloud compute images list --filter='name:demo8-vm1-disk-image-v1'
```
## Step-05: Review Disk Image Properties
- Go to Compute Engine -> Storage -> Images ->  demo8-vm1-disk-image-v1
- Review Disk Image Properties

## Step-06: Create VM Instance from Disk Image
- Go to Compute Engine -> Storage -> Images ->  demo8-vm1-disk-image-v1
- Click on **CREATE INSTANCE**
- **Name:** demo8-vm2-from-disk-image
- **Labels:** environment: dev
- **Region:** us-central1
- **Zone:** us-central1-a 
- **Machine Family:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Availability policies:**
  - **VM provisioning model:** Standard  
- **Display Device:** unchecked (leave to default)
- **Confidential VM Service:** unchecked (leave to default)
- **Container:** unchecked (leave to default)
- **Boot Disk:** Custom Image
  - **Name:** demo8-vm1-disk-image-v1
  - **Boot Disk Type:** New Balanced Persistent Disk
  - **Size (GB):** 10
  - **Image:** demo8-vm1-disk-image-v1
- **Identity and API Access:**
  - **Service Account:** Compute Engine default Service Account
  - **Access Scopes:** Allow default Access
- **Firewall**
  - Allow HTTP Traffic
- **Advanced Options:** LEAVE TO DEFAULTS
- Click on **Create**
- **KEY OBSERVATION:** We didn't pass any `Startup Script` here to install Webserver, but newly created VM instance will have the webserver. 
```t
# Create VM Instance from a Disk Image
gcloud compute instances create demo8-vm2-from-disk-image \
    --project=gcplearn9 \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --network-interface=subnet=default \
    --tags=http-server \
    --create-disk=image=projects/gcplearn9/global/images/demo8-vm1-disk-image-v1
```

## Step-06: Verify newly created VM
```t
# Connect to VM instance using cloud shell 
gcloud compute ssh --zone "us-central1-a" "demo8-vm2-from-disk-image" --project "gcplearn9"
hostname

# Access Application
curl http://<EXTERNAL-IP-ADDRESS>
Observation: 
1. You will see the hostname will be as `demo8-vm1` in index.html even though hostnae of VM is `demo8-vm2-from-disk-image` because it is a disk clone from demo8-vm1 using Disk Image creation
2. This is just an observation to tell that we are using demo8-vm1 disk here from Disk Image
```

## Step-07: How to create new disk using Disk Image ?
- Goto Storage -> Disks -> CREATE DISK
- **SOURCE:** Image
- **SOURE IMAGE:** demo8-vm1-disk-image-v1
- Verify Image list 

## Step-08: Disk Image - Deprecate Option
- Go to Compute Engine -> Storage -> Images -> demo8-vm1-disk-image-v1 -> Actions -> Deprecate

## Step-09: Disk Image - Delete Option
- Go to Compute Engine -> Storage -> Images -> demo8-vm1-disk-image-v1 -> Select CHECK BOX
- Click on **DELETE**

## Step-13: Delete or Stop VM to avoid charges
```t
# Delete VM: demo8-vm2-from-disk-image
gcloud compute instances delete demo8-vm2-from-disk-image --zone=us-central1-a
gcloud compute instances list --filter='name:demo8-vm2-from-disk-image'

# Delete VM: demo8-vm1  (DONT DELETE WE WILL USE IN NEXT DEMO)
gcloud compute instances delete demo8-vm1 --zone=us-central1-a
gcloud compute instances list --filter='name:demo8-vm1'
```


## Additional Reference
- [Linux application consistent persistent disk snapshot](https://cloud.google.com/compute/docs/disks/creating-linux-application-consistent-pd-snapshots)