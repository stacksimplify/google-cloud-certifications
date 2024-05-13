---
title: Kubernetes - Rollback Deployment
description: Learn and Implement Kubernetes Rollback Deployment
---

## Step-00: Introduction
- We can rollback a deployment in two ways.
  - Previous Version
  - Specific Version
- Rolling Restarts  

## Step-01: Rollback a Deployment to previous version

### Step-01-01: Check the Rollout History of a Deployment
```t
# List Deployment Rollout History
kubectl rollout history deployment/<Deployment-Name>
kubectl rollout history deployment/my-first-deployment  
```

### Step-01-02: Verify changes in each revision
- **Observation:** Review the "Annotations" and "Image" tags for clear understanding about changes.
```t
# List Deployment History with revision information
kubectl rollout history deployment/my-first-deployment --revision=1
kubectl rollout history deployment/my-first-deployment --revision=2
kubectl rollout history deployment/my-first-deployment --revision=3
```

### Step-01-03: Rollback to previous version
- **Observation:** If we rollback, it will go back to revision-2 and its number increases to revision-4
```t
# Undo Deployment
kubectl rollout undo deployment/my-first-deployment

# List Deployment Rollout History
kubectl rollout history deployment/my-first-deployment  
```

### Step-01-04: Verify Deployment, Pods, ReplicaSets
```t
# Verify Deployment, Pods, ReplicaSets
kubectl get deploy
kubectl get rs
kubectl get po
kubectl describe deploy my-first-deployment
```

### Step-01-05: Access the Application using Public IP
- We should see `Application Version:V2` whenever we access the application in browser
```t
# Get Load Balancer IP
kubectl get svc

# Application URL
http://<External-IP-from-get-service-output>
```


## Step-02: Rollback to specific revision
### Step-02-01: Check the Rollout History of a Deployment
```t
# List Deployment Rollout History
kubectl rollout history deployment/<Deployment-Name>
kubectl rollout history deployment/my-first-deployment 
```
### Step-02-02: Rollback to specific revision
```t
# Rollback Deployment to Specific Revision
kubectl rollout undo deployment/my-first-deployment --to-revision=3
```

### Step-02-03: List Deployment History
- **Observation:** If we rollback to revision 3, it will go back to revision-3 and its number increases to revision-5 in rollout history
```t
# List Deployment Rollout History
kubectl rollout history deployment/my-first-deployment
```

### Step-02-04: Access the Application using Public IP
- We should see `Application Version:V3` whenever we access the application in browser
```t
# Get Load Balancer IP
kubectl get svc

# Application URL
http://<Load-Balancer-IP>
```

## Step-03: Rolling Restarts of Application
- Rolling restarts will kill the existing pods and recreate new pods in a rolling fashion. 
```t
# Rolling Restarts
kubectl rollout restart deployment/<Deployment-Name>
kubectl rollout restart deployment/my-first-deployment

# Get list of Pods
kubectl get po
```