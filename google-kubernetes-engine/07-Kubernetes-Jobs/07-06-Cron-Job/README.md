---
title: Kubernetes Cron Jobs
description: Learn and Implement Kubernetes Cron Jobs 
---

## Step-01: Introduction
- Create a Kubernetes Cron Job

## Step-02: cron-job.yaml
```yaml
# cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cron-job-demo
spec:
  schedule: "*/1 * * * *"
  concurrencyPolicy: Allow
  startingDeadlineSeconds: 100
  suspend: false
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox
            args:
            - /bin/sh
            - -c
            - date; echo "Hello, World!"
          restartPolicy: OnFailure
```

## Step-03: Deploy and Verify
```t
# Deploy Cron Job Kubernetes Resource
kubectl apply -f kube-manifests/

# List Cron Jobs
kubectl get cronjob
kubectl get cj

# Describe Cron Job
kubectl describe cronjob cron-job-demo 
Observation:
1. Review the events

# List Pods
kubectl get pods
kubectl get pods --watch
Observation: 
1. Every minute cronjob will run which will create a pod and will run to completion
```

## Step-04: Clean-Up
```t
# Delete Cron Job
kubectl delete cronjob cron-job-demo 
```

