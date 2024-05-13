---
title: Google Cloud - Sole-tenant Nodes
description: Learn to create GCP GCE sole-tenant Nodes
---
## Step-01: Introduction
- Explore about creating sole-tenant nodes using google cloud console

## Step-02: Create a Sole-tenant Node
- Go to Compute Engine -> Virtual machines -> Sole-tenant Nodes -> CREATE NODE GROUP
### Node group properties
- **Name:** node-group-1
- **Region:** us-central1
- **Zone:** us-central1-a
- Click on **CONTINUE**
### Node template properties
- Click on **CREATE NODE TEMPLATE**
- **Name:** node-template-1
- **Node type:** c2-node-60-240
- **Local SSD:** none
- **GPU accelerator:** none
- **Affinitly Lables**
  - **Key:** appname
  - **Value:** mybankingapps
- Click on **CREATE**
- Click on **CONTINUE**
### Configure autoscaling
- **Autoscaling mode:** on
- **Minimum Number of nodes:** 1
- **Maximum Number of nodes:** 3
- Click on **CONTINUE**
### Configure maintenance settings (optional)
- **Maintenance policy:** Default (RECOMMENDED)
- **Maintenance window:** 0:00 - 4:00
- Click on **CONTINUE**
### Configure share settings (optional)
- Select **Do not share this node group with other projects**
- Click on **CREATE** DONT CREATE IT -  WE ARE JUST EXPLORING

## Step-03: Delete the Node Template 
- Go to Compute Engine -> Virtual machines -> Sole-tenant Nodes -> Node Templates
- Delete **node-template-1**

## Step-04: gcloud: Sole-tenant Node Commands
```t
# List Sole-tenant node types
gcloud compute sole-tenancy node-types list

# List Sole-tenant node templates
gcloud compute sole-tenancy node-templates list

# List Sole-tenant node groups
gcloud compute sole-tenancy node-groups list

# Create a sole-tenant node template
# https://cloud.google.com/compute/docs/nodes/provisioning-sole-tenant-vms#creating-a-sole-tenant-node-template
gcloud compute sole-tenancy node-templates create TEMPLATE_NAME \
  --node-type=NODE_TYPE \
  [--region=REGION \]
  [--node-affinity-labels=AFFINITY_LABELS \]
  [--accelerator type=GPU_TYPE,count=GPU_COUNT \]
  [--disk type=local-ssd,count=DISK_COUNT,size=DISK_SIZE \]
  [--cpu-overcommit-type=CPU_OVERCOMMIT_TYPE]

# Create a sole-tenant node group
# https://cloud.google.com/compute/docs/nodes/provisioning-sole-tenant-vms#create_a_sole-tenant_node_group
gcloud compute sole-tenancy node-groups create GROUP_NAME \
  --node-template=TEMPLATE_NAME \
  --target-size=TARGET_SIZE \
  [--zone=ZONE \]
  [--maintenance-policy=MAINTENANCE_POLICY \]
  [--maintenance-window-start-time=START_TIME \]
  [--autoscaler-mode=AUTOSCALER_MODE: \
  --min-nodes=MIN_NODES \
  --max-nodes=MAX_NODES]  

# Provision a sole-tenant VM
# https://cloud.google.com/compute/docs/nodes/provisioning-sole-tenant-vms#provision_a_sole-tenant_vm
gcloud compute instances create VM_NAME \
  [--zone=ZONE \]
  --image-family=IMAGE_FAMILY \
  --image-project=IMAGE_PROJECT \
  --node-group=GROUP_NAME \
  --machine-type=MACHINE_TYPE \
  [--maintenance-policy=MAINTENANCE_POLICY \]
  [--accelerator type=GPU_TYPE,count=GPU_COUNT \]
  [--local-ssd interface=SSD_INTERFACE \]
  [--restart-on-failure]  
```

