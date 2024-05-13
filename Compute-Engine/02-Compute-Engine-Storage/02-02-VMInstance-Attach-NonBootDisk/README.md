---
title: Google Cloud Create Non Boot Disk and attach to VM
description: Learn to Create Non Boot Disk and attach to VM on Google Cloud Platform GCP
---

## Step-01: Introduction
1. Create Non-Boot disk using Compute Engine Storage Disks
2. Attach the non-boot Disk to VM
3. Mount the disk in VM
4. Create some files and verify the same 

## Step-02: Create a new VM Instance
```t
# Create VM Instance
gcloud compute instances create demo7-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 

# List Compute Instances
gcloud compute instances list   
```

## Step-03: Create Disk (Non-Boot)
- Go to Compute Engine -> Storage -> Disks -> Create Disk
- **Name:** mydisk1
- **Description:** mydisk1
- **Location:** Single Zone
- **Region:** us-central1
- **Zone:** us-central1-a
- **Disk source type:** Blank disk
- **Disk settings:** 
  - **Disk type:** Balanced Persistent Disk
  - **Click on COMPARE DISK TYPES** - UNDERSTAND ABOUT VARIOUS DISK OPTIONS
  - **Size:** 15GB
- **Snapshot schedule (Recommended):**  leave empty (leave to defaults)
- **Encryption:** 
  - **Customer Managed Encryption Key (CMEK):** kalyankey1    
  - Click on **GRANT** to provide access to `The service-562846405594@compute-system.iam.gserviceaccount.com service account does not have the "cloudkms.cryptoKeyEncrypterDecrypter" role. Verify the service account has permission to encrypt/decrypt with the selected key.`
- **ADD LABEL:** environment=dev 
- Click on **CREATE**
```t
# Createa a Blank Disk
gcloud compute disks create mydisk1 \
    --project=gcplearn9 \
    --type=pd-balanced \
    --description=mydisk1 \
    --size=15GB \
    --zone=us-central1-a

# Createa a Blank Disk with KMS Key
gcloud compute disks create mydisk1 \
    --project=gcplearn9 \
    --type=pd-balanced \
    --description=mydisk1 \
    --size=15GB \
    --zone=us-central1-a \
    --kms-key=projects/gcplearn9/locations/global/keyRings/my-keyring3/cryptoKeys/kalyankey1    
```

## Step-04: Attach this disk to VM
- Go to Compute Engine -> VM Instances -> demo1-vm -> Edit
- **Additional Disks** 
  - Click on **Attach existing disk**
  - **Disk:** mydisk1
  - **Mode:** Read/Write
  - **Deletion Rule:** keep disk
  - **Device Name:** Based on disk name (default)
  - Click on **SAVE**
- Click on **SAVE**

## Step-05: List disks that are attached to your instance
- `sdb` is the device name for the new blank persistent disk.
```t
# Connect to VM instance using cloud shell
gcloud compute ssh --zone "us-central1-a" "demo7-vm" --project "gcplearn9"

# Use the symlink created for your attached disk to determine which device to format.
ls -l /dev/disk/by-id/google-*

## Sample Output
dkalyanreddy@demo1-vm:~$ ls -l /dev/disk/by-id/google-*
lrwxrwxrwx 1 root root  9 Mar 27 09:16 /dev/disk/by-id/google-demo1-vm -> ../../sda
lrwxrwxrwx 1 root root 10 Mar 27 09:16 /dev/disk/by-id/google-demo1-vm-part1 -> ../../sda1
lrwxrwxrwx 1 root root 11 Mar 27 09:16 /dev/disk/by-id/google-demo1-vm-part14 -> ../../sda14
lrwxrwxrwx 1 root root 11 Mar 27 09:16 /dev/disk/by-id/google-demo1-vm-part15 -> ../../sda15
lrwxrwxrwx 1 root root  9 Mar 27 09:16 /dev/disk/by-id/google-disk1-nonboot-app1 -> ../../sdb
dkalyanreddy@demo1-vm:~$

# Format disk using mkfs command
sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/DEVICE_NAME
sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb

# Create Mount Directory
sudo mkdir -p /mnt/disks/MOUNT_DIR
sudo mkdir -p /mnt/disks/myapp1

# Mount Disk
sudo mount -o discard,defaults /dev/DEVICE_NAME /mnt/disks/MOUNT_DIR
sudo mount -o discard,defaults /dev/sdb /mnt/disks/myapp1

# Enable Read Write permissions on disk
sudo chmod a+w /mnt/disks/MOUNT_DIR
sudo chmod a+w /mnt/disks/myapp1

# Verify Mount Point
df -h

## Sample Output
dkalyanreddy@demo7-vm:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            478M     0  478M   0% /dev
tmpfs            98M  388K   98M   1% /run
/dev/sda1       9.7G  2.0G  7.2G  22% /
tmpfs           488M     0  488M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/sda15      124M   11M  114M   9% /boot/efi
tmpfs            98M     0   98M   0% /run/user/1000
/dev/sdb         15G   24K   15G   1% /mnt/disks/myapp1


# Create File in newly mouted disk
echo "New disk attached" >> /mnt/disks/myapp1/newdisk.txt
cat /mnt/disks/app1-disk/newdisk.txt
```

