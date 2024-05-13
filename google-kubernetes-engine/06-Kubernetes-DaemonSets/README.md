---
title: Kubernetes - DaemonSets
description: Learn and Implement Kubernetes DaemonSets
---

## Step-01: Introduction
- Understand Kubernetes DaemonSets
- Review sample DaemonSet

## Step-02: Review DaemonSet
```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: myapp1-daemonset
  namespace: default
  labels:
    app: myapp
spec:
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp-container
        image: ghcr.io/stacksimplify/kubenginx:1.0.0
```


## Step-03: Deploy and Verify 
```t
# Deploy Kubernetes Resources
kubectl apply -f kube-manifests/

# Verify DaemonSet
kubectl get daemonset
kubectl get ds

# Verify Pods
kubectl get pods -o wide
Observation: 
1. Verify if pods got scheduled on Nodes created for NodePool:linuxapps-nodepool
NodePool:default
```

## Step-05: Clean-Up
```t
# Delete Kubernetes Resources
kubectl delete -f kube-manifests/

# Delete Node pool 
gcloud container node-pools delete "linuxapps-nodepool" \
  --cluster "standard-public-cluster-1" \
  --location "us-central1"
```




