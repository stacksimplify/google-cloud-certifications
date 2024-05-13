---
title: GCP Google Kubernetes Engine Autopilot Cluster
description: Implement GCP Google Kubernetes Engine GKE Autopilot Cluster
---

## Step-01: Introduction
- Create GKE Autopilot Cluster
- Understand in detail about GKE Autopilot cluster

## Step-02: Create GKE Autopilot Private Cluster
- Go to Kubernetes Engine -> Clusters -> **CREATE**
- Create Cluster -> GKE Autopilot -> **CONFIGURE**
### Cluster Basics
- **Name:** autopilot-cluster-public-1
- **Region:** us-central1
### Fleet Registration
- LEAVE TO DEFAULTS
### Networking
- **Network:** default  (LEAVE TO DEFAULTS)
- **Node subnet:** default (LEAVE TO DEFAULTS)
- **IPv4 Network access:** Public Cluster
- **Access control plane using its external IP address:** DEFAULT CHECKED
- **Control plane ip range:** 172.18.0.0/28
### Advanced Settings
- LEAVE TO DEFAULTS
- Click on **CREATE** 
```t
# Create GKE Autopilot Private cluster
gcloud container clusters create-auto "autopilot-cluster-public-1" \
  --region "us-central1" \
  --master-ipv4-cidr "172.18.0.0/28" \
  --network "default" \
  --subnetwork "default" 
```

## Step-03: Access GKE Autopilot Private Cluster from Cloud Shell
```t
# Configure kubeconfig for kubectl
gcloud container clusters get-credentials <CLUSTER-NAME> --region <REGION> --project <PROJECT>
gcloud container clusters get-credentials autopilot-cluster-public-1 --region us-central1 --project gcplearn9


# List Kubernetes Nodes
kubectl get nodes

# List Pods
kubectl get pods -n kube-system
```

## Step-04: Review Kubernetes Manifests
### Step-04-01: 01-kubernetes-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment 
metadata: #Dictionary
  name: myapp1-deployment
spec: # Dictionary
  replicas: 5 
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
          resources:
            requests:
              memory: "128Mi" # 128 MebiByte is equal to 135 Megabyte (MB)
              cpu: "200m" # `m` means milliCPU
            limits:
              memory: "256Mi"
              cpu: "400m"  # 1000m is equal to 1 VCPU core                           
```
### Step-04-02: 02-kubernetes-loadbalancer-service.yaml
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

## Step-05: Deploy Kubernetes Manifests
```t
# Deploy Kubernetes Manifests
kubectl apply -f kube-manifests

# List Deployments
kubectl get deploy

# List Pods
kubectl get pods
Observation:
1. It will take few minutes (2 to 3 minutes) for pods to come online (Pending to Ready status)
2. Nodes will be provisioned as per the need in Autopilot clusters

# List Services
kubectl get svc

# List Nodes
kubectl get nodes
Observation:
1. Nodes will be provisioned as needed
2. These nodes are managed by GKE
3. These nodes are not visible to us in Google Compute Engine too

# Access Application
http://<EXTERNAL-IP-OF-GET-SERVICE-OUTPUT>
```

## Step-06: Scale your Application
```t
# Scale your Application
kubectl scale --replicas=15 deployment/myapp1-deployment

# List Pods
kubectl get pods

# List Nodes
kubectl get nodes
```

## Step-07: Clean-Up
```t
# Delete Kubernetes Resources
kubectl delete -f kube-manifests

# List Kubernetes
kubectl get nodes
Observation:
1. After few minutes ( 5 to 10 minutes ) these will nodes will be terminated

# Delete GKE Autopilot Cluster 
Go to Kubernetes Engine > Clusters -> autopilot-cluster-public-1 -> DELETE
```


## References
- https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview#default_container_resource_requests
- https://cloud.google.com/kubernetes-engine/quotas#limits_per_cluster