## Step-06: Configure automatic mounting on VM restart
```t
# Backup fstab
sudo cp /etc/fstab /etc/fstab.backup

# Use the blkid command to list the UUID for the disk.
sudo blkid /dev/DEVICE_NAME
sudo blkid /dev/sdb

# Create Mountpoint entry and update in /etc/fstab
UUID=UUID_VALUE /mnt/disks/MOUNT_DIR ext4 discard,defaults,MOUNT_OPTION 0 2
UUID=88dfae9c-9c25-4e99-81a6-17825a5bd70b /mnt/disks/myapp1 ext4 discard,defaults,nofail 0 2

# Make the mount point permanent by adding in /etc/fstab (if not after VM reboot it will not be available)
sudo vi /etc/fstab
UUID=88dfae9c-9c25-4e99-81a6-17825a5bd70b /mnt/disks/myapp1 ext4 discard,defaults,nofail 0 2
[or]
echo UUID=88dfae9c-9c25-4e99-81a6-17825a5bd70b /mnt/disks/myapp1 ext4 discard,defaults,nofail 0 2 | sudo tee -a /etc/fstab

# Verify /etc/fstab
cat /etc/fstab

# Run mount -a to see if any errors
sudo mount -a
exit
```
## Step-07: Stop and Start VM to verify if new disk still attached to VM
```t
## Reboot VM
# Stop VM Instance
gcloud compute instances stop demo7-vm --zone=us-central1-a
gcloud compute instances list --filter='name:demo7-vm'

# Start VM Instance
gcloud compute instances start demo7-vm --zone=us-central1-a
gcloud compute instances list --filter='name:demo7-vm'

# Connect to VM instance using cloud shell and Verify the new disk attached
gcloud compute ssh --zone "us-central1-a" "demo7-vm" --project "gcplearn9"
df -h
cat /mnt/disks/myapp1/newdisk.txt
echo "my new file 101" >> /mnt/disks/myapp1/mynewfile.txt
ls /mnt/disks/myapp1/
cat /mnt/disks/myapp1/mynewfile.txt
exit
```

## Step-08: Clean-Up to Avoid Charges
- DONT DELETE THESE, WE WILL USE ion DEMO 02-03 later, just STOP THE VM
```t
# Stop VM Instance
gcloud compute instances stop demo7-vm --zone=us-central1-a
gcloud compute instances list --filter='name:demo7-vm'

# Delete VM 
gcloud compute instances delete demo7-vm --zone=us-central1-a
gcloud compute instances list --filter='name:demo7-vm'

# Delete Disk 
gcloud compute disks list 
gcloud compute disks delete mydisk1 --zone=us-central1-a
gcloud compute disks list 
```

## Additional Reference
- [Add Persistent Disk](https://cloud.google.com/compute/docs/disks/add-persistent-disk)
- [Format and Mount Disk](https://cloud.google.com/compute/docs/disks/format-mount-disk-linux)