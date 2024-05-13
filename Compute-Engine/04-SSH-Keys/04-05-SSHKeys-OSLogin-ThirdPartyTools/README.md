---
title: Google Cloud SSH Keys using OS Login Third Party Tools
description: Learn to Master SSH Keys using OS Login and Third Party Tools on Google Cloud Platform GCP
---

## Step-01: Introduction
1. **Metadata-managed** SSH Connections
   1. **Automatically Configured at Project Level:** Temporarily grant a user access to an instance (so far we are using this one)
   2. **Manually Managing SSH Keys in Metadata:** Generate SSH keys and upload to Project Medatada
   3. **Instance-Level** Public SSH Keys
2. **OS Login-managed** SSH connections (Google Recommended)
3. In this section, we are going to focus on SSH Keys using OS Login how to connect to VMs using Third Party Tools and our own custom SSH Key
4. Discuss about enabling `os-login` at VM Instance level.

## Step-02: Enable OS Login at Project Level (already enabled in previous demo)
- Go to Compute Engine -> Metadata -> Edit
- Click on **Add item**
- Add the following
   - **key:** enable-oslogin	
   - **value:** TRUE
- Click on **SAVE**

## Step-03: Generate SSH Keys using Cloud Shell
```t
# Connect to Cloushell
Go to -> Cloud Shell

# Set Project
gcloud config set project [PROJECT_ID]

# Switch Directory
mkdir ssh-oslogin
cd ssh-oslogin

# Generate SSH Keys
ssh-keygen -t rsa -f ssh-keys-oslogin -C dkalyanreddy_gmail_com

# File Names
SSH Private Key: ssh-keys-oslogin
SSH Public Key: ssh-keys-oslogin.pub

# Restrict access to your private key so that only you can read it and nobody can write to it
chmod 400 ssh-keys-oslogin
```

## Step-04: Add Custom SSH Public Key to OS-Login user profile
```t
# List SSH Keys (Before Adding)
gcloud compute os-login ssh-keys list

# Use the gcloud command-line tool to associate public SSH keys with an account.
gcloud compute os-login ssh-keys add \
    --key-file=KEY_FILE_PATH \
    --ttl=EXPIRE_TIME

gcloud compute os-login ssh-keys add \
    --key-file=ssh-keys-oslogin.pub \
    --ttl=0

# List SSH Keys (After adding)
gcloud compute os-login ssh-keys list

# Describe Profile (to find username)
gcloud compute os-login describe-profile 

gcloud compute os-login ssh-keys remove --key='40bf2d3870aa88105d46fc206821367da5521431ef381b8e73a046696ab080e5'

gcloud compute os-login ssh-keys remove --key='50fc14a59c5eb23331b92e86ad463bcfdd70bddab60cbbf3e7cafbedeaedc5c8'
```

## Step-05: Verify the connectivity to VM
```t
# Get Public IP of VM
Go to Compute Enginer -> VM Instances -> vm -> Copy Public IP

# Login using SSH Command on MacOS or Windows10 CMD
ssh -i ssh-keys-oslogin dkalyanreddy_gmail_com@104.198.236.153
```


## Step-06: Instance Level OS-Login enablement
- Go to Compute Engine -> VM Instances -> vm1 -> Edit
- Under `Custom metadata` add a metadata entry, setting the key to `enable-oslogin` value to `TRUE`
   - key: enable-oslogin
   - value: TRUE
- Click on **SAVE**   

## Additional References
- [SSH using OS Login](https://cloud.google.com/compute/docs/instances/managing-instance-access)