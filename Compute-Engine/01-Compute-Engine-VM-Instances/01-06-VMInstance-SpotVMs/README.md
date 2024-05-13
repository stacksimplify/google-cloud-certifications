---
title: Google Cloud Create VM instance with Spot VMs
description: Learn to Create VM instance with Spot VM Option
---

## Step-01: Introduction
- **Google Cloud Console:** Create VM instance using VM Provisioning Model: SPOT 
- **gcloud CLI:** Create VM instance using VM Provisioning Model: SPOT 

## Step-02: Create a VM Instance
- Go to Virtual Machines -> VM Instances -> Create Instance -> New VM Instance -> Provide required details
- **Name:** demo6-vm-spot
- **Labels:** environment: dev
- **Region:** us-central1
- **Zone:** us-central1-a 
- **Machine Configuration:** 
  - **Series:** E2
  - **Machine Type:** e2-micro
- **Availability Policies:**
  - **VM Provisioning Model:** SPOT  
  - **On VM termination:** STOP or DELETE
- **Display Device:** checked 
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

## Step-03: Verify the VM
- Go to VM Instances -> demo6-vm-spot -> Details Tab
- Review the warning `Spot VMs may be terminated at any time`
- Go to **Availability policies** and Verify `VM provisioning model`

## Step-04: Access Application
```t
# Access Application
http://<EXTERNAL-IP-OF-VM>
```

## Step-05: Delete VM
```t
# Delete VM Instance
gcloud compute instances delete demo6-vm-spot --zone us-central1-a
```

## Step-06: Create Spot VM Instance using gcloud
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance
# --instance-termination-action: Options  STOP OR DELETE
gcloud compute instances create demo6-vm-spot-gcloud \
  --provisioning-model=SPOT \
  --instance-termination-action=STOP \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh     

# Access Application 
http://<external-ip-of-vm>

# Delete VM Instance
gcloud compute instances delete demo6-vm-spot-gcloud --zone us-central1-a
```

## Additional References
- [Spot VMs](https://cloud.google.com/compute/docs/instances/spot)
