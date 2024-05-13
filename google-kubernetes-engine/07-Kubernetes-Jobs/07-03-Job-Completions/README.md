---
title: Kubernetes Jobs - Job Completions
description: Learn and Implement Kubernetes Job Completions
---

## Step-01: Introduction
- **Job completions:** Specify how many Pods must successfully complete for job to be considered complete.
- We are going to put `completions: 4`
- In short, "completions:4" means "4 Pods must successfully complete for job to be considered complete"

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
        command: ['sh', '-c', 'echo Kubernetes Jobs Demo - Job Completions Test ; sleep 20']
      # Do not restart containers after they exit
      restartPolicy: Never
  # backoffLimit: Number of retries before marking as failed.
  backoffLimit: 4 # Default value is 6
  # completions: Specify how many Pods must successfully complete for job to be considered complete.
  completions: 4
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
1. We see that 4 pods created and went to COMPLETED state
2. Each pod created and run in a sequential manner (one after the other)
3. In short, "completions:4" means "4 Pods must successfully complete for job to be considered complete"

### Sample Output
Kalyans-MacBook-Pro:$ kubectl get pods
NAME         READY   STATUS      RESTARTS   AGE
job1-6lq5m   0/1     Completed   0          110s
job1-ff98k   0/1     Completed   0          95s
job1-rbgqf   0/1     Completed   0          63s
job1-x6pd8   0/1     Completed   0          79s


# Describe Pod
kubectl describe pod <POD-NAME>

# List Jobs
kubectl get jobs
Observation: 
1. We can see job is completed "4/4" 

### Sample Output
Kalyans-MacBook-Pro:$ kubectl get job
NAME   COMPLETIONS   DURATION   AGE
job1   4/4           63s        115s

# Describe Job
kubectl describe job job1
```

## Step-04: Delete the Job
```t
# Delete the Job
kubectl delete job job1
```