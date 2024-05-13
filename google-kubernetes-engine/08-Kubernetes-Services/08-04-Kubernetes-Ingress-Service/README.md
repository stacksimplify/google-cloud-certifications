---
title: GCP Google Kubernetes Engine GKE Ingress Context Path Routing
description: Implement GCP Google Kubernetes Engine GKE Ingress Context Path Routing
---

## Step-01: Introduction
- Ingress Context Path based Routing
- Discuss about the Architecture we are going to build as part of this Section
- We are going to deploy all these 3 apps in kubernetes with context path based routing enabled in Ingress Controller
  - /app1/* - should go to app1-nginx-nodeport-service
  - /app2/* - should go to app2-nginx-nodeport-service
  - /*    - should go to  app3-nginx-nodeport-service


## Step-02: Review Nginx App1, App2 & App3 Deployment & Service
- Differences for all 3 apps will be only one field from kubernetes manifests perspective and additionally their naming conventions
  - **Kubernetes Deployment:** Container Image name
- **App1 Nginx: 01-Nginx-App1-Deployment-and-NodePortService.yaml**
  - **image:** ghcr.io/stacksimplify/kube-nginxapp1:1.0.0
- **App2 Nginx: 02-Nginx-App2-Deployment-and-NodePortService.yaml**
  - **image:** ghcr.io/stacksimplify/kube-nginxapp2:1.0.0
- **App3 Nginx: 03-Nginx-App3-Deployment-and-NodePortService.yaml**
  - **image:** ghcr.io/stacksimplify/kubenginx:1.0.0


## Step-03: 04-Ingress-ContextPath-Based-Routing.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-cpr
  annotations:
    # External Load Balancer  
    kubernetes.io/ingress.class: "gce"   
    # Complete GKE Ingress Controller Behavior: https://cloud.google.com/kubernetes-engine/docs/concepts/ingress 
spec: 
  defaultBackend:
    service:
      name: app3-nginx-nodeport-service
      port:
        number: 80                            
  rules:
    - http:
        paths:           
          - path: /app1
            pathType: Prefix
            backend:
              service:
                name: app1-nginx-nodeport-service
                port: 
                  number: 80
          - path: /app2
            pathType: Prefix
            backend:
              service:
                name: app2-nginx-nodeport-service
                port: 
                  number: 80
#          - path: /
#            pathType: Prefix
#            backend:
#              service:
#                name: app3-nginx-nodeport-service
#                port: 
#                  number: 80                     
```

## Step-04: Deploy kube-manifests and test
```t
# Deploy Kubernetes manifests
kubectl apply -f kube-manifests

# List Pods
kubectl get pods

# List Services
kubectl get svc

# List Ingress Load Balancers
kubectl get ingress

# Describe Ingress and view Rules
kubectl describe ingress ingress-cpr
```

## Step-05: Access Application
```t
# Important Note
Wait for 3 to 5 minutes for the Load Balancer to completely create and ready for use else we will get HTTP 502 errors

# Access Application
http://<ADDRESS-FIELD-FROM-GET-INGRESS-OUTPUT>/app1/index.html
http://<ADDRESS-FIELD-FROM-GET-INGRESS-OUTPUT>/app2/index.html
http://<ADDRESS-FIELD-FROM-GET-INGRESS-OUTPUT>/
```


## Step-06: Verify Load Balancer
- Go to Load Balancing -> Click on Load balancer
### Load Balancer View 
- DETAILS Tab
  - Frontend
  - Host and Path Rules
  - Backend Services
  - Health Checks
- MONITORING TAB
- CACHING TAB 
### Load Balancer Components View
- FORWARDING RULES
- TARGET PROXIES
- BACKEND SERVICES
- BACKEND BUCKETS
- CERTIFICATES
- TARGET POOLS


## Step-07: Clean Up
```t
# Delete Kubernetes Resources
kubectl delete -f kube-manifests
```
