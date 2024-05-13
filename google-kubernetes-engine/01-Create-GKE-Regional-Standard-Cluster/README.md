---
title: GCP Google Kubernetes Engine - Create GKE Cluster
description: Learn to create Google Kubernetes Engine GKE Cluster
---

## Step-01: Introduction
- Create GKE Regional Standard Cluster 
- Configure Google CloudShell to access GKE Cluster

## Step-02: Create Standard GKE Public Cluster 
### Cluster Basics
- **Name:** standard-public-cluster-1
- **Location type:** Regional
- **Region:** us-central1
- **Specify default node locations:** us-central1-a, us-central1-b, us-central1-c
- REST ALL LEAVE TO DEFAULTS
### Fleet Registration
- REVIEW AND LEAVE TO DEFAULTS
### NODE POOLS
#### NODE POOLS: default-pool
  - **Node pool details**
  - **Name:** default-pool
  - **Number of Nodes (per zone):** 1
  - **OPTIONAL SETTINGS - FOR MORE COST SAVING** 
  - **Enable cluster autoscaler:** Checked
  - **Location policy:** Balanced
  - **Size limits type:** Per Zone limits
  - **Minimum number of nodes:** 0
  - **Maximum number of nodes:** 1
- REST ALL LEAVE TO DEFAULTS
#### Nodes: Configure node settings
- **Machine configuration**
 - **GENERAL PURPOSE SERIES:** E2
 - **Machine Type:** e2-small
 - **Boot disk type:** Balanced persistent disk
 - **Boot disk size(GB):** 20
 - **Enable Node on Spot VMs:** CHECKED
 - REST ALL LEAVE TO DEFAULTS
#### Node Networking: 
- REVIEW AND LEAVE TO DEFAULTS  
#### Node Security: 
- REVIEW AND LEAVE TO DEFAULTS
#### Node Metadata:
- REVIEW AND LEAVE TO DEFAULTS
### CLUSTER
- **Automation:** REVIEW AND LEAVE TO DEFAULTS
- **Networking:** REVIEW AND LEAVE TO DEFAULTS
  - **Network:** default
  - **Node Subnet:** default
  - **IPv4 network access:** Public cluster
  - REST ALL LEAVE TO DEFAULTS
- **Security:** REVIEW AND LEAVE TO DEFAULTS
- **Metadata:** REVIEW AND LEAVE TO DEFAULTS
- **Features:** REVIEW AND LEAVE TO DEFAULTS
- CLICK ON **CREATE**
```t
# Create GKE Cluster with default node pool 
gcloud container clusters create "standard-public-cluster-1" \
  --machine-type "e2-micro" \
  --disk-size "20" \
  --spot \
  --num-nodes "1" \
  --region "us-central1"
```

## Step-03: Verify Cluster Details
- Go to Kubernetes Engine -> Clusters -> **standard-public-cluster-1** -> Review
- Details Tab
- Nodes Tab
  - Review same nodes **Compute Engine**
- Storage Tab
  - Review Storage Classes
- Observability Tab  
- Logs Tab
- Review Cluster Logs
  - Review Cluster Logs **Filter By Severity**
- App Errors Tab  

## Step-04: Install GKE gcloud auth plugin and kubectl
- [Pre-requisite: gcloud cli already installed](https://cloud.google.com/sdk/docs/install)
- [kubectl Authentication in GKE](https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke)
```t
# Verify gke-gcloud-auth-plugin Installation (if not installed, install it)
gke-gcloud-auth-plugin --version 

# FOR DEB BASED SYSTEMS: Install Kubectl authentication plugin for GKE 
sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin

# FOR WINDOWS and MACOS: Install Kubectl authentication plugin for GKE 
gcloud components install gke-gcloud-auth-plugin

# FOR YUM BASED SYSTEMS: Install Kubectl authentication plugin for GKE 
sudo yum install google-cloud-sdk-gke-gcloud-auth-plugin

# Verify gke-gcloud-auth-plugin Installation
FOR Linux/Mac: gke-gcloud-auth-plugin --version 
FOR WINDOWS: gke-gcloud-auth-plugin.exe --version

# Verify, List and Install kubectl (if not installed, install it)
gcloud components list --filter=kubectl
gcloud components install kubectl 

# List Kubernetes Client and Server version
kubectl version --output=yaml
Observation:
1. Server version will not be displayed because we didnt configure th kubeconfig for kubectl yet in this terminal
```

## Step-05: Google CloudShell: Connect to GKE Cluster using kubectl
```t
# Configure kubeconfig for kubectl
gcloud container clusters get-credentials <CLUSTER-NAME> --region <REGION> --project <PROJECT-NAME>
gcloud container clusters get-credentials standard-public-cluster-1 --region us-central1 --project gcplearn9

# List Kubernetes Client and Server version
kubectl version --output=yaml

# List Kubernetes Nodes
kubectl get nodes

# List Kubernetes Nodes (-o wide)
kubectl get nodes -o wide
Observation:
1. Review the EXTERNAL-IP for each GKE Node
2. For Public cluster, we will have the External IP allocated for each GKE Node. 
```

## Step-06: Verify Additional Features in GKE on a High-Level
### Step-06-01: Verify Workloads Tab
- Go to Kubernetes Engine -> Clusters -> **standard-public-cluster-1**
- Workloads -> **SHOW SYSTEM WORKLOADS**

### Step-06-02: Verify Services & Ingress
- Go to Kubernetes Engine -> Clusters -> **standard-public-cluster-1**
- Services & Ingress -> **SHOW SYSTEM OBJECTS**

### Step-06-03: Verify Applications, Secrets & ConfigMaps
- Go to Kubernetes Engine -> Clusters -> **standard-public-cluster-1**
- Applications
- Secrets & ConfigMaps

### Step-06-04: Verify Storage
- Go to Kubernetes Engine -> Clusters -> **standard-public-cluster-1**
- Storage Classes
  - premium-rwo
  - standard
  - standard-rwo

### Step-06-05: Verify the below
### Resource Management
1. Object Browser
2. Backup for GKE
### Features
1. Feature Manager
2. Service Mesh
3. Security Posture
4. Config
5. Policy
### Migrate
1. Migrate to Containers
```