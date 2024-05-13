---
title: Kubernetes Jobs - Job Parallelism
description: Learn and Implement Kubernetes Job Parallelism
---

## Step-01: Introduction
1. By default, Job Pods do not run in parallel. 
2. The optional **parallelism** field specifies the maximum desired number of Pods a Job should run concurrently at any given time.

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
        command: ['sh', '-c', 'echo Kubernetes Jobs Demo - Job Completions and Parallelism Test ; sleep 20']
      # Do not restart containers after they exit
      restartPolicy: Never
  # backoffLimit: Number of retries before marking as failed.
  backoffLimit: 4 # Default value is 6
  # completions: Specify how many Pods must successfully complete for job to be considered complete.
  completions: 4
  # parallelism: Specifies the maximum desired number of Pods a Job should run concurrently at any given time.
  parallelism: 2
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
1. We see that 2 pods created first and went to COMPLETED state (2 Pods run concurrently)
2. We see 2 more created after first 2 pods COMPLETED, and finally last 2 pods also went to COMPLETED State
3. In short, "completions:4"  means "4 Pods must successfully complete for job to be considered complete" 
4. At the same time "parallelism: 2" which means "2 pods will run at a time " 


### Sample Output
Kalyans-MacBook-Pro: kdaida$ kubectl get pods
NAME         READY   STATUS      RESTARTS   AGE
job1-6wxcv   0/1     Completed   0          16s
job1-c6j4c   0/1     Completed   0          34s
job1-fnvpt   0/1     Completed   0          34s
job1-jlfwr   0/1     Completed   0          16s


# Describe Pod
kubectl describe pod <POD-NAME>

# List Jobs
kubectl get jobs
Observation: 
1. We can see job is completed "4/4" 

### Sample Output
Kalyans-MacBook-Pro:64-GKE-Kubernetes-Job-Parallelism kdaida$ kubectl get jobs
NAME   COMPLETIONS   DURATION   AGE
job1   4/4           36s        45s


# Describe Job
kubectl describe job job1
```

## Step-04: Delete the Job
```t
# Delete the Job
kubectl delete job job1
```