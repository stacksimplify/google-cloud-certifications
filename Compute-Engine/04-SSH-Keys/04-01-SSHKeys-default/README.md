---
title: Google Cloud SSH Keys Metadata-Managed Project Level
description: Learn to Master SSH Keys Metadata-Managed at Project Level on Google Cloud Platform GCP
---

## Step-01: Introduction
1. **Metadata-managed** SSH Connections
   1. **Automatically Configured at Project Level:** Temporarily grant a user access to an instance (so far we are using this one)
   2. **Manually Managing SSH Keys in Metadata:** Generate SSH keys and upload to Project Medatada
   3. **Instance-Level** Public SSH Keys
2. **OS Login-managed** SSH connections (Google Recommended)
3. In this section, we are going to focus on `Automatically Configured at Project Level` at Project level

## Step-02: Create a VM Instance
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create VM Instance
gcloud compute instances create vm1 \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --network-interface=subnet=default \
  --tags=http-server \
  --metadata-from-file=startup-script=webserver-install.sh 
```
## Step-03: Connect to VM instance using Open in New browser window
- Go to Compute Engine -> Virtual Machines -> VM Instances -> VM1 -> SSH -> Open in new browser window
- Review **Compute Engine -> Settings -> Metadata -> SSH Keys**
- **What happens during this process ?**
1. By default, Google Compute Engine uses custom project and/or instance metadata to configure SSH keys 
2. If we use `OS Login`, metadata SSH Keys are disabled. 
3. As of now we are using this option so far, lets understand this in detail.
4. Go to Compute Engine -> Settings -> Metadata -> SSH Keys
  1. **Observation-1:** We can use Username and Public Key with expiration dates.
  2. **Observation-2:** Username will be the user we have logged to Google Cloud Console trimming the `@domain.com` part of our username (Example: dkalyanreddy@gmail.com, Username field will have dkalyanreddy)
5. Your public and private SSH keys are stored in your browser session.
6. Your SSH key has an expiry of five minutes. Five minutes after Compute Engine creates the key, you can't use the SSH key to connect to the VM anymore.
7. Compute Engine uploads the public SSH key and username to metadata.
8. Compute Engine retrieves the SSH key and username from metadata, creates a user account with the username and public key, and stores the public key in your user's ~/.ssh/authorized_keys file on the VM.
9. Compute Engine grants your connection.

> :warning: **VERY VERY IMPORTANT NOTE-1:** Google doesn't have access to your private key.

> :warning: **VERY VERY IMPORTANT NOTE-2:** In this approach we can only access our Linux VMs using Google Cloud console browser based SSH and using GCloud Command line`gcloud compute ssh`.  We cannot connect using Third Party Tools because SSH Private Key is generated dynamically and stays valid for 5 mins only on browser session. 

> :warning: **VERY VERY IMPORTANT NOTE-3:** In addition, it takes good amount of time to connect to VM, because it need to generate temporary SSH keys during the runtime when we are connecting to VM and also valid only for 5 minutes. Not feasible in Real-World case when we deal with 100's of VMs with SSH connections open for larger deployments etc. 

## Step-03: Create new Username for automatic Metadata-Managed SSH Connection approach
- Go to Compute Engine -> VM Instances -> vm1 -> SSH -> Open in Browser Window
- Go to newly opened SSH Browser Window -> Settings -> Change Linux Username -> kalyanreddy -> Click on **Change**
- **Observation:**
  - New SSH keys will be generated in browser session for user `demouser1`
  - We will relogin with new user `demouser1`
- Review **Compute Engine -> Settings -> Metadata -> SSH Keys**

## Step-04: SSH Connect to Linux VM using gcloud in Cloud Shell
- Go to Compute Engine -> Virtual Machines -> VM Instances -> vm1 -> SSH -> View gcloud command
```t
# Set GCP Project
gcloud config set project <PROJECT-ID>
gcloud config set project gcplearn9

# Connect to VM using gcloud in Cloud Shell
gcloud compute ssh --zone "us-central1-a" "vm2" --project "gcplearn9"
```

## Additional References
- [SSH Access](https://cloud.google.com/compute/docs/instances/access-overview)
- [Instance SSH](https://cloud.google.com/compute/docs/instances/ssh)
- [Adding or Removing SSH keys](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys)
- [SSH OS Login](https://cloud.google.com/compute/docs/oslogin)
- [Managing Instance Access](https://cloud.google.com/compute/docs/instances/managing-instance-access)
