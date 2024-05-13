---
title: Kubernetes StatefulSets
description: Implement Kubernetes StatefulSets on GKE
---

## Step-01: Introduction
1. Create StatefulSet and Verify StatefulSet concepts
2. Access application deployed using StatefulSet using Headless Service

## Step-02: Review 01-kubernetes-statefulset.yaml
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: myapp1-sts
spec:
  selector:
    matchLabels:
      app: nginx # has to match .spec.template.metadata.labels
  serviceName: "myapp1-hs-svc"
  replicas: 3 # by default is 1
  minReadySeconds: 10 # by default is 0
  template:
    metadata:
      labels:
        app: nginx # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      initContainers:
      - name: init-pass-hostname
        image: alpine
        command: ["/bin/sh", "-c", "echo POD_HOSTNAME: $HOSTNAME > /usr/share/nginx/html/index.html"]
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html   
      containers:
      - name: nginx
        #image: registry.k8s.io/nginx-slim:0.8
        image: ghcr.io/stacksimplify/kubenginx:1.0.0
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html            
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "premium-rwo"
      resources:
        requests:
          storage: 1Gi
```

## Step-03: Review 02-kubernetes-headless-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp1-hs-svc
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
```

## Step-04: Review 03-curl-pod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: curl-pod
spec:
  containers:
  - name: curl
    image: curlimages/curl 
    command: [ "sleep", "600" ]
```

## Step-05: Deploy Kubernetes Resources and Verify StatefulSet
```yaml
# Deploy Kubernetes Resources
kubectl apply -f kube-manifests/

# List Kubernetes Pods
kubectl get pods
Observation:
1. Pods will be created one after the other

# Verify Kubernetes StatefulSets
kubectl get statefulset
kubectl get sts 
Observation:
1. Review the Events
2. PVC Claim will be created for Pod-0
3. Pod-0 will be created
4. PVC Claim will be created for Pod-1
5. Pod-1 will be created
6. Same applies to Pod-2
7. That said  Pods will be created one after the other
```

## Step-06: Verify Persistent Volumes 
```t
# Verify PVC and PV
kubectl get pv
kubectl get pvc
Go to Compute Engine -> Disks -> Verify if 3 persistent disks created
Observation:
1. We will find 3 persistent disks created in Compute Engine for 3 StatefulSet pods
```

## Step-07: Verify Headless Service
```t
# Verify Headless Service
kubectl get svc
kubectl describe svc myapp1-hs-svc # review endpoints 
kubectl get endpoints myapp1-hs-svc
Observation:
1. Make a note of endpoint IP address
Endpoints:         10.124.0.11:80,10.124.1.12:80,10.124.2.11:80

# Connect to curl-pod
kubectl exec -it curl-pod -- /bin/sh

# Verify Headless Service
curl myapp1-hs-svc.default.svc.cluster.local

# Verify Headless Service in a while loop 
while true; do curl -s "http://myapp1-hs-svc.default.svc.cluster.local"; sleep 1; done
Observation:
1. Traffic will be distributed across multiple statefulset pods
2. Example: Read from all MySQL databases from application

# Verify Independent Headless service endpoints for each statefulset pod
## nslookup Test
nslookup myapp1-sts-0.myapp1-hs-svc.default.svc.cluster.local
nslookup myapp1-sts-1.myapp1-hs-svc.default.svc.cluster.local
nslookup myapp1-sts-2.myapp1-hs-svc.default.svc.cluster.local
Observation:
1. Verify if the IP addresses matches with IP addresses we made a note
Endpoints:         10.124.0.11:80,10.124.1.12:80,10.124.2.11:80

# curl Test
curl myapp1-sts-0.myapp1-hs-svc.default.svc.cluster.local
curl myapp1-sts-1.myapp1-hs-svc.default.svc.cluster.local
curl myapp1-sts-2.myapp1-hs-svc.default.svc.cluster.local
Observation:
1. Request will be sent to that respective pod only
2. Example: Which means we can configure our application to send write requests to specific mysql pod (master mysql pod) 
```
## Step-08: Delete a pod in StatefulSet and understand what happens
```t
# List PV and PVC
kubectl get pvc
kubectl get pv
Observation:
1. make a note of PV and PVC associated with Pod: myapp1-sts-0

# Describe Pod to verify the same
kubectl describe pod myapp1-sts-0
Observation:
1. Verify volumes section to find the claim name
2. We should find ClaimName:  www-myapp1-sts-0

# Delete StatefulSet pod
kubectl get pods
kubectl delete pod myapp1-sts-0
kubectl get pods
Observation: 
1. Pod will be re-created with same name

# Verify new pod created has same volume attached before deletion
kubectl describe pod myapp1-sts-0
Observation:
1. Same PV claim should be present 
2. ClaimName:  www-myapp1-sts-0
```

## Step-09: Clean-Up Resources
```t
# Delete Kubernetes Resources
kubectl delete -f kube-manifests

# Verify PVC and PV
kubectl get pvc
kubectl get pv
Observation:
1. Persistent volumes will not be deleted when statefulset is deleted
2. Go to Compute Engine -> Disks and we should find 3 persistent disks

# Delete PVC 
kubectl delete pvc www-myapp1-sts-0
kubectl delete pvc www-myapp1-sts-1
kubectl delete pvc www-myapp1-sts-2
kubectl get pvc
kubectl get pv # will take couple of minutes to delete the disks
Observation:
1. Persistent volumes will be deleted
2. Go to Compute Engine -> Storage -> Disks and we should find disks were deleted
```
