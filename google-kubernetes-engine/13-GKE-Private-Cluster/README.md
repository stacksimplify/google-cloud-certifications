---
title: GCP Google Kubernetes Engine GKE Private Cluster
description: Implement GCP Google Kubernetes Engine GKE Private Cluster
---

## Step-01: Introduction
- Create GKE Private Cluster
- Create Cloud NAT
- Deploy Sample App and Test
 
## Step-02: Create Standard GKE Cluster 
- Go to Kubernetes Engine -> Clusters -> CREATE
- Select **GKE Standard -> CONFIGURE**
### Cluster Basics
- **Name:** standard-private-cluster-1
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
  - **IPv4 network access:** Private cluster
  - **Access control plane using its external IP address:** BY DEFAULT CHECKED
  - **Control Plane IP Range:** 172.16.0.0/28  
  - **Enable Control Plane Global Access:** CHECKED (OPTIONAL)
  - **Control plane authorized networks:** ENABLED 
  - REST ALL LEAVE TO DEFAULTS
```t
# Least secure option: 
Public endpoint access enabled
authorized networks disabled

# Medium secure option: (WE WILL CHOOSE OPTION-2)
Public endpoint access enabled
authorized networks enabled

# High secure option:
Public endpoint access disabled
```  
- **Security:** REVIEW AND LEAVE TO DEFAULTS
- **Metadata:** REVIEW AND LEAVE TO DEFAULTS
- **Features:** REVIEW AND LEAVE TO DEFAULTS
- CLICK ON **CREATE**


## Step-03: Access GKE Private Cluster from Cloud Shell
- Enable Cloud Shell Public IP in GKE Networking Authorized Networks section
```t
# Configure kubeconfig for kubectl
gcloud container clusters get-credentials <CLUSTER-NAME> --region <REGION> --project <PROJECT>
gcloud container clusters get-credentials standard-cluster-private-1 --region us-central1 --project gcplearn9

# List Kubernetes Nodes
kubectl get nodes
Observation:
1. it should fail. 
2.As of now we didnt allow any networks to allow public IP of GKE private cluster

# List existing Authorized Networks
gcloud container clusters describe standard-private-cluster-1 --format "flattened(masterAuthorizedNetworksConfig.cidrBlocks[])" --location "us-central1"

# Get Public IP of Google Cloud Shell
dig +short myip.opendns.com @resolver1.opendns.com

# Add the external address of your Cloud Shell to your cluster's list of authorized networks:
# Template
gcloud container clusters update CLUSTER_NAME \
    --enable-master-authorized-networks \
    --master-authorized-networks EXISTING_AUTH_NETS,CLOUD_SHELL_IP/32 \
    --location us-central1

# Replace Values CLUSTER_NAME, EXISTING_AUTH_NETS, CLOUD_SHELL_IP/32
gcloud container clusters update standard-private-cluster-1 \
    --enable-master-authorized-networks \
    --master-authorized-networks 35.187.230.177/32 \
    --location us-central1
[or]
Go to Cluster -> Details -> Networking -> EDIT -> Control plane authorized networks	

# List Kubernetes Nodes
kubectl get nodes
Observation:
1. It should pass
2. Private GKE cluster nodes should be listed
```

## Step-04: Review kube-manifests: 01-kubernetes-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment 
metadata: #Dictionary
  name: myapp1-deployment
spec: # Dictionary
  replicas: 2
  selector:
    matchLabels:
      app: myapp1
  template:  
    metadata: # Dictionary
      name: myapp1-pod
      labels: # Dictionary
        app: myapp1  # Key value pairs
    spec:
      containers: # List
        - name: myapp1-container
          image: ghcr.io/stacksimplify/kubenginx:1.0.0
          ports: 
            - containerPort: 80      
          imagePullPolicy: Always            
```

## Step-05: Review kube-manifest: 02-kubernetes-loadbalancer-service.yaml
```yaml
apiVersion: v1
kind: Service 
metadata:
  name: myapp1-lb-service
spec:
  type: LoadBalancer # ClusterIp, # NodePort
  selector:
    app: myapp1
  ports: 
    - name: http
      port: 80 # Service Port
      targetPort: 80 # Container Port      
```

## Step-06: Deploy Kubernetes Manifests
```t
# Deploy Kubernetes Manifests
kubectl apply -f kube-manifests/

# Verify Pods 
kubectl get pods 
Observation: SHOULD FAIL - UNABLE TO DOWNLOAD DOCKER IMAGE FROM DOCKER HUB
dkalyanreddy@cloudshell:~/11-GKE-Private-Cluster (gcplearn9)$ kubectl get pods
NAME                                READY   STATUS             RESTARTS   AGE
myapp1-deployment-6f56fd57c-5bfkz   0/1     ImagePullBackOff   0          46s
myapp1-deployment-6f56fd57c-tn4xf   0/1     ImagePullBackOff   0          46s
dkalyanreddy@cloudshell:~/11-GKE-Private-Cluster (gcplearn9)$ 

# Describe Pod
kubectl describe pod <POD-NAME>

# Clean-Up
kubectl delete -f kube-manifests/
```

## Step-07: Create Cloud NAT
- Go to Network Services -> CREATE CLOUD NAT GATEWAY
- **Gateway Name:** gke-us-central1-default-cloudnat-gw
- **Select Cloud Router:** 
  - **Network:** default
  - **Region:** us-central1
  - **Cloud Router:** CREATE NEW ROUTER
    - **Name:** gke-us-central1-cloud-router
    - **Description:** GKE Cloud Router Region us-central1
    - **Network:** default (POPULATED by default)
    - **Region:** us-central1 (POPULATED by default)
    - **BGP Peer keepalive interval:** 20 seconds (LEAVE TO DEFAULT)
    - Click on **CREATE**
- **Cloud NAT Mapping:** LEAVE TO DEFAULTS
- **Destination (external):** LEAVE TO DEFAULTS
- **Stackdriver logging:**  LEAVE TO DEFAULTS
- **Port allocation:** 
  - CHECK **Enable Dynamic Port Allocation**
- **Timeouts for protocol connections:** LEAVE TO DEFAULTS
- CLICK on **CREATE**  

## Step-08: Deploy Kubernetes Manifests
```t
# Deploy Kubernetes Manifests
kubectl apply -f kube-manifests

# Verify Pods 
kubectl get pods 
Observation: SHOULD BE ABLE TO DOWNLOAD THE DOCKER IMAGE

# List Services
kubectl get svc

# Access Application
http://<External-IP>
```
## Step-09: Clean-Up
```t
# Clean-Up
kubectl delete -f kube-manifests
```
