---
title: Google Cloud SSH Keys Metadata-Managed Instance Level
description: Learn to Master SSH Keys Metadata-Managed at Instance Level on Google Cloud Platform GCP
---

## Step-01: Introduction
1. **Metadata-managed** SSH Connections
   1. **Automatically Configured at Project Level:** Temporarily grant a user access to an instance (so far we are using this one)
   2. **Manually Managing SSH Keys in Metadata:** Generate SSH keys and upload to Project Medatada
   3. **Instance-Level** Public SSH Keys
2. **OS Login-managed** SSH connections (Google Recommended)
3. In this section, we are going to focus on SSH Keys Metadata-Managed at Instance level

## Step-02: Create SSH Keys Manually - Public and Private Key
- [Risks of Manual Key Management](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#risks)
```t
# Switch Directory
cd ssh-keys

# Generate SSH Keys
ssh-keygen -t rsa -f ssh-keys-instance-level -C sshinstanceleveluser1

# File Names
SSH Private Key: ssh-keys-instance-level
SSH Public Key: ssh-keys-instance-level.pub

# Restrict access to your private key so that only you can read it and nobody can write to it
chmod 400 ssh-keys-instance-level

# Copy content from ssh-keys-instance-level.pub
cat ssh-keys-instance-level.pub
```

## Step-03: Upload Custom SSH Public Key and Username to VM Instance
- Go to Compute Engine -> VM Instances -> vm1 -> Edit
- **SSH Keys**
   - **Block Project-wide SSH Keys:** Check the box (Enable it)
   - Click on **Add Item**
```t
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCjveFK/CHYMMnUtlNk6f5sDNXfQlaz6TgJwcZWFHm5EGAjoUqkq5c3JknFINnF0W3Ad33+GNZheBl9FRDtxkUC+QjSQcVEEcMd4Z6F0wGD/V/oj7WSNHbSzMlUWKSeUF0225EsaZjM8Bx2YQdWxmqr0RTFXviSsqRfc4SYB82ELD75BQF4eq6IoAvC8/q40+5tFR+ytRaPRk5gnhm/3ae4/Jl0X2SmoVqvvhHRVgsop31danjYLlG5Gup7gyx+wu0ADW5U0FWZB7UJY/GB6DywBEgHH8oer96Ow4iPh3yZ9AhnIIi/Kum5TcXE6EYHDfvzJILeXhVFt4Wvnc7TO36pSMFTxF1+/oKge6hoSqconcDoNZb87smqTUcuTkMqlP7xBejeViUXzrmhi/QAWFbqnVDQn+cH77/lM8ZN5DUjxk0GhKNBdk5WJuXzFmZngrLNcVHcAeGlcr6k+gSUkmNQXtuyCYyYeUmhE0ceTPNS4F/MgU5LaNcMATTYW+YBqsU= sshinstanceleveluser1
```   
- Click on **SAVE**

## Step-04: Connect using your Local Desktop Terminal
```t
# Connect from MacOS / Windows10 CMD line
cd ssh-keys
ssh -i ssh-keys-instance-level sshinstanceleveluser1@104.198.236.153
```

## Step-05: Connect using Project Level SSH Keys - Custom
- **Observation:** As we have enabled the option `Block Project-wide SSH Keys` at VM Instance level, we have got access denied for project level SSH keys
```t
# Connect from MacOS / Windows10 CMD line - Project Level Custom SSH Key from previous demo
cd 04-02-SSHKeys-Project-Level-Metadata/ssh-keys
ssh -i ssh-keys-custom sshcustomuser1@104.198.236.153

# Sample Output
Kalyans-Mac-mini:ssh-keys-custom kalyanreddy$ ssh -i ssh-keys-custom sshcustomuser1@104.198.236.153
sshcustomuser1@104.198.236.153: Permission denied (publickey).
Kalyans-Mac-mini:ssh-keys-custom kalyanreddy$ 
```

## Step-06: Clean-Up
- Delete Project level metadata
- Delete Project level SSH keys
- Delete Instance level metadata related to SSH keys
