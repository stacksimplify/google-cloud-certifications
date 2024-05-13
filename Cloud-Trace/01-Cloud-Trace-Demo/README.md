---
title: GCP Google Cloud Platform - Cloud Trace
description: Learn to use Cloud Trace in Google Cloud
---

## Step-01: Introduction
1. Create a Google Kubernetes Engine (GKE) cluster by using the Google Cloud CLI.
2. Download and deploy a sample application to GKE cluster.
3. Create a trace by sending an HTTP request to the sample application.
4. View the latency information of the trace we created.
5. Clean up.

## Step-02: Create a GKE cluster
```t
# Set Project
gcloud config set project PROJECT_ID
gcloud config set project gcplearn9

# Create a GKE cluster
gcloud container clusters create cloud-trace-demo --zone us-central1-c

# Configure kubectl
gcloud container clusters get-credentials cloud-trace-demo --zone us-central1-c

# List Kubernetes nodes
kubectl get nodes
```

## Step-03: Download and deploy Sample application
```t
# Clone a Python app from GitHub:
git clone https://github.com/GoogleCloudPlatform/python-docs-samples.git

# Run the following command to deploy the sample application:
cd python-docs-samples/trace/cloud-trace-demo-app-opentelemetry && ./setup.sh
```

## Step-04: Create trace data
```t
# Create a Trace
curl $(kubectl get svc -o=jsonpath='{.items[?(@.metadata.name=="cloud-trace-demo-a")].status.loadBalancer.ingress[0].ip}')

## Sample output
Hello, I am service A
And I am service B
Hello, I am service C
```

## Step-05: View latency data
- Go to Cloud Monitoring -> Explore -> Trace Explorer

## Step-06: Clean-up
```t
# Delete Kubernetes Resources
cd python-docs-samples/trace/cloud-trace-demo-app-opentelemetry
kubectl delete -f app/cloud-trace-demo.yaml

# Delete Kubernetes Cluster
Go to Kubernetes Engine -> Clusters -> cloud-trace-demo -> DELETE
```

## Additional Reference
- https://cloud.google.com/trace/docs/trace-app-latency
- https://cloud.google.com/trace/docs
- **Node.js App:** https://cloud.google.com/trace/docs/setup/nodejs-ot
