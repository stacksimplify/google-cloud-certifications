---
title: Kubernetes Jobs - Basics
description: Learn and Implement Kubernetes Job Basics
---

## Step-01: Introduction
1. Review Kubernetes Job yaml file
2. Deploy and verify the job
3. Create Kubernetes job imperatively using `kubectl job`
4. Clean-up both jobs

## Step-02: job1.yaml
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  # Unique key of the Job instance
  name: job1
spec:
  template:
    metadata:
      name: job1
    spec:
      containers:
      - name: job1
        image: alpine
        command: ['sh', '-c', 'echo Kubernetes Jobs Demo ; sleep 30']
      # Do not restart containers after they exit
      restartPolicy: Never
```

## Step-03: Deploy Kubernetes Manifests
```t
# Deploy Kubernetes Manifests
kubectl apply -f kube-manifests
[or]
kubectl create -f kube-manifests

# List Jobs
kubectl get jobs

# Describe Job
kubectl describe job job1

# List Pods
kubectl get pods
Observation:
1. We see this Pod ran for around 30 seconds. 2. Then Pod status turns to Completed.

# Describe Pod
kubect describe pod <POD-NAME>
```

## Step-04: Delete the Job
```t
# Delete the Job
kubectl delete job job1
```

## Step-05: Create Job using kubectl Imperative command and clean-up
```t
# Create Job
kubectl create job job2 --image=alpine -- sh -c 'echo Kubernetes Jobs Basics Demo ; sleep 30'

# List the Job
kubectl get jobs

# List the Pods
kubectl get pods

# Delete Job
kubectl delete job job2
```
