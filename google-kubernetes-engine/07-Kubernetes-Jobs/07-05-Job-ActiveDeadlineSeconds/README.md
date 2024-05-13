---
title: Kubernetes Jobs - Job activeDeadlineSeconds
description: Learn and Implement Kubernetes Job activeDeadlineSeconds
---

## Step-01: Introduction
- **activeDeadlineSeconds:**  is an attribute that specifies the maximum duration (in seconds) that the Job is allowed to run
- If the Job does not complete within the specified duration, Kubernetes will terminate the Job regardless of its completion status
- This attribute is useful for setting a timeout for Jobs, ensuring that they do not run indefinitely and freeing up resources if they take too long to complete.
- You can specify a deadline value using the optional `.spec.activeDeadlineSeconds` field of the Job.
- The `activeDeadlineSeconds value` is relative to the startTime of the Job, and applies to the duration of the Job, no matter how many Pods are created.
- **Important Note:** Ensure that you add the activeDeadlineSecond value to the `Job's spec field`. The spec field in the Pod template field also accepts an activeDeadlineSeconds value.

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
  # activeDeadlineSeconds: Specifies the total runtime of the Kubernetes Job
  activeDeadlineSeconds: 5 # 5 Seconds should fail, change to 60 Seconds and Job should pass 
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
1. Pods will terminate because the time it takes to complete each pod is 20 seconds.
2. We have given activeDeadlineSeconds as 5 seconds so it will fail because the whole time we have given is 5 seconds to complete the Job. 


### Sample Output
Kalyans-MacBook-Pro:$ kubectl get pods
NAME         READY   STATUS        RESTARTS   AGE
job1-ckw6l   1/1     Terminating   0          12s
job1-lvqk5   1/1     Terminating   0          12s


# List Jobs
kubectl get jobs
Observation: 
1. We can see job is completed with "0/4" 

### Sample Output
Kalyans-MacBook-Pro:$ kubectl get jobs
NAME   COMPLETIONS   DURATION   AGE
job1   0/4           18s        18s


# Describe Job
kubectl describe job job1

### Sample Output
Events:
  Type     Reason            Age    From            Message
  ----     ------            ----   ----            -------
  Normal   SuccessfulCreate  3m44s  job-controller  Created pod: job1-lvqk5
  Normal   SuccessfulCreate  3m44s  job-controller  Created pod: job1-ckw6l
  Normal   SuccessfulDelete  3m38s  job-controller  Deleted pod: job1-lvqk5
  Normal   SuccessfulDelete  3m38s  job-controller  Deleted pod: job1-ckw6l
  Warning  DeadlineExceeded  3m38s  job-controller  Job was active longer than specified deadline
```

## Step-04: Delete the Job
```t
# Delete the Job
kubectl delete job job1
```

## Step-06: Update job1.yaml
```yaml
activeDeadlineSeconds: 60
```
## Step-07: Deploy Kubernetes Manifests
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
1. All 4 pods successfully complete (2 pods at a time)

### Sample Output
Kalyans-MacBook-Pro:$ kubectl get pods
NAME         READY   STATUS      RESTARTS   AGE
job1-2744n   0/1     Completed   0          18s
job1-98xl7   0/1     Completed   0          35s
job1-hwzgd   0/1     Completed   0          35s
job1-n6pzk   0/1     Completed   0          18s


# Describe Pod
kubectl describe pod <POD-NAME>

# List Jobs
kubectl get jobs
Observation: 
1. We can see job is completed "4/4" 

### Sample Output
Kalyans-MacBook-Pro:65-GKE-Kubernetes-Job-ActiveDeadlineSeconds kdaida$ kubectl get jobs
NAME   COMPLETIONS   DURATION   AGE
job1   4/4           34s        77s

# Describe Job
kubectl describe job job1

## Sample Output
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  98s   job-controller  Created pod: job1-hwzgd
  Normal  SuccessfulCreate  98s   job-controller  Created pod: job1-98xl7
  Normal  SuccessfulCreate  81s   job-controller  Created pod: job1-2744n
  Normal  SuccessfulCreate  81s   job-controller  Created pod: job1-n6pzk
  Normal  Completed         64s   job-controller  Job completed
```

## Step-08: Delete the Job
```t
# Delete the Job
kubectl delete job job1
```