---
title: Google Cloud Create Simple GCP GCE VM Instance
description: Learn to create Simple GCP GCE VM Instance on Google Cloud Platform GCP
---

## Step-01: Introduction
- We will learn the following concepts as part of this section
- How to create Linux VM Instnace in Google Cloud Platform ? 
- How to connect to Linux VM Instnace in GCP using SSH via Browser ? 
- What are various settings available on SSH via Browser ? 
- How to install a simple webserver on GCP VM Instance and access those sample pages on webserver via Browser using GCP External IP ? 
- How to Manage VM Instances (Stop / Start / Suspend / Resume / Reset / Delete etc)? 

## Step-02: Create VM Instance
- Enable `Google Compute Engine API`
- Go to Virtual Machines -> VM Instances -> Create Instance -> New VM Instance -> Provide required details
- **Name:** demo1-vm
- **Labels:** environment: dev
- **Region:** us-central1
- **Zone:** us-central1-a 
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Availability Policies:**
  - **VM Provisioning Model:** Standard  
- **Display Device:** checked 
- **Confidential VM Service:** unchecked (leave to default)
- **Container:** unchecked (leave to default)
- **Boot Disk:** Leave to defaults
- **Identity and API Access:**
  - **Service Account:** Compute Engine default Service Account
  - **Access Scopes:** Allow default Access
- **Firewall**
  - Allow HTTP Traffic
- **Advanced Options:** We will learn these later in detail, lot to discuss for each and every option 
- Click on **Create**

## Step-03: Discuss about newly created VM (very high level)
1. What are VM Filters ?
2. What is VM Internal IP ?
3. What is VM External IP ? 
4. How to connect to Linux VM ?


## Step-04: Connect to Linux VM Instance using SSH
1. Go to VM Instances -> demo1-vm -> SSH -> Open in browser window
2. Understand what happens in background when opening SSH Connection via browser
  1. SSH Keys transferred to VM
  2. Verify in `.ssh/authorized_keys` file
3. We will talk more about `SSH Keys` in that respective demo in detail with all options  
```t
# After login via SSH Verify ID it logged in
id 
Observation: It should be the id with which you logged in to your Google Cloud Console 

# Verify `/home/<USER_NAME>/.ssh/authorized_keys` 
cat /home/dkalyanreddy/.ssh/authorized_keys
```

## Step-05: Create / Review webserver-install.sh
- Create a simple script named `webserver-install.sh` and put the below contnent and run it 
- **webserver-install.sh**
```t
#!/bin/bash
sudo apt install -y telnet
sudo apt install -y nginx
sudo systemctl enable nginx
sudo chmod -R 755 /var/www/html
HOSTNAME=$(hostname)
sudo echo "<!DOCTYPE html> <html> <body style='background-color:rgb(250, 210, 210);'> <h1>Welcome to StackSimplify - WebVM App1 </h1> <p><strong>VM Hostname:</strong> $HOSTNAME</p> <p><strong>VM IP Address:</strong> $(hostname -I)</p> <p><strong>Application Version:</strong> V1</p> <p>Google Cloud Platform - Demos</p> </body></html>" | sudo tee /var/www/html/index.html
```

## Step-06: Understand SSH Settings when connected via Browser
1. Color Themes
2. Text Size
3. Font
4. Copy Settings
5. Key Board Shortcuts
6. Upload File
7. Download File
8. Instance Details
9. New Connection to VM
10. Change Linux Username

## Step-07: Upload and Run the webserver install script
```t
# Run the commands 
hostname
ip -s addr
Observation:
1. make a note of IP address and hostname

# Upload file
Upload file webserver-install.sh

# Give Permissions 
chmod 755 webserver-install.sh

# Install Webserver using script
./webserver-install.sh

# Verify Files
cd /var/www/html
ls
cd app1
ls
```

## Step-08: Access Webserver Pages
```t
# Access Webserver Pages
http://<external-ip-of-vm>
```

## Step-10: Managing VM Instnace - VM Actions
1. **VM Stop:** Stop shuts down the instance. If the shutdown doesn't complete within 90 seconds, the instance is forced to halt. This can lead to file-system corruption. 
2. **VM Start:** Start the VM
3. **VM Suspend:** The instance will preserve its running state, similar to closing a laptop. You'll be billed for storage of the suspended VM state and any persistent disks it uses. The instance won't be accessible while it's being suspended, which may take a few minutes.
4. **VM Resume:** Resume the VM from suspended state
5. **VM Reset:** Reset performs a hard reset on the instance, which wipes the memory contents of the machine and resets the virtual machine to its initial state. This can lead to filesystem corruption.
6. **VM Delete:** Delete the VM instance
7. **View Network Details:** It will take us to Network Interface Details of a VM
  - Review `Network Interface details`
  - Review `VM Instance details`
  - Review `Firewall Rules`
  - Review `Network Analysis`
8. **Create new Machine Image:** We will have a dedicated demo for this
9. **View logs:** We will have a dedicated demos for this
10. **View Monitoring:** We will have a dedicated demo for this
11. Verify **VM Instance ID** details

## Step-11: Perform VM Action - Suspend and Resume
- Go to VM Instances -> demo1-vm -> Actions -> **Suspend**
- We should see suspend action is success :ballot_box_with_check:
- Go to VM Instances -> demo1-vm -> Actions -> **Start / Resume**
- Exteral IP before and after "suspend and resume" action will vary (Its a Ephemeral IP Address - NOT STATIC)


## Step-12: Perform VM Action - Reset
- Go to VM Instances -> demo1-vm -> Actions -> **Reset**
- Just memory wipes, any data in system memory will be reset
```t
# Access Webserver Pages
http://<external-ip-of-vm>
Observation:
1. Application should be accessible
```

## Step-13: Review VM Settings after Creation
- Go to VM Instances -> demo1-vm
   - Details Tab
   - Observability Tab
   - Screenshots Tab

## Step-14: Stop VM to avoid charges
- Go to VM Instances -> demo1-vm -> Stop
- Verify Notifications at the top right corner.
- **Additional Observation:** When VM is stopped, Public IP or External IP is released

## Step-15: Where is the Boot Disk located for the demo1-vm
- Go to Compute Engine -> Storage -> Disks -> demo1-vm
- Review 
  - DETAILS Tab
  - MONITORING Tab

## References
- [Suspend VM OS Compatability](https://cloud.google.com/compute/docs/instances/suspend-resume-instance#os_compatibility)