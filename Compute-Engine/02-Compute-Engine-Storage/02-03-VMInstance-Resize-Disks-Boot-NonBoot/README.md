---
title: Google Cloud Resize Boot and Non-Boot Disks
description: Learn to Resize Boot and Non-Boot Disks on Google Cloud Platform GCP
---

## Step-01: Introduction
- Resize Boot Disk
- Resize Non-Boot Disk
- **Best Practice:** Take snapshots of both disks before doing this Resize step in real-world. In our case, snapshot also holds storage space we will ignore. 

## Step-02: Resize Disks for demo7-vm
- Currently demo7-vm containes Boot Disk and Non-Boot Disk
- **Boot Disk Name:** demo7-vm
- **Non-Boot Disk Name:** mydisk1
- **Boot disk:** 
  - VMs using public images automatically resize the root partition and file system after you've resized the boot disk on the VM and restarted the VM. 
  - If you are using an image that does not support this functionality, you must manually resize the root partition and file system.
- **Non-boot disk:**
  - After resizing the disk, you must extend the file system on the disk to use the added space.
### Stop demo7-vm if not stopped
```t
# Stop VM Instance
gcloud compute instances stop demo7-vm --zone=us-central1-a
gcloud compute instances list --filter='name:demo7-vm'
```  

## Step-03: Resize Boot Disk demo1-vm
- Go to Compute Engine -> Storage -> Disks -> **demo7-vm** -> Edit
- **Size:** 10GB (Current Size)
- **Size:** 20GB (New Size)
- Click on **SAVE**

## Step-04: Resize Non-Boot Disk disk1-nonboot-app1
- Go to Compute Engine -> Storage -> Disks -> **disk1-nonboot-app1** -> Edit
- **Size:** 15GB (Current Size)
- **Size:** 25GB (New Size)
- Click on **SAVE**


## Step-05: Start VM demo7-VM and Connect to VM using SSH and Verify Root Mount Size
- Go to Compute Engine -> VM Instances -> **demo7-vm** -> Actions -> Start
```t
# Start VM Instance
gcloud compute instances start demo7-vm --zone=us-central1-a
gcloud compute instances list --filter='name:demo7-vm'

# Connect to VM instance using cloud shell 
gcloud compute ssh --zone "us-central1-a" "demo7-vm" --project "gcplearn9"

# Verify Root Mount Size 
sudo df -Th

dkalyanreddy@demo7-vm:~$ df -Th
Filesystem     Type      Size  Used Avail Use% Mounted on
udev           devtmpfs  478M     0  478M   0% /dev
tmpfs          tmpfs      98M  392K   98M   1% /run
/dev/sda1      ext4       20G  2.0G   17G  11% /  ----- ROOT MOUNT SIZE CHANGED to 40GB
tmpfs          tmpfs     488M     0  488M   0% /dev/shm
tmpfs          tmpfs     5.0M     0  5.0M   0% /run/lock
/dev/sda15     vfat      124M   11M  114M   9% /boot/efi
/dev/sdb       ext4       15G   28K   15G   1% /mnt/disks/myapp1 -- NONBOOT-DISK NOT CHANGED
tmpfs          tmpfs      98M     0   98M   0% /run/user/1000
dkalyanreddy@demo7-vm:~$ 
```
- In the above case, debian supported automatic root partition and file system resize, so automatically ROOT Partition size increased to from 10GB to 20GB
- If the Operating system you are using doesn't support this, you can follow steps in [google documentation](https://cloud.google.com/compute/docs/disks/resize-persistent-disk)

## Step-06: Resize the Non-Boot Data disk
```t
# Connect to VM instance using cloud shell 
gcloud compute ssh --zone "us-central1-a" "demo7-vm" --project "gcplearn9"

# List Disks
sudo df -Th

# List Devices attached to VM
sudo lsblk
dkalyanreddy@demo7-vm:~$ sudo lsblk
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda       8:0    0   20G  0 disk 
├─sda1    8:1    0 19.9G  0 part /
├─sda14   8:14   0    3M  0 part 
└─sda15   8:15   0  124M  0 part /boot/efi
sdb       8:16   0   25G  0 disk /mnt/disks/myapp1
dkalyanreddy@demo7-vm:~$ 


# If you are using ext4, use the resize2fs command to extend the file system:
sudo resize2fs /dev/DEVICE_NAME
sudo resize2fs /dev/sdb
sudo df -h /dev/sdb
sudo df -Th

## SAMPLE OUTPUT
dkalyanreddy@demo7-vm:~$ df -h /dev/sdb
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb         25G   28K   25G   1% /mnt/disks/myapp1
dkalyanreddy@demo7-vm:~$ sudo df -Th
Filesystem     Type      Size  Used Avail Use% Mounted on
udev           devtmpfs  478M     0  478M   0% /dev
tmpfs          tmpfs      98M  388K   98M   1% /run
/dev/sda1      ext4       20G  2.0G   17G  11% /
tmpfs          tmpfs     488M     0  488M   0% /dev/shm
tmpfs          tmpfs     5.0M     0  5.0M   0% /run/lock
/dev/sda15     vfat      124M   11M  114M   9% /boot/efi
/dev/sdb       ext4       25G   28K   25G   1% /mnt/disks/myapp1
tmpfs          tmpfs      98M     0   98M   0% /run/user/1000
dkalyanreddy@demo7-vm:~$ 
```

## Step-07: Stop or Delete VM to avoid charges
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
- [Resizing Persistent Disks](https://cloud.google.com/compute/docs/disks/working-with-persistent-disks#linux-instances)