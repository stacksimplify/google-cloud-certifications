---
title: GCP Google Kubernetes Engine Horizontal Pod Autoscaling
description: Implement GKE Cluster Horizontal Pod Autoscaling
---

## Step-01: Introduction
- Implement a Sample Demo with Horizontal Pod Autoscaler

## Step-02: Review Kubernetes Manifests
- Primarily review `HorizontalPodAutoscaler` Resource in file `kube-manifests-autoscalerV2/03-kubernetes-hpa.yaml`
1. 01-kubernetes-deployment.yaml
2. 02-kubernetes-cip-service.yaml
3. 03-kubernetes-hpa.yaml
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cpu
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp1-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 30
```

## Step-03: Deploy Sample App and Verify using kubectl
```t
# Deploy Sample
kubectl apply -f kube-manifests-autoscalerV2

# List Pods
kubectl get pods
Observation: 
1. Currently only 1 pod is running

# List HPA
kubectl get hpa

# Run Load Test (New Terminal)
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://myapp1-cip-service; done"


# List Pods (SCALE UP EVENT)
kubectl get pods
Observation:
1. New pods will be created to reduce the CPU spikes

# kubectl top command
kubectl top pod

# List HPA (after few mins - approx 3 to 5 mins)
kubectl get hpa --watch

# List Pods (SCALE IN EVENT)
kubectl get pods
Observation:
1. Only 1 pod should be running when there is no load on the workloads
```

## Step-04: Clean-Up
```t
# Delete Load Generator Pod which is in Error State
kubectl delete pod load-generator

# Delete Sample App
kubectl delete -f kube-manifests-autoscalerV2
```

## Step-05: Create HPA using Imperative command (kubectl autoscale)
```t
# Deploy Sample (Replicas: 1)
kubectl apply -f kube-manifests-autoscalerV2/01-kubernetes-deployment.yaml

# List Pods
kubectl get pods
Observation: One pod will be running

# Create HPA using imperative command
kubectl autoscale deployment myapp1-deployment --min 3 --max 10 --cpu-percent 30

# List HPA
kubectl get hpa

# List Pods
kubectl get pods
Observation: 3 pods will be running as per --min 3 from HPA imperative command

# Review HPA yaml file
kubectl get hpa myapp1-deployment -o yaml
Observation:
1. It should create a HPA with apiVersion: autoscaling/v2
```

## Step-06: Clean-Up
```t
# Delete Sample App
kubectl delete -f kube-manifests-autoscalerV2/01-kubernetes-deployment.yaml

# Delete HPA
kubectl delete hpa myapp1-deployment
```

## Step-07: kubectl top command
```t
# Nodes
kubectl top node

# Pods
kubectl top pod -n kube-system
```

## References
- https://cloud.google.com/kubernetes-engine/docs/concepts/horizontalpodautoscaler
- https://cloud.google.com/kubernetes-engine/docs/how-to/horizontal-pod-autoscaling
