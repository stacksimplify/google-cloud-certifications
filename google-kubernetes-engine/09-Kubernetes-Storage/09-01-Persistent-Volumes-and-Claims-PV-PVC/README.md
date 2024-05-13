---
title: Kubernetes Persistent Volumes (PV) and Volume Claims (PVC)
description: Learn Kubernetes Persistent Volumes (PV) and Volume Claims (PVC)
---

## Step-01: Introduction
- Use predefined Storage Class `standard-rwo`
- `standard-rwo` uses balanced persistent disk

## Step-02: List Kubernetes Storage Classes in GKE Cluster
```t
# List Storage Classes
kubectl get sc

# Also verify GCE PD CSI Setting in GKE cluster
Goto GKE Cluster -> DETAILS -> FEATURES
Compute Engine persistent disk CSI Driver	(Should be enabled)
```

## Step-03: 01-persistent-volume-claim.yaml
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mypvc1
spec: 
  accessModes:
    - ReadWriteOnce
  storageClassName: standard-rwo
  resources: 
    requests:
      storage: 1Gi
```

## Step-04: 02-mypod1.yaml
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: mypod1
spec:
  containers:
    - name: pod-demo
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: pvc-demo-vol
  volumes:
    - name: pvc-demo-vol
      persistentVolumeClaim:
       claimName: mypvc1
```

## Step-05: Deploy kube-manifests
```t
# Deploy PVC manifest
kubectl apply -f kube-manifests/01-persistent-volume-claim.yaml

# List Storage Classes
kubectl get sc
kubectl describe sc standard-rwo
Observation:
1. VolumeBindingMode:     WaitForFirstConsumer
2. This setting instructs Kubernetes to provision a persistent disk in the same zone that the Pod gets scheduled to. 
3. In short, it will wait till pod is scheduled to create a Persistent Volume (PV)

# List PVC and PV
kubectl get pvc
kubectl get pv
Observation:
1. PVC will be in pending state due to Volume binding mode WaitForFirstConsumer  

# Deploy Pod Manifest
kubectl apply -f kube-manifests/02-mypod1.yaml

# List Pods
kubectl get pods

# List PVC and PV
kubectl get pvc
kubectl get pv
Observation:
1. Persistent Volume (PV) will get created when pod is deployed
2. Goto Compute Engine -> Storage -> Disks - You should see the disk created

# Connect to Pod mypod1 and create a file
kubectl exec -it mypod1 -- /bin/bash

# Execute below commands in mypod1
echo "PVC and PV Demo 101" >> /usr/share/nginx/html/index.html
cat /usr/share/nginx/html/index.html
ls /usr/share/nginx/html
curl localhost
exit

# Delete Pod
kubectl delete pod mypod1

# Verify if PV and PVC deleted when pod deleted
kubectl get pvc
kubectl get pv
Observation:
1. PV and PVC should be present
2. These are persistent disks and will not be deleted when attached workloads (Pods) are deleted
```

## Step-06: 03-mypod2.yaml
- Mount the existing PVC created Volume in new pod and verify
```yaml
kind: Pod
apiVersion: v1
metadata:
  name: mypod2
spec:
  containers:
    - name: pod-demo
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: pvc-demo-vol
  volumes:
    - name: pvc-demo-vol
      persistentVolumeClaim:
       claimName: mypvc1
```
## Step-07: Deploy mypod2 and verify
```t
# Deploy mypod2
kubectl apply -f kube-manifests/03-mypod2.yaml

# List Pods
kubectl get pods

# Connec to Pod and Verify
kubectl exec -it mypod2 -- /bin/bash

# Execute below commands in mypod2
cat /usr/share/nginx/html/index.html
ls /usr/share/nginx/html
curl localhost
exit
Observation:
1. We should find the index.html 
```

## Step-08: Clean-Up
```t
# Delete kube-manifests
kubectl delete -f kube-manifests/

# Verify if Persistent Disk got deleted
kubectl get pvc
kubectl get pv
Goto Compute Engine -> Storage -> Disks
```

## Reference
- [Using the Compute Engine persistent disk CSI Driver](https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/gce-pd-csi-driver)

