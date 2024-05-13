---
title: GCP Google Kubernetes Engine Cluster Autoscaler
description: Implement GKE Cluster Autoscaler
---

## Step-01: Introduction
- Implement Google GKE Nodepool Autoscaling
### Pre-requisite: Create GKE Cluster with default node pool
```t
# Create GKE Cluster with default node pool 
gcloud container clusters create "standard-public-cluster-1" \
  --machine-type "e2-micro" \
  --disk-size "20" \
  --spot \
  --num-nodes "1" \
  --region "us-central1"
```

## Step-02: NodePool Autoscaling
- Go to Cluster -> standard-public-cluster-1 -> NODES -> default-pool -> EDIT
- Verify if `Cluster Autoscaler` enabled
- Review additional settings
  - Location Policy: Balanced or Any
  - Size limits type: Per zone limits or Total limits
```t
# We will select
Location Policy: Balanced

# Nodes Per Zone
Minimum number of nodes (per zone): 1
Maximum number of nodes (per zone): 3
```


## Step-03: Review 01-kubernetes-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment 
metadata: 
  name: myapp1-deployment
spec: 
  replicas: 1
  selector:
    matchLabels:
      app: myapp1
  template:  
    metadata:
      name: myapp1-pod
      labels:
        app: myapp1  
    spec:
      containers: 
        - name: myapp1-container
          image: ghcr.io/stacksimplify/kubenginx:1.0.0
          ports: 
            - containerPort: 80  
          resources:
            requests:
              memory: "5Mi" # 128 MebiByte is equal to 135 Megabyte (MB)
              cpu: "25m" # `m` means milliCPU
            limits:
              memory: "50Mi"
              cpu: "50m"  # 1000m is equal to 1 VCPU core                                      
```

## Step-04: Deploy and Verify
```t
# Deploy Kubernetes Resources
kubectl apply -f kube-manifests

# List Pods
kubectl get pods

# List Nodes
kubectl get nodes

# Scale the Deployment
kubectl scale deployment myapp1-deployment --replicas=10

# List Nodes
kubectl get nodes
Observation:
1. Nodes will be autoscaled
2. new nodes will be created.
```

## Step-05: Clean-Up
```t
# Delete Kubernetes Resources
kubectl apply -f kube-manifests

# Verify every 5 to 10 minutes, nodes will be scaled-in 
kubectl get nodes
Observation:
1. Unused nodes will be terminated
2. After few minutes (15 to 30 minutes) we will notice that we will be running the cluster with only 1 node
```

