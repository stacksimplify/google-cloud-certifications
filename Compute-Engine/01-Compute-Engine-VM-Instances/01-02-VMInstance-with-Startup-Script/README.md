---
title: Google Cloud Create VM instance with Startup Script
description: Learn to create VM instance with Startup Script on Google Cloud Platform GCP
---

## Step-01: Introduction
1. We are going to provision VM with startup script
2. Verify if all the steps outlined in startup script got executed during the creation of the VM. 
3. Verify `Deletion protection`
4. Implement `Project Level Startup Script` and test it. 

## Step-02: Create VM Instance
- Enable `Google Compute Engine API`
- Go to Virtual Machines -> VM Instances -> Create Instance -> New VM Instance -> Provide required details
- **Name:** demo2-vm-startupscript
- **Labels:** environment: dev
- **Region:** us-central1
- **Zone:** us-central1-a 
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Availability Policies:**
  - **VM Provisioning Model:** Standard    
- **Display Device:** unchecked (leave to default)
- **Confidential VM Service:** unchecked (leave to default)
- **Container:** unchecked (leave to default)
- **Boot Disk:** Leave to defaults  
- **Identity and API Access:**
  - **Service Account:** Compute Engine default Service Account
  - **Access Scopes:** Allow default Access
- **Firewall**
  - Allow HTTP Traffic
- **Advanced Options**
  - **Management:**
    - **Description:** demo2-vm-startupscript
    - **Deletion Protection:** Enable it
    - **Reservations:** Automatically use created reservation (leave to default)
    - **Automation:**
      - **Startup Script:** Copy paste content from `webserver-install.sh` file
```t
#!/bin/bash
sudo apt install -y telnet
sudo apt install -y nginx
sudo systemctl enable nginx
sudo chmod -R 755 /var/www/html
HOSTNAME=$(hostname)
sudo echo "<!DOCTYPE html> <html> <body style='background-color:rgb(250, 210, 210);'> <h1>Welcome to StackSimplify - WebVM App1 </h1> <p><strong>VM Hostname:</strong> $HOSTNAME</p> <p><strong>VM IP Address:</strong> $(hostname -I)</p> <p><strong>Application Version:</strong> V1</p> <p>Google Cloud Platform - Demos</p> </body></html>" | sudo tee /var/www/html/index.html
```
  - **Metadata:** empty (leave to default)
  - **Data Encryption:** Leave to defaults
- Click on **Create**

## Step-03: View Logs in Logs Explorer
- Go to VM Instances -> demo2-vm-startupscript -> View Logs
- Wait for sometime so that VM can provision the webserver defined in startup script

## Step-04: Connect to VM and Verify
1. Go to VM Instances -> demo2-vm-startupscript -> SSH -> Open in browser window
```t
# Verify logs
grep nginx /var/log/dpkg.log
grep nginx /var/log/auth.log
more /var/log/auth.log

# Verify nginx binaries installed
dpkg --get-selections | grep nginx
apt list --installed | grep nginx

# Verify Webserver Static Pages
cd /usr/share/nginx/html
ls
```

## Step-05: Access Webserver Pages
```t
# Access Webserver Pages
http://<external-ip-of-vm>
```
## Step-06: Verify Deletion protection Setting
- Go to VM Instances -> demo2-vm-startupscript
- `Delete` Option should be in disabled state.
- Verify the same for demo1-vm
- Go to VM Instances -> demo1-vm
- `Delete` Option should be in enabled state.

## Step-07: How to delete a VM whose Delete Protection is enabled ? 
1. Edit VM
2. Disable `Deletion protection` setting (Uncheck it)
3. Save changes
4. Now if we verify `Delete` setting should be in enabled state

## Step-08: Delete VM 
- Delete VM whose name is `demo2-vm-startupscript-similar`

## Step-09: Define Project Level Startup Script
- Go to Compute Engine -> Settings -> Metadata 
- Click on **Edit**
```t
# Add Metadata Key
startup-script

# Add Metadata Value
#!/bin/bash
sudo apt install -y telnet
sudo apt install -y nginx
sudo systemctl enable nginx
sudo chmod -R 755 /var/www/html
HOSTNAME=$(hostname)
sudo echo "<!DOCTYPE html> <html> <body style='background-color:rgb(250, 210, 310);'> <h1>PROJECT-LEVEL STARTUP SCRIPT Welcome to StackSimplify - WebVM App1 </h1> <p><strong>VM Hostname:</strong> $HOSTNAME</p> <p><strong>VM IP Address:</strong> $(hostname -I)</p> <p><strong>Application Version:</strong> V1</p> <p>Google Cloud Platform - Demos</p> </body></html>" | sudo tee /var/www/html/index.html
```

## Step-10: Create New VM
- Go to Virtual Machines -> VM Instances -> Create Instance -> New VM Instance -> Provide required details
- **Name:** projectlevel-startuscript-demo
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Firewall**
  - Allow HTTP Traffic
- **REST ALL LEAVE TO DEFAULTS**  
- Click on **Create**

## Step-11: Verify by accessing webserver pages
- Go to Compute Engine -> VM Instances -> **projectlevel-startuscript-demo**
- If required, you can do SSH connect and verify
```t
# Access Webserver Pages
http://<external-ip-of-vm>
```

## Step-12: How to override project level Startup Script?
- Provide the start-script at VM instance level overrides the project level startup script metadata
- Create a new VM
- **Name:** override-projectlevel-startuscript
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Firewall**
  - Allow HTTP Traffic
- **Management**
  - **Automation:**
    - **Startup Script:** Copy paste content from `override-webserver-install.sh` file  
- **REST ALL LEAVE TO DEFAULTS**  
- Click on **Create**

## Step-13: Verify by accessing webserver pages
- Go to Compute Engine -> VM Instances -> **override-projectlevel-startuscript**
- If required, you can do SSH connect and verify
```t
# Access Webserver Pages
http://<external-ip-of-vm>
```

## Step-14: Delete VMs
```t
# Delete VMs
projectlevel-startuscript-demo
override-projectlevel-startuscript
```

## Step-15: Stop VM to avoid charges
- Go to VM Instances -> demo2-vm-startupscript  -> Stop
- Verify Notifications at the top right corner.
- **Additional Observation:** When VM is stopped, Public IP or External IP is released

## Step-16: Remove Project level Metadata created for Startup Scripts
- Go to Compute Engine -> Settings -> Metadata -> EDIT
- Delete `startup-script` Metadata
- Click on **SAVE**
